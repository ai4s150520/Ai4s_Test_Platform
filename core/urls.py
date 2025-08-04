# core/urls.py

from django.urls import path
from . import views

# This is crucial for using names like 'core:home' in your templates
app_name = 'core'

urlpatterns = [
    # --- Main Page and Dashboard URLS ---
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tests/', views.test_list, name='test_list'),
    path('tests/<int:test_id>/', views.test_detail, name='test_detail'),
    path('tests/<int:test_id>/take/', views.take_test, name='take_test'),
    path('tests/<int:test_id>/submit/', views.submit_test, name='submit_test'),
    path('results/<int:attempt_id>/', views.results, name='results'), 
    path('create-test/', views.create_test, name='create_test'),
    path('manage-test/<int:test_id>/', views.manage_test, name='manage_test'),
    path('manage-test/<int:test_id>/add-question/', views.add_question, name='add_question'),
    path('question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('test/<int:test_id>/delete/', views.delete_test, name='delete_test'),
    path('test/<int:test_id>/toggle-status/', views.toggle_test_status, name='toggle_test_status'),
    path('manage-test/<int:test_id>/bulk-add/', views.bulk_add_questions, name='bulk_add_questions'),
]