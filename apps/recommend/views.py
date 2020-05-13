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
                ret_json = ItemRetJson()
                for recommend in recommend_list:
                    item_id = recommend[0]
                    try:
                        item = JpaItems.objects.get(id=item_id)
                    except Exception as e:
                        print(e)
                        # status 101 获取推荐信息的商品id失败
                        return JsonResponse({"code": "101", "message": "Get recommend data failed"})
                    item_json = ItemDataJson(item_id=item.id, name=item.item_name, pic=item.item_portrait,
                                             simple_desc=item.simple_desc, price=float(
                            item.original_price if item.original_price is not None else None),
                                             sale=float(
                                                 item.discount_price) if item.discount_price is not None else None)
                    ret_json.appendItemJson(item_json)
                return JsonResponse(ret_json.ret_json)
            elif subtype == "index":
                limit: int = None
                if "limit" in data.keys():
                    limit = int(data["limit"])
                recommend = UserIndexRecommend(user=self.user)
                ret_list = recommend.doJob(limit=limit)
                data_list = []
                ret_json = ItemRetJson()
                for item_id in ret_list:
                    try:
                        item = JpaItems.objects.get(id=item_id)
                    except Exception as e:
                        print(e)
                        # status 100 获取商品信息失败
                        return JsonResponse({"code": "100", "message": "Get Item Failed"})
                    item_json = ItemDataJson(item_id=item.id, name=item.item_name, pic=item.item_portrait,
                                             simple_desc=item.simple_desc, price=float(
                            item.original_price if item.original_price is not None else None),
                                             sale=float(
                                                 item.discount_price) if item.discount_price is not None else None)
                    ret_json.appendItemJson(item_json)
                return JsonResponse(ret_json.ret_json)
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


class ItemDataJson:
    data_json = {
        "type": 1,
        "id": 0,
        "categoryItem": {
            "id": 0,
            "listPicUrl": "",
            "simpleDesc": "",
            "simpleDescClose": False,
            "name": "",
            "retailPrice": 0.0,
            "activityPrice": 0.0,
        }
    }

    def __init__(self, item_id: int, name: str, pic: str, simple_desc: str, price: float, sale: float):
        self.data_json["id"] = item_id
        categoryItem = self.data_json["categoryItem"]
        categoryItem["name"] = name
        categoryItem["id"] = item_id
        categoryItem["listPicUrl"] = pic
        categoryItem["simpleDesc"] = simple_desc
        categoryItem["retailPrice"] = price
        categoryItem["activityPrice"] = sale


class ItemRetJson:
    ret_json = {
        "code": "200",
        "data": {
            "rcmdItemList": []
        }
    }

    def appendItemJson(self, item: ItemDataJson):
        self.ret_json["data"]["rcmdItemList"].append(item.data_json)

    def __str__(self):
        return json.dumps(self.ret_json, ensure_ascii=False)
