from django.urls import path
from . import views
from .views import TwittsList,TwittsDetail,CreateTwitt,UpdateTwitt,DeleteTwitt,UserPostListView,follows,view_flls



urlpatterns = [
    path('', TwittsList.as_view(),name="blog-home"),
    path("massages/",views.messages,name="blog-mesagges"),
    path("post/<int:pk>/", TwittsDetail.as_view(), name="post-detail"),
    path('post/new/', CreateTwitt.as_view(), name='post-create'),
    path('post/<int:pk>/update/', UpdateTwitt.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', DeleteTwitt.as_view(), name='post-delete'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-post'),
    path('follow/<str:username>/', views.follows, name='user-follow'),
    path('view/<str:username>/', views.view_flls, name='view-follow'),
    path('search/', views.search, name='search'),
    path('viewd/<str:username>/', views.view_fllss, name='view-followd')
]