from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('',views.home),
    path('feedback',views.Feedback),
    path('admin/<str:location>/<str:action>/<int:id>',views.Admin ,name ='admin'),
    path('blood', views.blood, name='blood'),
    path('msg', views.msg, name='msgs'),
    path('msg/<int:sender>/<int:receiver>', views.msg_details, name='msg'),
    path('inbox', views.inbox, name='inbox'),
    path('inbox/<int:sender>/<int:receiver>', views.inbox, name='inbox_details'),
    path('notification', views.Notification, name='notification'),
    path('addProfile',views.addProfile),
    path('follow',views.follow),
    path('upost',views.UploadPost),
    path('comment',views.comment,name="comment"),
    path('delComment', views.delComment, name="delComment"),
    path('deleteimg', views.deleteimg, name="deleteimg"),
    path('deleteReportPost',views.deleteReportPost, name="deleteReportPost"),
    path('like',views.like,name='like'),
    path('sathiharu',views.sathiharu,name="sathiharu"),
    path('gallery/<str:post>', views.gallery),
    path('user/<str:id>',views.user),
    path('pswd',auth_views.PasswordChangeView.as_view(template_name='signup.html')),
    path('signup/<str:action>',views.signup,name='signup'),
    path('friends/<str:action>/<int:id>',views.followers),
    path('rental/<str:rentalid>', views.rental),    
    
]
