from django.urls import path
from . import views

app_name = "AgroRx"

urlpatterns = [
    path("report/", views.report_issue, name="report_issue"),
    
    
    path('issues/', views.issue_list, name='issue_list'),
    path('issues/<int:pk>/', views.issue_detail, name='issue_detail'),
    path("issue/<int:pk>/pdf_view/", views.issue_pdf_view, name="issue_pdf_view"), 
    
    
    path('my-issues/', views.my_issues, name='my_issues'),
    path('my-issues/<int:pk>/', views.my_issue_detail, name='my_issue_detail'),
    
]
