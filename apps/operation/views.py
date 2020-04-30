from django.shortcuts import render
from django.http.response import JsonResponse
from django.views import View
from apps.tokens.models import JpaTokens, Doki2
from apps.users.models import JpaUsers
from typing import Tuple, List, Dict
import json


class TokenUserView(View):
    JSON_RETURN_DICT = {
        -1: {"id": -1, "status": -1, "message": "Error JSON key", "data": {}},
        -2: {"id": -1, "status": -2, "message": "Error JSON value", "data": {}},
        -3: {"id": -1, "status": -3, "message": "Error data key", "data": {}},
        -100: {"id": -1, "status": -100, "message": "Missing necessary args", "data": {}},
        -101: {"id": -1, "status": -101, "message": "Error Token", "data": {}},
    }
    JSON_F1_ERROR_JSON_KEY: dict = {"id": -1, "status": -1, "message": "Error JSON key", "data": {}}
    JSON_F2_ERROR_JSON_VALUE: dict = {"id": -1, "status": -2, "message": "Error JSON value", "data": {}}
    JSON_F3_ERROR_DATA_KEY: dict = {"id": -1, "status": -3, "message": "Error data key", "data": {}}
    JSON_F100_MISSING_NECESSARY_ARGS: dict = {"id": -1, "status": -100, "message": "Missing necessary args", "data": {}}
    JSON_F101_ERROR_TOKEN: dict = {"id": -1, "status": -101, "message": "Error Token", "data": {}}

    data: dict = None
    id: int = None
    token: str = None
    user: JpaUsers = None

    def get(self, request, *args, **kwargs):
        self.NormalTokenCheck()
        self.GetEventID()

    def post(self, request, *args, **kwargs):
        print("=" * 20)
        self.NormalTokenCheck()
        self.NormalDataCheck()
        self.GetEventID()
        print("=" * 20)

    def NormalTokenCheck(self) -> Tuple[bool, JsonResponse]:
        try:
            token = self.request.GET.get("token")
            print("[token]:", token)
        except Exception as e:
            print(e)
            print("[token]:Missing necessary args")
            # log_main.error("Missing necessary agrs")
            # status -100 缺少必要的参数
            return False, JsonResponse(
                {"id": -1, "status": -100, "message": "Missing necessary args", "data": {}})
        result, user = Doki2(token=token)
        print("[user]:", user)
        if result is False:
            # status -101 错误的token
            return False, JsonResponse(self.JSON_RETURN_DICT[-101])
        self.token = token
        self.user = user
        return True, JsonResponse({})

    def NormalDataCheck(self) -> Tuple[bool, JsonResponse]:
        try:
            data = dict(json.loads(self.request.body))
            print("[data]:", data)
        except:
            # status -1 错误的json key Error JSON key
            return False, JsonResponse(self.JSON_RETURN_DICT[-1])
        self.data = data
        return True, JsonResponse({})

    def GetEventID(self) -> int:
        if not isinstance(self.data, dict):
            self.id = -1
        elif "id" in self.data.keys():
            self.id = self.data["id"]
        else:
            self.id = -1
        for key in self.JSON_RETURN_DICT:
            self.JSON_RETURN_DICT[key]["id"] = self.id
        return self.id

    def OuterCheck(self) -> Tuple[bool, JsonResponse]:
        for key in ["type", "subtype", "data"]:
            if key not in self.data.keys():
                # status -1 json的key错误。
                return False, JsonResponse(self.JSON_RETURN_DICT[-1])
        return True, JsonResponse({})

    def getJsonReturn(self, status: int = 0, message: str = "Successful", data: dict = {}) -> JsonResponse:
        return JsonResponse({"id": self.id, "status": status, "message": message, "data": data})
