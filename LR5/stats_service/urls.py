from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'stats'

urlpatterns = [
    path('question/<int:question_id>/', views.QuestionStatsAPI.as_view(), name='question_stats'),
    path('global/', views.GlobalStatsAPI.as_view(), name='global_stats'),
    path('chart/<int:question_id>/', views.ChartAPI.as_view(), name='chart'),
    path('chart/base64/<int:question_id>/', views.ChartBase64API.as_view(), name='chart_base64'),
    path('dashboard/', TemplateView.as_view(template_name='stats/dashboard.html'), name='dashboard'),
]