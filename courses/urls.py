from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.create_courses),
    path('courses/<int:course_id>/', views.course_detail),
    path('selection/', views.selected_courses),
    path('selection/<int:selection_id>/', views.selection_detail),
    # path('selections/', views.get_selections),
    path('access courses/',views.payment)
]