from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'analog-devices', views.AnalogDeviceViewSet)
router.register(r'digital-devices', views.DigitalDeviceViewSet)
router.register(r'smart-devices', views.SmartDeviceViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'analog-values', views.AnalogValuesViewSet)
router.register(r'digital-values', views.DigitalValuesViewSet)
router.register(r'smart-values', views.SmartValuesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('analog-devices/<int:pk>/activate/', views.AnalogDeviceViewSet.as_view({'patch': 'activate'}),
         name='analog-device-activate'),
    path('digital-devices/<int:pk>/activate/', views.DigitalDeviceViewSet.as_view({'patch': 'activate'}),
         name='digital-device-activate'),
    path('smart-devices/<int:pk>/activate/', views.SmartDeviceViewSet.as_view({'patch': 'activate'}),
         name='smart-device-activate'),

]
