from django.contrib.auth.decorators import login_required
from django.urls import path
from . import  views

from . import  views

urlpatterns = [
    path('',views.getPolls,name="get_polls_end_point"),
    path('answer/', views.Answer, name="answer_polls_end_point"),
    path('search/<str:search>', views.search, name="search_polls_end_point"),
    path('discussionThread/', views.getComments, name="comments_polls_end_point"),
]
