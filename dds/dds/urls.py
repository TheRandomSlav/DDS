"""
URL configuration for dds project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='main_page'),
    path('<int:pk>/delete/', RecordDeleteView.as_view(), name='delete_record'),
    path('create/', create_record, name='create_record'),
    path('<int:pk>/edit/', EditRecordView.as_view(), name='edit_record'),
    path('ajax/load-categories/', ajax_load_categories, name='ajax_load_categories'),
    path('admin-panel/', admin_panel, name='admin_panel'),
    path('edit-object/<str:object_type>/<int:object_id>/', edit_object, name='edit_object'),
    path('create-object/<str:object_type>/', create_object, name='create_object'),
    path('delete-object/<str:object_type>/<int:object_id>/', delete_object, name='delete_object'),
]
