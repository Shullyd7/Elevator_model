"""
URL configuration for elevator_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from elevators.views import ElevatorViewSet



router = DefaultRouter()
router.register(r'elevators', ElevatorViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('elevators/<int:pk>/requests/', ElevatorViewSet.as_view({'get': 'get_requests', 'post': 'save_user_request'}), name='elevator-requests'),
    path('num_elevators/', ElevatorViewSet.as_view({'get': 'get_num_elevators'}), name='num-elevators'),
    path('clear_elevators/', ElevatorViewSet.as_view({'post': 'clear_elevators'}), name='clear-elevators'),
    path('elevators/<int:pk>/destination/', ElevatorViewSet.as_view({'get': 'get_next_destination_floor'}), name='elevator-destination'),
    path('elevators/<int:pk>/is_moving/', ElevatorViewSet.as_view({'get': 'is_moving_up_down'}), name='elevator-moving-status'),
    path('elevators/<int:pk>/maintenance/', ElevatorViewSet.as_view({'put': 'mark_maintenance'}), name='elevator-maintenance'),
    path('elevators/<int:pk>/door/open/', ElevatorViewSet.as_view({'put': 'open_door'}), name='elevator-door-open'),
    path('elevators/<int:pk>/door/close/', ElevatorViewSet.as_view({'put': 'close_door'}), name='elevator-door-close'),
    path('elevators/<int:pk>/requests/clear/', ElevatorViewSet.as_view({'post': 'clear_user_requests'}), name='elevator-requests-clear'),
]


