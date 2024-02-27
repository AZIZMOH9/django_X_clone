from django.urls import path
from . import views


urlpatterns = [
    path('', views.ChatsList.as_view(),name="chat-home"),
    path('view/<int:pk>', views.MessagesList.as_view(),name="chat-view"),
    path('send/<int:pk>', views.SendMessage.as_view(),name="send-message"),
    path('start/<str:username>', views.Start_conv,name="start-conv"),
    
]