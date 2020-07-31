import json

from django.db.models import Q

from apps.recommend.models import JpaItemUserBehavior
from apps.products.models import JpaItems
from apps.users.models import JpaUsers
import pandas as pd
import numpy as np
import math

from typing import Tuple, List, Dict


class UserItemRecommend:
    """
    基于用户行为的协同过滤
    """
    user: JpaUsers = None
    item: JpaItems = None
    data: dict = {}

    def __init__(self, user: JpaUsers, item: JpaItems, score: dict = None):
        """
        初始化操作，定义行为权重并获取用户行为数据
        :param user: 目标用户
        :param item: 目标商品
        :param score: 行为权重字典
        """
        self.user = user
        self.item = item
        if score is not None:
            self.behavior_score = score
        else:
            self.behavior_score = {1: 1, 2: 2, 3: 3, 4: 4}  # 分别表示 浏览1分，收藏2分，加购物车3分，购买4分
        self._getBrowseData()

    def CosineSim(self, item_tags, i, j)->float:
        """
        余弦相似度计算公式
        :param item_tags: 商品
        :param i: 序列1
        :param j: 序列2
        :return: 余弦相似度，越接近于1表示越相似
        """
        ret = 0
        for b, wib in item_tags[i].items():
            if b in item_tags[j]:
                ret += wib * item_tags[j][b]
        ni = 0
        nj = 0
        for b, w in item_tags[i].items():
            ni += w * w
        for b, w in item_tags[j].items():
            nj += w * w
        if ret == 0:
            return 0
        return ret / math.sqrt(ni * nj)  # 相同的标签上面乘加一下

    def _getBrowseData(self):
        """
        获取基于某个商品的用户行为数据组
        :return:
        """
        # behavior_list = JpaItemUserBehavior.objects.exclude(username=self.user.username).filter(item_id=self.item.id)
        # 根据条件从数据库中获取用户行为数据集
        condition = Q(item_id=self.item.id)
        behavior_user_list = JpaItemUserBehavior.objects.filter(condition)
        # 遍历数据集，加工成所需格式
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
        user1_data_list: dict = self.data[user1] if user1 in self.data.keys() else {}
        user2_data_list: dict = self.data[user2] if user2 in self.data.keys() else {}
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
        user1_data_list: dict = self.data[user1] if user1 in self.data.keys() else {}
        user2_data_list: dict = self.data[user2] if user2 in self.data.keys() else {}
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

    def doJob(self, count: int = 10, mode: int = 0) -> List[Tuple[str, float]]:
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


