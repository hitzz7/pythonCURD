


from django.urls import path,include
from. import views



urlpatterns = [
    
    
    path('event-list/', views.eventlist, name="event-list"),
    path('event-detail/<str:pk>/', views.eventdetail, name="event-detail"),
    path('event-create/', views.eventcreate, name="event-create"),
    path('event-update/<str:pk>/', views.eventupdate, name="event-update"),
    path('event-delete/<str:pk>/', views.eventdelete, name="event-delete"),
    
]