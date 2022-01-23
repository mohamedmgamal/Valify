import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import PollsSerializer,AnswersSerializer,PollsAndCommentsSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import poll,Answers

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getPolls(request):
    list = Answers.objects.filter(user_id=request.user).values_list('poll_id', flat=True)
    polls = poll.objects.all().exclude(id__in=list)
    response = PollsSerializer(instance=polls, many=True)
    return Response(data=response.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def Answer(request):
    serializer = AnswersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['user']=request.user
        serializer.save()
        return Response(data={
            "success": True,
            "message": "Answer added successfully "
        }, status=status.HTTP_201_CREATED)
    return Response(data={
        "success": False,
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search(request,search):
    list = Answers.objects.filter(user_id=request.user).values_list('poll_id', flat=True)
    print(search)
    polls1 = poll.objects.exclude(id__in=list).filter(title__icontains=search)
    polls2 = poll.objects.exclude(id__in=list).filter(description__icontains=search)
    polls3 = poll.objects.exclude(id__in=list).filter(choices__name__icontains=search)
    polls = polls1.union(polls2,polls3)
    response = PollsSerializer(instance=polls, many=True)
    return Response(data=response.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getComments(request):
    polls = poll.objects.all()
    response = PollsAndCommentsSerializer(instance=polls, many=True)
    return Response(data=response.data, status=status.HTTP_200_OK)