class UserIndexRecommend:
    """
    基于商品标签的TagbasedTFIDF
    算法核心：
    统计用户所有浏览过的商品的标签及次数，计算余弦相似度
    加入时间的比重，越新权重越高
    不同的行为对评分也有不同的分值
    """
    user: JpaUsers = None
    data: dict = {}
    tag_user_num_dict = {}
    item_user_num_dict = {}
    tags_item: dict = None
    user_tags: list = None

    def __init__(self, user: JpaUsers, score: dict = None):
        """
        初始化TagBasedTFIDF算法模型，获取所有商品标签及用户所拥有的商品标签数据
        :param user: 用户类
        :param score: 行为权重字典
        """
        self.user = user
        if score is not None:
            self.behavior_score = score
        else:
            self.behavior_score = {1: 3, 2: 3, 3: 4, 4: 1}  # 分别表示 浏览3分，收藏3分，加购物车4分，购买1分
        self._getUserTags(user_id=user.username)
        self._getTags()
        print("username:", self.user.username)
        print("user_tags:", self.user_tags)
        print("tags_item:", self.tags_item)
        print("tag_user_num:", self.tag_user_num_dict)
        print("item_user_num:", self.item_user_num_dict)
        # self._getBrowseData()

    def _getTags(self, user_id: str = None) -> Dict[str, List[Tuple[str, int]]]:
        """
        获取用户行为表中所有商品tag及权重

        :param user_id: 用户id，若不传则为全部用户行为
        :return: Dict[tag:[(item_id,weight),]]
        """
        # 根据筛选条件获取商品tag数据集
        condition = Q()
        if user_id is not None:
            condition = Q(username=user_id)
        behavior_list = JpaItemUserBehavior.objects.filter(condition).order_by("-happen_time")
        tags_dict = {}
        # 遍历收集商品的标签以及权重，并加工成所需数据结构
        for behavior in behavior_list:
            item_id = behavior.item_id
            print("item_id:",item_id)
            item = JpaItems.objects.get(id=item_id)
            # item user item 处理方法,排除获取单用户的情况，防止数据重复
            if user_id is None:
                if item_id not in self.item_user_num_dict.keys():
                    self.item_user_num_dict[item_id] = {}
                user = behavior.username
                if user not in self.tag_user_num_dict.keys():
                    self.item_user_num_dict[item_id][user] = 1

            tags = item.item_tags
            if tags is None:
                tags = "[]"
            tag_list = json.loads(tags)
            # 针对每个tag，统计其所拥有的行为权重值字段
            for tag in tag_list:
                # tag item 处理方法
                if tag not in tags_dict.keys():
                    # todo 最终决定加入行为权重
                    # tags_dict[tag] = {item_id: 1}
                    tags_dict[tag] = {item_id: self.behavior_score[behavior.behavior_type]}  # 加入权重
                else:
                    if item_id not in tags_dict[tag].keys():
                        # tags_dict[tag][item_id] = 1
                        tags_dict[tag][item_id] = self.behavior_score[behavior.behavior_type]
                    else:
                        # tags_dict[tag][item_id] += 1
                        tags_dict[tag][item_id] += self.behavior_score[behavior.behavior_type]
                # tag user item 处理方法,排除获取单用户的情况，防止数据重复
                if user_id is None:
                    if tag not in self.tag_user_num_dict.keys():
                        self.tag_user_num_dict[tag] = {}
                    user = behavior.username
                    if user not in self.tag_user_num_dict.keys():
                        self.tag_user_num_dict[tag][user] = 1
        # 格式化数据结构，加工成后期易于操作的元组结构
        self.tags_item = {}
        for tag in tags_dict.keys():
            item_weight_list = []
            for item_id in tags_dict[tag]:
                tmp = (item_id, tags_dict[tag][item_id])
                item_weight_list.append(tmp)
            item_weight_list.sort(key=lambda val: val[1], reverse=True)
            # print("{}:{}".format(tag, item_weight_list))
            self.tags_item[tag] = item_weight_list
        return self.tags_item

    def _getUserTags(self, user_id: str) -> List[Tuple[str, int]]:
        """
        获取该用户的商品标签数据集
        :param user_id: 用户id
        :return: 用户商品标签组
        """
        tags_item = self._getTags(user_id=user_id)
        self.user_tags = []
        for tag in tags_item.keys():
            weight_sum = 0
            for item_weight in tags_item[tag]:
                weight_sum += item_weight[1]
            self.user_tags.append((tag, weight_sum))
        self.user_tags.sort(key=lambda val: val[1], reverse=True)
        return self.user_tags

    def _calculate(self) -> List[Tuple[str, int]]:
        """
        计算商品标签间的距离，获得相似度，公式及参数如下。
        P(u,i)=∑sub(b) N(u,b)*N(b,i)
        u:用户
        i:商品
        b:标签
        P(u,i) 用户u对商品i的兴趣公式
        N(u,b) 用户u对标签b的标记次数
        N(b,i) 商品i被标记b标记的次数
        n(sub(b))(sup(u))
        :return: 商品相似度列表
        """
        P = {}
        for tag1, weight1 in self.user_tags:
            if tag1 not in self.tags_item.keys():
                # 如果用户的tag在商品全集中找不到，则返回空列表（理论上不存在这种情况）
                return []
            for item_weight in self.tags_item[tag1]:
                item_id = item_weight[0]
                weight2 = item_weight[1]
                if item_id not in P.keys():
                    P[item_id] = 0
                nbu = len(self.tag_user_num_dict[tag1].keys())
                niu = len(self.item_user_num_dict[item_id].keys())
                P[item_id] += (weight1 * weight2) / ((math.log10(1 + nbu)) * math.log10(1 + niu))
        ret_list = []
        for item_id in P.keys():
            ret_list.append((item_id, P[item_id]))
        ret_list.sort(key=lambda val: val[1], reverse=True)
        print("ret_list:", ret_list)
        return ret_list

    def doJob(self, limit: int = None)->list:
        """
        通过此函数调用算法
        :param limit: 限制返回条数
        :return: 商品信息列表
        """
        ret_list = self._calculate()[:limit]
        item_list = []
        for item, weight in ret_list:
            item_list.append(item)
        return item_list
