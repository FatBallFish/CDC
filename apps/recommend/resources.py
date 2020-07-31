from import_export import resources
from apps.recommend.models import JpaItemUserBehavior


class JpaItemUserBehaviorResource(resources.ModelResource):
    class Meta:
        model = JpaItemUserBehavior
