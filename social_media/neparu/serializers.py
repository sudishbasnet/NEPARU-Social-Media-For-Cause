from rest_framework import serializers
from neparu import models

class Inbox(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=models.User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=models.User.objects.all())

    class Meta:
        model = models.Inbox
        fields = ['sender', 'receiver', 'message', 'created_at']

class Notification(serializers.ModelSerializer):
    post = serializers.SlugRelatedField(many=False, slug_field='id', queryset=models.Post.objects.all())
    rental = serializers.SlugRelatedField(many=False, slug_field='id', queryset=models.Rental.objects.all())
    actor = serializers.SlugRelatedField(many=False, slug_field='username', queryset=models.User.objects.all())
    class Meta:
        model = models.Notification
        fields = ['actor', 'content', 'post','created_at','action','actor_id','blood_group','id','description','location','rental']

