"""Serializers to map the Model instances into JSON format."""
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.serializers import FileField
from rest_framework.serializers import ListField
from rest_framework_recursive.fields import RecursiveField
from iconmason.models.tag import Tag
from iconmason.models.group import Group
from iconmason.models.iconset import IconSet
from iconmason.models.icon import Icon

class TagSerializer(HyperlinkedModelSerializer):
    """Serializer to map the Tag model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Tag
        fields = ('name', 'id')


class IconSetSerializer(HyperlinkedModelSerializer):
    """Serializer to map part of the IconSet model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = IconSet
        fields = ('uuid', 'name')
        read_only_fields = ('uuid',)


class GroupSerializer(ModelSerializer):
    """Serializer to map the Group model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Group
        fields = ('uuid', 'name', 'sort', 'groups', 'group', 'iconsets')
        read_only_fields = ('uuid',)


class IconSerializer(HyperlinkedModelSerializer):
    """Serializer to map the Icon model instance into JSON format."""
    tags = TagSerializer(required=False, allow_null=True, many=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Icon
        fields = ('uuid', 'name', 'file', 'tags', 'url', 'svg_data')
        read_only_fields = ('uuid', 'svg_data')


class IconSetReverseSerializer(HyperlinkedModelSerializer):
    """Serializer to map the IconSet model instance into JSON format."""
    group = RecursiveField(required=False, allow_null=True, many=False)
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = IconSet
        fields = ('uuid', 'name', 'group')
        read_only_fields = ('uuid',)


class TagDetailSerializer(ModelSerializer):
    """Serializer to map the Tag model instance into JSON format."""
    icons = IconSerializer(required=False, allow_null=True, many=True)
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Tag
        fields = ('name', 'id', 'icons')


class IconDetailSerializer(HyperlinkedModelSerializer):
    """Serializer to map the Icon model instance into JSON format."""
    tags = TagSerializer(required=False, allow_null=True, many=True)
    icon_set = IconSetReverseSerializer(
        required=False, allow_null=True, many=False)
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Icon
        fields = ('uuid', 'name', 'file', 'svg_source', 'tags', 'icon_set')
        read_only_fields = ('uuid', 'svg_source')
