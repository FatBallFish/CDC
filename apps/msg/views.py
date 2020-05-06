from django.shortcuts import render
from django.views import View
from apps.operation.views import TokenUserView
from django.http.response import JsonResponse

from apps.tokens.models import JpaUsers, Doki2
from apps.msg.models import Messages, MessageSysStatus, MessageText
from apps.msg.models import getNewSysMessageNum, getSysMessage, getNewPrivateNum, getPrivateMessage, \
    SignPrivateMessageBatch, SignSysMessageBatch, FilterMessage, getPrivateList

import json


# Create your views here.
class MsgView(TokenUserView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        if self.user is None:
            return JsonResponse(self.JSON_RETURN_DICT[-101])
        if self.data is None:
            return JsonResponse(self.JSON_RETURN_DICT[-1])
            # 检验json文本外层中是否包含必要的键名
        result, json_ret = self.OuterCheck()
        if request is False:
            return json_ret

        type = self.data["type"]
        subtype = self.data["subtype"]
        data = dict(self.data["data"])
        if type == "msg":
            if subtype == "has_new":
                private_dict = getNewPrivateNum(user=self.user)
                num_private = private_dict["total"]
                num_sys = getNewSysMessageNum(user=self.user)
                num = num_private + num_sys
                # status 0 成功处理事件
                return self.getJsonReturn(
                    data={"sys": num_sys, "private": num_private, "private_detail": private_dict["detail"]})
            elif subtype == "sys":
                if_new = 0  # 0为新消息，1为旧消息，2为新消息，错误代码默认为新消息
                if "if_new" in data.keys():
                    if_new = data["if_new"]
                    try:
                        if_new = int(if_new)
                        if if_new not in [0, 1, 2]:
                            if_new = 0
                    except Exception as e:
                        if_new = 0
                json_dict = getSysMessage(user=self.user, if_new=if_new, id=self.id)
                print(json_dict)
                return JsonResponse(json_dict)
            elif subtype == "private":
                if_new = 0  # 0为新消息，1为旧消息，2为新消息，错误代码默认为新消息
                people = ""
                start = 0
                limit = -1
                if "if_new" in data.keys():
                    if_new = data["if_new"]
                    try:
                        if_new = int(if_new)
                        if if_new not in [0, 1, 2]:
                            if_new = 0
                    except Exception as e:
                        if_new = 0
                if "people" in data.keys():
                    people = str(data["people"])
                    if "start" in data.keys():
                        start = data["start"]
                        try:
                            start = int(start)
                        except Exception as e:
                            start = 0
                    if "limit" in data.keys():
                        limit = data["limit"]
                        try:
                            limit = int(limit)
                            if limit < 0:
                                limit = -1
                        except Exception as e:
                            limit = -1
                json_dict = getPrivateMessage(user=self.user, if_new=if_new, people=people, start=start, limit=limit,
                                              id=self.id)
                return JsonResponse(json_dict)
            elif subtype == "msg_list":
                json_dict = getPrivateList(user=self.user, id=self.id)
                return JsonResponse(json_dict)
            elif subtype == "send":
                for key in ["receiver", "title", "content"]:
                    if key not in data.keys():
                        # status -3 错误的 data 键
                        return JsonResponse(self.JSON_RETURN_DICT[-3])
                receiver = str(data["receiver"])
                title = str(data["title"])
                content = str(data["content"])
                try:
                    recID = JpaUsers.objects.get(username=receiver)
                except Exception as e:
                    # status 100 错误的接收者
                    return self.getJsonReturn(status=100, message="Error receiver")
                try:
                    msgtext, result = MessageText.objects.get_or_create(title=title, content=content)
                    # if not result:
                    #     # status 101 创建消息内容失败
                    #     return self.getJsonReturn(status=101, message="Create MessageText Failed")
                except Exception as e:
                    # status 101 创建消息内容失败
                    return self.getJsonReturn(status=101, message="Create MessageText Failed")
                msg = Messages()
                msg.sendID = self.user
                msg.recID = recID
                msg.text = msgtext
                msg.type = "private"
                msg.subtype = "default"
                msg.extra = "{}"
                msg.status = False
                msg.save()
                # status 0 成功处理事件
                return self.getJsonReturn(data={"msg_id": msg.id})
            elif subtype == "sign":
                if "msg_id" not in data.keys():
                    # status -3 错误的key
                    return JsonResponse(self.JSON_RETURN_DICT[-3])
                try:
                    msg_id = int(data["msg_id"])
                    message = Messages.objects.get(id=msg_id)
                except Exception as e:
                    # status 100 错误的 msg_id
                    return self.getJsonReturn(status=100, message="Error msg_id")
                admin = JpaUsers.objects.get(username="guosai")
                if message.sendID == admin or message.sendID is None:
                    # 系统消息
                    defaults = {"status": True}
                    MessageSysStatus.objects.update_or_create(defaults=defaults, message=message, recID=self.user)
                else:
                    message.status = True
                    message.save()
                # status 0 成功处理事件
                return self.getJsonReturn()
            elif subtype == "sign_batch":
                sys = 0  # 为0表示不设为已读，1表示设为已读
                private = 0
                people = ""
                status = 0
                message = "Successful"
                if "sys" in data.keys():
                    sys = data["sys"]
                    try:
                        sys = int(sys)
                        if sys not in [0, 1]:
                            sys = 0
                    except Exception as e:
                        sys = 0
                if "private" in data.keys():
                    private = data["private"]
                    try:
                        private = int(private)
                        if private not in [0, 1]:
                            private = 0
                    except Exception as e:
                        private = 0
                    if "people" in data.keys():
                        people = str(data["people"])
                        if not people.isdecimal():
                            people = ""
                if sys == 1 and status == 0:
                    print("进入系统消息批量已读")
                    status, message = SignSysMessageBatch(user=self.user)
                if private == 1 and status == 0:
                    print("进入私聊消息批量已读")
                    status, message = SignPrivateMessageBatch(user=self.user, people=people)
                # status 100,101,0
                return self.getJsonReturn(status=status, message=message)
            elif subtype == "filter":
                if "type" not in data.keys():
                    # status -3 data中有非预料中的key字段
                    return JsonResponse(self.JSON_RETURN_DICT[-3])
                msg_type = str(data["type"])
                msg_subtype = ""
                if "subtype" in data.keys():
                    msg_subtype = str(data["subtype"])
                if_new = 0  # 0为新消息，1为旧消息，2为新消息，错误代码默认为新消息
                if "if_new" in data.keys():
                    try:
                        if_new = int(data["if_new"])
                        if if_new not in [0, 1, 2]:
                            if_new = 0
                    except Exception as e:
                        if_new = 0
                json_dict = FilterMessage(user=self.user, type=msg_type, subtype=msg_subtype, if_new=if_new, id=self.id)
                return JsonResponse(json_dict)

            else:
                # status -2 json的value错误。
                return self.JSON_RETURN_DICT[-2]
        else:
            # status -2 json的value错误。
            return self.JSON_RETURN_DICT[-2]
