from .models import Note, Share
from rest_framework import serializers
from django.utils import timezone
from myuser.serializer import MyUserSerializer
from myuser.models import MyUser


class NoteSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=False, default=serializers.CurrentUserDefault(), queryset=MyUser.objects.all())

    class Meta:
        model = Note
        fields = ('id', 'title', 'content', 'author', 'created_on', 'updated_on',)

    def update(self, instance, validated_data):
        instance.updated_on = timezone.now()
        return super().update(instance, validated_data)


class ShareSerializer(serializers.ModelSerializer):
    shared_by = MyUserSerializer(many=False)
    shared_with = MyUserSerializer(many=False)
    note = NoteSerializer(many=False)

    class Meta:
        model = Share
        fields = ('id', 'shared_by', 'shared_with', 'note', 'created_on',)
