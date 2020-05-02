from django.shortcuts import render
from django.http.response import JsonResponse

from apps.operation.views import TokenUserView
from apps.recommend.models import JpaItems, JpaItemUserBehavior
from extra_apps.CF.base_item import RelationRecommend

# Create your views here.

class UserItemCfView(TokenUserView):
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
            if subtype == "user":
                for key in ["item_id"]:
                    if key not in data.keys():
                        return self.JSON_RETURN_DICT[-3]
                item_id = str(data["item_id"])
                try:
                    item = JpaItems.objects.get(id=item_id)
                except Exception as e:
                    # status 100 错误的item id
                    return self.getJsonReturn(100, "Error item id")
                recommend = RelationRecommend(user=self.user, item=item)
                recommend_list = recommend.recommend(mode=0)
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
                        "item_id": item.id,
                        "item_name": item.item_name,
                        "item_portrait": item.item_portrait,
                        "item_status": item.item_status,
                        "original_price": item.original_price,
                        "discount_price": item.discount_price,
                    }
                    data_list.append(data_dict)
                return self.getJsonReturn(data={"num": len(data_list), "list": data_list})
            else:
                return self.JSON_RETURN_DICT[-2]
        else:
            return self.JSON_RETURN_DICT[-2]
