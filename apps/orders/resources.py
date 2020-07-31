from import_export.resources import ModelResource
from apps.orders.models import JpaOrderform


class JpaOrderformResource(ModelResource):
    class Meta:
        model = JpaOrderform
