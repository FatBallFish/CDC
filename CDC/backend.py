from django.contrib.auth.backends import BaseBackend,UserModel

from apps.users.models import JpaUsers
from extra_apps import MD5


class MyBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None) -> JpaUsers:
        try:
            user = JpaUsers.objects.get(username=username)
        except Exception as e:
            return None
        check_pass = user.password
        salt, check_pass = check_pass.split("$", 1)
        md5_pass = MD5.md5(password, salt)
        if check_pass == md5_pass:
            return user

    def get_user(self, user_id):
        try:
            return JpaUsers.objects.get(username=user_id)
        except Exception as e:
            return None
