from rest_framework import serializers

from .models import Paper, Author


# TODO: 删除mysql里的数据的同时也要删除redis里的


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'created')
        read_only_fields = ('created', 'id',)


class PaperSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    class Meta:
        model = Paper
        fields = ('id', 'title','url', 'created','authors','cit_paper')
        read_only_fields = ('created', 'id')

