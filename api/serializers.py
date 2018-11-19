"""Serializers to map the Model instances into JSON format."""
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.serializers import FileField
from rest_framework.serializers import ListField
from rest_framework_recursive.fields import RecursiveField
from iconviewer.models.tag import Tag
from iconviewer.models.group import Group
from iconviewer.models.iconset import IconSet
from iconviewer.models.icon import Icon

class TagSerializer(HyperlinkedModelSerializer):
    """Serializer to map the Tag model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Tag
        fields = ('name', 'url')


class IconSetSerializer(HyperlinkedModelSerializer):
    """Serializer to map part of the IconSet model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = IconSet
        fields = ('uuid', 'name', 'url')
        read_only_fields = ('uuid',)


class GroupSerializer(ModelSerializer):
    """Serializer to map the Group model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Group
        fields = ('uuid', 'name', 'sort', 'groups', 'group')
        read_only_fields = ('uuid',)


class TreeSerializer(ModelSerializer):
    """Serializer to map the Group model instance into JSON format."""
    groups = RecursiveField(required=False, allow_null=True, many=True)
    iconsets = IconSetSerializer(required=False, allow_null=True, many=True)
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Group
        fields = ('uuid', 'name', 'sort', 'groups', 'iconsets')
        read_only_fields = ('uuid',)


class IconSerializer(HyperlinkedModelSerializer):
    """Serializer to map the Icon model instance into JSON format."""
    tags = TagSerializer(required=False, allow_null=True, many=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Icon
        fields = ('uuid', 'name', 'file', 'tags', 'url')
        read_only_fields = ('uuid',)


class IconSetDetailSerializer(HyperlinkedModelSerializer):
    """Serializer to map the IconSet model instance into JSON format."""
    icons = IconSerializer(required=False, allow_null=True, many=True)
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = IconSet
        fields = ('uuid', 'name', 'group', 'icons')
        read_only_fields = ('uuid',)


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
        fields = ('uuid', 'name', 'file', 'tags', 'icon_set')
        read_only_fields = ('uuid',)