from django.shortcuts import render
from django.views import View
from django.http.response import JsonResponse

from apps.operation.views import TokenUserView
import json


# Create your views here.

class LoginTestView(TokenUserView):
    def get(self, request, *args, **kwargs):
        return render(request, "login.html")

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        # json校验，判断是否传递的正确的json数据过来
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
        if type == "login":
            if subtype == "pass":
                for key in ["username", "password"]:
                    if key not in data.keys():
                        # status -3 json的value错误。
                        return JsonResponse(self.JSON_RETURN_DICT[-3])
                username = str(data["username"])
                password = str(data["password"])
                return JsonResponse({"id": self.id, "status": 0, "message": "Successful",
                                     "data": {"username": username, "password": password}})
            else:
                # status -2 json的value错误。
                return JsonResponse(self.JSON_RETURN_DICT[-2])
        else:
            # status -2 json的value错误。
            return JsonResponse(self.JSON_RETURN_DICT[-2])
