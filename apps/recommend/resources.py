from import_export import resources
from apps.recommend.models import JpaItems, JpaItemUserBehavior, JpaStores


class JpaStoresResource(resources.ModelResource):
    class Meta:
        model = JpaStores


class JpaItemsResource(resources.ModelResource):
    class Meta:
        model = JpaItems


class JpaItemUserBehaviorResource(resources.ModelResource):
    class Meta:
        model = JpaItemUserBehavior
