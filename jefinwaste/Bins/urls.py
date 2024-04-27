
from django.urls import path 
from . import views
from .views import CustomLogoutView

urlpatterns = [
    path('',views.login_page,name='login_page'),
    path('register',views.register_page,name='register_page'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('home',views.home_page,name='home_page'),
    path('get-bin-contents/', views.get_bin_contents, name='get_bin_contents'),
    path('update-bin-content/<int:bin_id>/', views.update_bin_content, name='update_bin_content'),
    path('showbin/', views.showbin, name='showbin'),
    path('addbin/', views.addbin, name='addbin'),
    path('calculate/', views.calculate, name='calculate'),
    path('deletebin/', views.deletebin, name='deletebin'),
    path('confirmdelete/<int:bin_id>/',views.deleteconfirm, name='delete_bin' )
]
