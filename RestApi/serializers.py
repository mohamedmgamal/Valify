import datetime
from rest_framework import serializers
from RestApi import models
from RestApi.models import DiscussionThread,Answers,Choices,poll


class ChoicesSerializer(serializers.ModelSerializer):
    number_of_Votes=serializers.SerializerMethodField("count")
    def count(self,obj):
        return Answers.objects.filter(choice_id__exact=obj.id).count()
    class Meta:
        model = Choices
        fields = "__all__"

class PollsSerializer(serializers.ModelSerializer):
    choices = ChoicesSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        status="Available"
        if obj.expiry_date.replace(tzinfo=None) < datetime.datetime.now():
            status="Expired"
        return status
    class Meta:
        model = poll
        fields = ['id','title', 'description','created_at','expiry_date', 'choices','status']

class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields=("poll","choice")

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscussionThread
        fields = "__all__"

class PollsAndCommentsSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        status="Available"
        if obj.expiry_date.replace(tzinfo=None) < datetime.datetime.now():
            status="Expired"
        return status
    class Meta:
        model = poll
        fields = ['id','title', 'description','created_at','expiry_date', 'comments','status']