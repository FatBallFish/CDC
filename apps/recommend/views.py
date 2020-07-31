from django.shortcuts import render
from django.http.response import JsonResponse

from apps.operation.views import TokenUserView
from apps.products.models import JpaItems
from extra_apps.CF.base_item import UserItemRecommend, UserIndexRecommend
from extra_apps.tags.main import TfIdf
from extra_apps.m_cos import py_cos_main as COS
from extra_apps.m_arcface import main as Arcface
from extra_apps.m_facemask import main as FaceMask

from CDC import settings

import json

COS.Initialize(settings.BASE_DIR)
Arcface.Initialize(False)
FaceMask.Initialize(settings.BASE_DIR)


# Create your views here.

class RecommendView(TokenUserView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        if self.user is None:
            return JsonResponse({"code": "-101", "message": "Error token"})
        if self.data is None:
            # status -1 json的key错误
            return JsonResponse({"code": "-1", "message": "Error JSON key"})
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
                    return JsonResponse({"code": "100", "message": "Error item id"})
                recommend = UserItemRecommend(user=self.user, item=item)
                recommend_list = recommend.doJob(mode=1)
                ret_json = {
                    "code": "200",
                    "data": {
                        "rcmdItemList": []
                    }
                }
                for recommend in recommend_list:
                    item_id = recommend[0]
                    try:
                        item = JpaItems.objects.get(id=item_id)
                    except Exception as e:
                        print(e)
                        # status 101 获取推荐信息的商品id失败
                        return JsonResponse({"code": "101", "message": "Get recommend data failed"})
                    data_json = {
                        "type": 1,
                        "id": item.id,
                        "categoryItem": {
                            "id": item.id,
                            "listPicUrl": item.item_portrait,
                            "simpleDesc": item.simple_desc,
                            "simpleDescClose": False,
                            "name": item.item_name,
                            "retailPrice": float(
                                item.original_price) if item.original_price is not None else None,
                            "activityPrice": float(
                                item.discount_price) if item.discount_price is not None else None,
                        }
                    }
                    ret_json["data"]["rcmdItemList"].append(data_json)
                return JsonResponse(ret_json)
            elif subtype == "index":
                limit: int = None
                if "limit" in data.keys():
                    limit = int(data["limit"])
                recommend = UserIndexRecommend(user=self.user)
                ret_list = recommend.doJob(limit=limit)
                data_list = []
                ret_json = {
                    "code": "200",
                    "data": {
                        "rcmdItemList": []
                    }
                }
                for item_id in ret_list:
                    try:
                        item = JpaItems.objects.get(id=item_id)
                    except Exception as e:
                        print(e)
                        # status 100 获取商品信息失败
                        return JsonResponse({"code": "100", "message": "Get Item Failed"})
                    data_json = {
                        "type": 1,
                        "id": item.id,
                        "categoryItem": {
                            "id": item.id,
                            "listPicUrl": item.item_portrait,
                            "simpleDesc": item.simple_desc,
                            "simpleDescClose": False,
                            "name": item.item_name,
                            "retailPrice": float(
                                item.original_price) if item.original_price is not None else None,
                            "activityPrice": float(
                                item.discount_price) if item.discount_price is not None else None,
                        }
                    }
                    ret_json["data"]["rcmdItemList"].append(data_json)
                print("index_json:", ret_json)
                return JsonResponse(ret_json)
            else:
                return JsonResponse({"code": "-2", "message": "Error JSON value"})
        else:
            return JsonResponse({"code": "-2", "message": "Error JSON value"})


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
