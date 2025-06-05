"""URL patterns for Teacher Portal."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('add_student/', views.add_student, name='add_student'),
    path('edit_student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('get_subjects/', views.get_subjects, name='get_subjects'),
    path('send_reset_code/', views.send_reset_code, name='send_reset_code'),
    path('verify_reset_code_and_update_password/', views.verify_reset_code_and_update_password, name='verify_reset_code_and_update_password'),
    path('upload_teachers_csv/', views.upload_teachers_csv, name='upload_teachers_csv'),
]
