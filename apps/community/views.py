from django.shortcuts import render
from django.http.response import JsonResponse
from django.views import View
from apps.community.models import Community
from apps.products.models import JpaItems, JpaStores
from apps.operation.views import TokenUserView

from extra_apps.LatLon.main import CaculateDistance


# Create your views here.

class CommunityView(TokenUserView):
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
        if type == "community":
            if subtype == "publish":
                for key in ["content"]:
                    if key not in data.keys():
                        # status -3
                        return JsonResponse(self.JSON_RETURN_DICT[-3])
                content = data["content"]
                item: JpaItems = None
                if "item_id" in data.keys():
                    item_id = data["item_id"]
                    try:
                        item = JpaItems.objects.get(id=item_id)
                    except Exception as e:
                        return self.getJsonReturn(100, "Error item id")
                latitude: float = None
                longitude: float = None
                if "latitude" in data.keys():
                    latitude = data["latitude"]
                if "longitude" in data.keys():
                    longitude = data["longitude"]
                community = Community()
                community.sender = self.user
                community.content = content
                community.item = item if item is not None else None
                community.latitude = latitude if latitude is not None else None
                community.longitude = longitude if longitude is not None else None
                community.save()
                return self.getJsonReturn(data={"community_id": community.id})
            elif subtype == "list":
                for key in ["latitude", "longitude"]:
                    if key not in data.keys():
                        # status -3
                        return self.JSON_RETURN_DICT[-3]
                latitude = data["latitude"]
                longitude = data["longitude"]
                start = 0
                if "start" in data.keys():
                    start = data["start"]
                limit: int = None
                if "limit" in data.keys():
                    limit = data["limit"]
                distance = 500
                if "distance" in data.keys():
                    distance = data['distance']
                community_list = Community.objects.all().order_by("-add_time")
                temp_list = []
                for community in community_list:
                    lat1 = float(community.latitude)
                    lng1 = float(community.longitude)
                    calc_distance = CaculateDistance.getDistance(lat1=lat1, lng1=lng1, lat2=latitude, lng2=longitude)
                    print("distance:", calc_distance)
                    if calc_distance <= distance:
                        temp_list.append(community)
                if limit is None:
                    limit = len(temp_list)
                temp_list = temp_list[start:start + limit]
                data_list = []
                for community in temp_list:
                    data_json = {
                        "community_id": community.id,
                        "user": {
                            "username": community.sender.username,
                            "nickname": community.sender.nickname
                        },
                        "content": community.content,
                        "item": {
                            "id": community.item.id,
                            "name": community.item.item_name,
                            "simpleDesc": community.item.simple_desc,
                            "listPicUrl": community.item.item_portrait,
                            "retailPrice": float(community.item.original_price) if community.item.original_price is not None else None,
                            "activityPrice": float(
                                community.item.discount_price) if community.item.discount_price is not None else None,
                        } if community.item is not None else None,
                        "add_time": community.add_time.timestamp(),
                        "update_time": community.update_time.timestamp()
                    }
                    data_list.append(data_json)
                return self.getJsonReturn(data={"num": len(data_list), "list": data_list})
            elif subtype == "delete":
                if 'community_id' not in data.keys():
                    # status -3
                    return self.JSON_RETURN_DICT[-3]
                community_id = data['community_id']
                try:
                    community = Community.objects.get(id=community_id)
                except Exception as e:
                    # status 100 错误的community id
                    return self.getJsonReturn(100, "Error community id")
                community.delete()
                # status 0
                return self.getJsonReturn()
            elif subtype == "update":
                if 'community_id' not in data.keys():
                    # status -3
                    return self.JSON_RETURN_DICT[-3]
                community_id = data['community_id']
                try:
                    community = Community.objects.get(id=community_id)
                except Exception as e:
                    # status 100 错误的community id
                    return self.getJsonReturn(100, "Error community id")
                for key in data.keys():
                    if key == "content":
                        content = data["content"]
                        community.content = content
                    elif key == "item_id":
                        item_id = data["item_id"]
                        try:
                            item = JpaItems.objects.get(id=item_id)
                        except Exception as e:
                            return self.getJsonReturn(101, "Error Item id")
                        community.item = item
                community.save()
                return self.getJsonReturn()
            else:
                return JsonResponse(self.JSON_RETURN_DICT[-2])
        else:
            return JsonResponse(self.JSON_RETURN_DICT[-2])


class DistanceView(TokenUserView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
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
        if type == "distance":
            if subtype == "calc":
                for key in ['lat1', 'lng1', 'lat2', 'lng2']:
                    if key not in data.keys():
                        # status -3
                        return JsonResponse(self.JSON_RETURN_DICT[-3])
                try:
                    lat1 = float(data["lat1"])
                    lng1 = float(data["lng1"])
                    lat2 = float(data["lat2"])
                    lng2 = float(data["lng2"])
                except Exception as e:
                    # status 100
                    return self.getJsonReturn(100, "Error location data")
                distance = CaculateDistance.getDistance(lat1, lng1, lat2, lng2)
                return self.getJsonReturn(data={"distance": distance})
            else:
                return JsonResponse(self.JSON_RETURN_DICT[-2])
        else:
            return JsonResponse(self.JSON_RETURN_DICT[-2])
