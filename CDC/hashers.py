from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.translation import gettext_noop as _
from django.utils.crypto import (
    constant_time_compare, get_random_string, pbkdf2,
)
from django.contrib.auth.hashers import mask_hash
import hashlib


class MyMD5PasswordHasher(BasePasswordHasher):
    algorithm = "myMD5"

    def encode(self, password, salt):
        assert password is not None
        assert salt and '$' not in salt
        hash = hashlib.md5((password + salt).encode()).hexdigest()
        return "%s$%s" % (salt, hash)

    def verify(self, password, encoded):
        salt, hash = encoded.split('$', 1)
        encoded_2 = self.encode(password, salt)
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        algorithm, salt, hash = encoded.split('$', 2)
        assert algorithm == self.algorithm
        return {
            _('algorithm'): algorithm,
            _('salt'): mask_hash(salt, show=2),
            _('hash'): mask_hash(hash),
        }

    def harden_runtime(self, password, encoded):
        pass
