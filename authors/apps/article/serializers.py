'''Serializers allow complex data
such as querysets and model instances
 to be converted to
native Python datatypes that can then
be easily rendered into JSON, XML or other content types.'''

from rest_framework import serializers
from django.apps import apps
from .models import RateArticle
from authors.apps.profiles.serializers import ProfileListSerializer


TABLE = apps.get_model('article', 'Article')
Profile = apps.get_model('profiles', 'UserProfile')

NAMESPACE = 'article'
fields = ('id', 'slug', 'image', 'title', 'description', 'body', 'user',)


class ArticleSerializer(serializers.ModelSerializer):
    update_url = serializers.HyperlinkedIdentityField(
        view_name=NAMESPACE + ':update', lookup_field='slug')
    delete_url = serializers.HyperlinkedIdentityField(
        view_name=NAMESPACE + ':delete', lookup_field='slug')
    author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TABLE

        fields = fields + ('author', 'update_url', 'delete_url')

    def get_author(self, obj):
        try:
            serializer = ProfileListSerializer(
                instance=Profile.objects.get(user=obj.user)
            )
            return serializer.data
        except BaseException:
            return {}

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.body = validated_data.get('body', instance.body)
        if validated_data.get('image'):
            instance.image = validated_data.get('image', instance.image)

        instance.save()

        return instance


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TABLE

        fields = fields

    def create(self, validated_data):
        instance = TABLE.objects.create(**validated_data)
        validated_data['slug'] = instance.slug

        return validated_data


class RateArticleSerializer(serializers.ModelSerializer):
    """
    validate rate article
    """
    slug = serializers.SlugField()
    rate = serializers.IntegerField()

    def validate(self, data):
        rate = data['rate']
        if not rate > 0 or not rate <= 5:
            raise serializers.ValidationError(
                'invalid rate value should be > 0 or <=5')

        return data

    class Meta:
        model = RateArticle
        fields = ("slug", "rate")
