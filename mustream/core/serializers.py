from rest_framework import serializers

from django.contrib.auth.models import User

from mustream.core.models import MuUser, Collection, Track# continue



class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all()) # change Snippet and snippets to something else
    # in the example Snippets has a reverse relationship (multiple snippets can belong to one User (Fiorenkey)) we need to add a explicit field for it

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets'] # not snippets


class CollectionSerializer(serializers.ModelSerializer):
    # this can be create/mod by create() and update() methods
    class Meta:
        model = Collection
        fields = ['id', 'title']
