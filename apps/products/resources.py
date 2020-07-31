from import_export import resources
from apps.products.models import JpaStores, JpaItems


class JpaStoresResource(resources.ModelResource):
    class Meta:
        model = JpaStores


class JpaItemsResource(resources.ModelResource):
    class Meta:
        model = JpaItems
