from django.urls import path

from . import views

app_name = 'staff'

urlpatterns = [
    path('staffs', views.StaffsListAPIView.as_view(), name='staffs_list'),
#    path('staffs/<str:title>', views.StaffsByTitleListAPIView.as_view(), name='staffs_by_title_list'),
]
