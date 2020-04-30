from django.db.models import Q

from apps.recommend.models import JpaItemUserBehavior, JpaItems
from apps.users.models import JpaUsers
import pandas as pd
import numpy as np
import math

from typing import Tuple, List


class RelationRecommend:
    user: JpaUsers = None
    item: JpaItems = None
    data: dict = {}

    def __init__(self, user: JpaUsers, item: JpaItems, score: dict = None):
        self.user = user
        self.item = item
        if score is not None:
            self.behavior_score = score
        else:
            self.behavior_score = {1: 1, 2: 2, 3: 3, 4: 4}  # 分别表示 浏览1分，收藏2分，加购物车3分，购买4分
        self._getBrowseData()

    def _getBrowseData(self):
        # behavior_list = JpaItemUserBehavior.objects.exclude(username=self.user.username).filter(item_id=self.item.id)
        condition = Q(item_id=self.item.id)
        behavior_user_list = JpaItemUserBehavior.objects.filter(condition)
        for behavior_user in behavior_user_list:
            user_id = behavior_user.username
            condition = Q(username=user_id)
            behavior_list = JpaItemUserBehavior.objects.filter(condition)
            for behavior in behavior_list:
                # 先排除非在售的商品列表
                try:
                    item = JpaItems.objects.get(id=behavior.item_id)
                except Exception as e:
                    print("获取商品失败", e)
                    continue
                if item.item_status != 1:
                    continue
                # 判断用户的行为是浏览，收藏，加购物车以及购买中的哪一种
                if behavior.behavior_type in self.behavior_score.keys():
                    user_id = behavior.username
                    # 以用户名为key，存入该用户所有操作过的商品列表以及操作类型，并排除重复信息
                    if user_id not in self.data.keys():
                        # 用户不存在的情况，先创建一个dict
                        self.data[user_id] = {}
                    if behavior.item_id not in self.data[user_id].keys():
                        self.data[user_id][behavior.item_id] = self.behavior_score[behavior.behavior_type]
                    else:
                        # 考虑到用户对一件商品可以有多次的操作以及多次的评分不一定相同
                        # 暂时的做法是取大值保存，即 购买>加购物车>收藏>浏览
                        if self.data[user_id][behavior.item_id] < self.behavior_score[behavior.behavior_type]:
                            self.data[user_id][behavior.item_id] = self.behavior_score[behavior.behavior_type]
                else:
                    print("item_id:", behavior.item_id, "商品状态", behavior.behavior_type, "不在列表内")
        print("data:", self.data)

    def _calcDistance(self, user1: str, user2: str) -> float:
        """
        使用欧式距离计算用户间的距离

        :param user1:
        :param user2:
        :return:
        """
        # 获取两个用户访问过的所有数据，并初始化距离为0
        user1_data_list: dict = self.data[user1]
        user2_data_list: dict = self.data[user2]
        distance = 0.0
        # 找到两个用户都操作过的商品列表，并计算欧氏距离
        for item_id in user1_data_list.keys():
            if item_id in user2_data_list.keys():
                # 计算distance，值越大表示两者越近似
                distance += pow(float(user1_data_list[item_id]) - float(user2_data_list[item_id]), 2)
        print("distance ", user1, "-", user2, ":", distance)
        return 1 / (1 + math.sqrt(distance))  # 这里返回值越小，相似度越大

    def _calcDistance2(self, user1: str, user2: str) -> float:
        """
        使用 Pearson相关系数来衡量两个变量之间的线性相关性，这个方法可以避免两方数据量不统一的问题（一大一小）
        0.8-1.0 极强相关
        0.6-0.8 强相关
        0.4-0.6 中等程度相关
        0.2-0.4 弱相关
        0.0-0.2 极弱相关或无相关

        :param user1:
        :param user2:
        :return:
        """
        # 获取两个用户访问过的所有数据，并初始化距离为0
        user1_data_list: dict = self.data[user1]
        user2_data_list: dict = self.data[user2]
        distance = 0.0
        common = {}
        # 找到两个用户都操作过的商品列表，进行标记
        for item_id in user1_data_list.keys():
            if item_id in user2_data_list.keys():
                # 对商品进行标记
                common[item_id] = 1
        num = len(common)
        if num == 0:
            print("num值为0")
            print("distance ", user1, "-", user2, ":", distance)
            return 0.0  # 如果没有共同操作过的商品，返回结果0
        print("common:", num, common)
        # 计算评分和
        sum1 = sum([user1_data_list[item] for item in common])
        sum2 = sum([user2_data_list[item] for item in common])
        print("sum1:{} sum2:{}".format(sum1, sum2))
        # 计算评分平方和
        sum1Sq = sum([pow(user1_data_list[item], 2) for item in common])
        sum2Sq = sum([pow(user2_data_list[item], 2) for item in common])
        print("sum1Sq:{} sum2Sq:{}".format(sum1Sq, sum2Sq))
        # 计算乘积和
        PSum = sum(user1_data_list[item] * user2_data_list[item] for item in common)
        print("PSum:", PSum)
        # 计算相关系数
        molecule = PSum - (sum1 * sum2 / num)  # 分子
        denominator = math.sqrt((sum1Sq - pow(sum1, 2) / num) * (sum2Sq - pow(sum2, 2) / num))  # 分母
        # denominator = math.sqrt((sum1Sq - pow(sum1 / 2, 2)) * (sum2Sq - pow(sum2 / num, 2)))
        print("分子:", molecule)
        print("分母:", denominator)

        if denominator == 0:
            print("分母为0")
            print("distance ", user1, "-", user2, ":", distance)
            return 0.0  # 出现分母为0的情况
        distance = molecule / denominator
        print("distance ", user1, "-", user2, ":", distance)
        return distance

    def _top_simliar(self, count: int = 10, mode: int = 0) -> list:
        """
        批量计算目标用户与其他用户的距离，并返回指定数量的排行
        :param count: 指定返回数量
        :param mode: 距离计算模型。0 欧式距离，1 Pearson相关系数
        :return:
        """
        self.res = []
        clacDistance = {0: self._calcDistance, 1: self._calcDistance2}
        reverse = {0: False, 1: True}
        for user_id in self.data.keys():
            # 排除与自己的计算，因为在获取数据时并未排除，且不能排除，因此在下面需判断。
            if user_id == self.user.username:
                continue
            simliar = clacDistance[mode](user1=self.user.username, user2=user_id)
            # simliar = self._calcDistance(user1=self.user.username, user2=user_id)
            self.res.append((user_id, simliar))
        self.res.sort(key=lambda val: val[1], reverse=reverse[mode])
        return self.res[:count]

    def recommend(self, count: int = 10, mode: int = 0) -> List[Tuple[str, float]]:
        """
        获得指定条数的推荐数据，以List[Tuple[item_id,score]]的形式返回

        :param count: 返回条数
        :param mode: 距离计算模型。0 欧式距离，1 Pearson相关系数
        :return: List[Tuple[item_id,score]]
        """
        # 获得相似度最高的用户
        simliar_list = self._top_simliar(mode=mode)
        if len(simliar_list) == 0:
            return []
        top_sim_user = simliar_list[0]
        # 获得相似度最高的用户的商品操作记录
        items: dict = self.data[top_sim_user[0]]
        recommend_actions = []
        # 筛选出该用户未操作的商品并添加到列表中
        for item in items.keys():
            if item not in self.data[self.user.username]:
                # 添加 (商品id,商品操作分数)到列表中
                recommend_actions.append((item, items[item]))
        recommend_actions.sort(key=lambda val: val[1], reverse=True)  # 按照操作评分降序排序
        # 返回评分最高的10件商品（基本属于操作过这个商品的其他用户购买过的其他商品）
        print("recommend data:", recommend_actions[:count])
        return recommend_actions[:count]
