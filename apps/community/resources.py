from import_export import resources
from apps.community.models import Community


class CommunityResource(resources.ModelResource):
    class Meta:
        model = Community
