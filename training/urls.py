from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Module related URLs
    path('modules/', views.module_list, name='module_list'),
    path('modules/create/', views.module_create, name='module_create'),
    path('modules/<int:pk>/', views.module_detail, name='module_detail'),
    path('modules/<int:pk>/edit/', views.module_edit, name='module_edit'),
    
    # Enrollment related URLs
    path('enroll/<int:module_id>/', views.enroll, name='enroll'),
    path('unenroll/<int:module_id>/', views.unenroll, name='unenroll'),
    
    # Resource related URLs
    path('modules/<int:module_id>/resources/', views.resource_list, name='resource_list'),
    path('modules/<int:module_id>/resources/upload/', views.resource_upload, name='resource_upload'),
    
    # Forum related URLs
    path('modules/<int:module_id>/forum/', views.forum_list, name='forum_list'),
    path('modules/<int:module_id>/forum/create/', views.forum_post_create, name='forum_post_create'),
    path('modules/<int:module_id>/forum/<int:post_id>/', views.forum_post_detail, name='forum_post_detail'),
    path('modules/<int:module_id>/forum/<int:post_id>/edit/', views.forum_post_edit, name='forum_post_edit'),
    
    # Progress related URLs
    path('progress/', views.progress_list, name='progress_list'),
    path('progress/<int:resource_id>/complete/', views.mark_resource_complete, name='mark_resource_complete'),
    
    # Certificate related URLs
    path('certificates/', views.certificate_list, name='certificate_list'),
    path('certificates/<int:enrollment_id>/generate/', views.generate_certificate, name='generate_certificate'),
] 