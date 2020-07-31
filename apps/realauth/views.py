from django.shortcuts import render
from django.http import JsonResponse
from CDC import settings

from apps.operation.views import TokenUserView
from apps.tokens.models import Doki2
from apps.realauth.models import RealAuth
from apps.users.models import JpaUsers

from datetime import datetime
import time
import json


# Create your views here.
class RealAuthView(TokenUserView):
    def post(self, request, *args, **kwargs):
        super(RealAuthView, self).post(request, *args, **kwargs)
        if self.user is None:
            return JsonResponse(self.JSON_RETURN_DICT[-101])
        if self.data is None:
            return JsonResponse(self.JSON_RETURN_DICT[-1])
        result, json_ret = self.OuterCheck()
        if not result:
            return json_ret
        type = self.data["type"]
        subtype = self.data["subtype"]
        ## -------正式处理事务-------
        data = dict(self.data["data"])
        if type == "realauth":  ## 用户信息api
            if subtype == "create":
                real_info = {
                    'id_type': "sfz",
                    'id': "",
                    'name': "",
                    'gender': "",
                    'nation': None,
                    'birthday': None,
                    'address': None,
                    'organization': None,
                    'date_start': None,
                    'date_end': None
                }
                for key in ['id_type', 'id', 'name', 'gender', 'birthday']:
                    if key not in data.keys():
                        # status -3 Error data key data数据中必需key缺失 / data中有非预料中的key字段
                        return JsonResponse(self.JSON_RETURN_DICT[-3])
                    elif key == "id_type":
                        if data[key] == "sfz":
                            real_info[key] = data[key]
                        else:
                            # status 200 Error id_type
                            return self.getJsonReturn(200, "Error id_type")
                    elif key == "id":
                        real_info[key] = str(data[key])
                    elif key == "name":
                        real_info[key] = str(data[key])
                    elif key == "gender":
                        if data[key] not in ["male", "female"]:
                            # status 201 Error gender
                            return self.getJsonReturn(201, "Error gender")
                        real_info[key] = data[key]
                    elif key == "birthday":
                        try:
                            timestamp = float(data[key])
                        except Exception as e:
                            # status 202
                            return self.getJsonReturn(202, "Error birthday")
                        time_str = time.strftime("%Y-%m-%d", time.localtime(timestamp))
                        real_info[key] = datetime.strptime(time_str, "%Y-%m-%d").date()
                if "nation" in data.keys():
                    real_info["nation"] = str(data["nation"])
                if "address" in data.keys():
                    real_info["address"] = str(data["address"])
                if "organization" in data.keys():
                    real_info["organization"] = str(data["organization"])
                if "date_start" in data.keys():
                    try:
                        timestamp = float(data["date_start"])
                    except Exception as e:
                        # status 203 错误的开始日期
                        return self.getJsonReturn(203, "Error data_start")
                    time_str = time.strftime("%Y-%m-%d", time.localtime(timestamp))
                    real_info["date_start"] = datetime.strptime(time_str, "%Y-%m-%d").date()
                if "date_end" in data.keys():
                    try:
                        timestamp = float(data["date_end"])
                    except Exception as e:
                        # status 204 错误的结束日期
                        return self.getJsonReturn(204, "Error data_end")
                    time_str = time.strftime("%Y-%m-%d", time.localtime(timestamp))
                    real_info["date_end"] = datetime.strptime(time_str, "%Y-%m-%d").date()
                try:
                    real_auth = RealAuth()
                    real_auth.id_type = real_info["id_type"]
                    real_auth.ID = real_info["id"]
                    real_auth.name = real_info["name"]
                    real_auth.gender = real_info["gender"]
                    real_auth.nation = real_info["nation"]
                    real_auth.birthday = real_info["birthday"]
                    real_auth.address = real_info["address"]
                    real_auth.organization = real_info["organization"]
                    real_auth.date_start = real_info["date_start"]
                    real_auth.date_end = real_info["date_end"]
                    real_auth.save()
                    self.user.real_auth = real_auth
                    self.user.save()
                except Exception as e:
                    # status 100 创建实名认证失败
                    return self.getJsonReturn(100, "Create RealAuth failed")
                # status 0 成功处理事件
                return self.getJsonReturn(data={"real_auth_id": real_auth.ID})
            elif subtype == "update":
                real_auth = self.user.real_auth
                if not real_auth:
                    # status 100 实名未认证
                    return self.getJsonReturn(100, "RealAuth not certified")
                real_info = {
                    'nation': self.user.real_auth.nation,
                    'address': self.user.real_auth.address,
                    'organization': self.user.real_auth.organization,
                    'date_start': self.user.real_auth.date_start,
                    'date_end': self.user.real_auth.date_end
                }
                for key in data.keys():
                    if key not in ['nation', 'address', 'organization', 'date_start', "date_end"]:
                        # status -3 Error data key data数据中必需key缺失 / data中有非预料中的key字段
                        return self.getJsonReturn(-3, "Error data key")
                    elif key in ["date_start", "date_end"]:
                        try:
                            timestamp = float(data[key])
                        except Exception as e:
                            # status 200 错误的date信息
                            return self.getJsonReturn(200, "Error {}".format(key))
                        time_str = time.strftime("%Y-%m-%d", time.localtime(timestamp))
                        real_info[key] = datetime.strptime(time_str, "%Y-%m-%d").date()
                    else:
                        real_info[key] = str(data[key])
                real_auth.nation = real_info["nation"]
                real_auth.address = real_info["address"]
                real_auth.organization = real_info["organization"]
                real_auth.date_start = real_info["date_start"]
                real_auth.date_end = real_info["date_end"]
                real_auth.save()
                return self.getJsonReturn()
            elif subtype == "get":
                real_auth = self.user.real_auth
                if not real_auth:
                    # status 100 实名未认证
                    return self.getJsonReturn(100, "RealAuth not certified")
                data_dict = {
                    "id_type": real_auth.id_type,
                    "id": real_auth.ID,
                    "name": real_auth.name,
                    "gender": real_auth.gender,
                    "nation": real_auth.nation,
                    "birthday": time.mktime(real_auth.birthday.timetuple()),
                    "address": real_auth.address,
                    "organization": real_auth.organization,
                    "date_start": time.mktime(real_auth.date_start.timetuple()),
                    "date_end": time.mktime(real_auth.date_end.timetuple())
                }
                return self.getJsonReturn(data=data_dict)
            else:
                # status -2 json的value错误。
                return JsonResponse(self.JSON_RETURN_DICT[-2])
        else:
            # status -2 json的value错误。
            return JsonResponse(self.JSON_RETURN_DICT[-2])


class RealAuthCheckView(TokenUserView):
    def post(self, request, *args, **kwargs):
        super(RealAuthCheckView, self).post(request, *args, **kwargs)
        if self.data is None:
            return JsonResponse(self.JSON_RETURN_DICT[-1])
        type = self.data["type"]
        subtype = self.data["subtype"]
        data = dict(self.data["data"])
        if type == "realauth":
            if subtype == "check":
                if 'username' not in data.keys():
                    # status -3
                    return JsonResponse(self.JSON_RETURN_DICT[-3])
                username = data["username"]
                try:
                    user = JpaUsers.objects.get(username=username)
                except Exception as e:
                    return self.getJsonReturn(100, "Error username")
                if user.real_auth is not None:
                    return self.getJsonReturn(data={"result": True})
                else:
                    return self.getJsonReturn(data={"result": False})
            else:
                return JsonResponse(self.JSON_RETURN_DICT-2)
        else:
            return JsonResponse(self.JSON_RETURN_DICT - 2)