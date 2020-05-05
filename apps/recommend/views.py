from django.shortcuts import render
from django.http.response import JsonResponse

from apps.operation.views import TokenUserView
from apps.recommend.models import JpaItems
from extra_apps.CF.base_item import UserItemRecommend, UserIndexRecommend
from extra_apps.tags.main import TfIdf
from extra_apps.m_cos import py_cos_main as COS

from CDC import settings

import json

COS.Initialize(settings.BASE_DIR)


# Create your views here.

class RecommendView(TokenUserView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        if self.user is None:
            return JsonResponse(self.JSON_RETURN_DICT[-101])
        if self.data is None:
            # status -1 json的key错误
            return JsonResponse(self.JSON_RETURN_DICT[-1])
        # 检验json文本外层中是否包含必要的键名
        result, json_ret = self.OuterCheck()
        if request is False:
            return json_ret
        type = self.data["type"]
        subtype = self.data["subtype"]
        data = dict(self.data["data"])
        if type == "recommend":
            if subtype == "item":
                for key in ["item_id"]:
                    if key not in data.keys():
                        return self.JSON_RETURN_DICT[-3]
                item_id = str(data["item_id"])
                try:
                    item = JpaItems.objects.get(id=item_id)
                except Exception as e:
                    # status 100 错误的item id
                    return self.getJsonReturn(100, "Error item id")
                recommend = UserItemRecommend(user=self.user, item=item)
                recommend_list = recommend.doJob(mode=1)
                data_list = []
                for recommend in recommend_list:
                    item_id = recommend[0]
                    try:
                        item = JpaItems.objects.get(id=item_id)
                    except Exception as e:
                        print(e)
                        # status 101 获取推荐信息的商品id失败
                        return self.getJsonReturn(101, "Get recommend data failed")
                    data_dict = {
                        "id": item.id,
                        "store_id": item.store_id,
                        "item_name": item.item_name,
                        "item_des": item.item_des,
                        "item_portrait": item.item_portrait,
                        "item_type": item.item_type,
                        "item_geohash": item.item_geohash,
                        "item_status": item.item_status,
                        "item_stock": item.item_stock,
                        "original_price": item.original_price,
                        "discount_price": item.discount_price,
                        "create_time": item.create_time.timestamp(),
                        "last_modified_time": item.lastmodified_time.timestamp(),
                    }
                    data_list.append(data_dict)
                return self.getJsonReturn(data={"num": len(data_list), "list": data_list})
            elif subtype == "index":
                limit: int = None
                if "limit" in data.keys():
                    limit = int(data["limit"])
                recommend = UserIndexRecommend(user=self.user)
                ret_list = recommend.doJob(limit=limit)
                data_list = []
                for item_id in ret_list:
                    try:
                        item = JpaItems.objects.get(id=item_id)
                    except Exception as e:
                        print(e)
                        # status 100 获取商品信息失败
                        return self.getJsonReturn(100, "Get Item Failed")
                    data_dict = {
                        "id": item.id,
                        "store_id": item.store_id,
                        "item_name": item.item_name,
                        "item_des": item.item_des,
                        "item_portrait": item.item_portrait,
                        "item_type": item.item_type,
                        "item_geohash": item.item_geohash,
                        "item_status": item.item_status,
                        "item_stock": item.item_stock,
                        "original_price": item.original_price,
                        "discount_price": item.discount_price,
                        "create_time": item.create_time.timestamp(),
                        "last_modified_time": item.lastmodified_time.timestamp(),
                    }
                    data_list.append(data_dict)
                return self.getJsonReturn(data={"num": len(ret_list), "list": data_list})
            else:
                return JsonResponse(self.JSON_RETURN_DICT[-2])
        else:
            return JsonResponse(self.JSON_RETURN_DICT[-2])


class ItemTagsView(TokenUserView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        if self.data is None:
            return JsonResponse(self.JSON_RETURN_DICT[-1])
            # 检验json文本外层中是否包含必要的键名
        result, json_ret = self.OuterCheck()
        if request is False:
            return json_ret
        type = self.data["type"]
        subtype = self.data["subtype"]
        data = dict(self.data["data"])
        if type == "tags":
            if subtype == "text":
                if "text_list" in data.keys():
                    text_list = data["text_list"]
                elif "text" in data.keys():
                    text = data["text"]
                    text_list = [text]
                else:
                    return JsonResponse(self.JSON_RETURN_DICT[-3])
                tf = TfIdf(text_list=text_list)
                result = tf.doJob()
                return self.getJsonReturn(data={"num": len(result), "list": result})
            elif subtype == "item":
                if "item_list" not in data.keys():
                    return JsonResponse(self.JSON_RETURN_DICT[-3])
                item_list = data["item_list"]
                text_list = []
                for item_id in item_list:
                    try:
                        item = JpaItems.objects.get(id=item_id)
                    except Exception as e:
                        # status 100 错误的商品id
                        return self.getJsonReturn(status=100, message="Error item id")
                    if item.item_status == -1:
                        continue
                    if item.item_name is None or item.item_name == "":
                        continue
                        # # status 101 Error item name
                        # return self.getJsonReturn(status=101, message="Error item name")
                    text_list.append(item.item_name)
                tf = TfIdf(text_list=text_list)
                ret_list = tf.doJob()
                for ret in ret_list:
                    index = ret_list.index(ret)
                    tags = json.dumps(ret, ensure_ascii=False)
                    try:
                        JpaItems.objects.filter(id=item_list[index]).update(item_tags=tags)
                    except Exception as e:
                        print("item:", item_list[index], "更新失败")
                # status 0 成功处理
                return self.getJsonReturn()

            else:
                return JsonResponse(self.JSON_RETURN_DICT[-2])
        else:
            return JsonResponse(self.JSON_RETURN_DICT[-2])
