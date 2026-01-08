from django.urls import path
from . import views

app_name = 'export'

urlpatterns = [
    path('question/<int:question_id>/csv/', views.ExportCSVAPI.as_view(), name='export_csv'),
    path('question/<int:question_id>/json/', views.ExportJSONAPI.as_view(), name='export_json'),
    path('all/json/', views.ExportAllJSONAPI.as_view(), name='export_all_json'),
    path('all/csv/', views.ExportAllCSVAPI.as_view(), name='export_all_csv'),
]