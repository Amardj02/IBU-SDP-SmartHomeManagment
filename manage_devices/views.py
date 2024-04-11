from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from .models import Room, AnalogDevice, SmartDevice, DigitalDevice, SmartValues, DigitalValues, AnalogValues
from .permissions import IsAdminUserOrReadOnly, IsOwnerOfDeviceInRoom
from .serializers import (RoomSerializer, AnalogDeviceSerializer, DigitalDeviceSerializer, SmartDeviceSerializer,
                          AnalogValuesSerializer, DigitalValuesSerializer, SmartValuesSerializer,
                          RoomCreationSerializer)
from rest_framework.response import Response


class AnalogDeviceViewSet(viewsets.ModelViewSet):
    queryset = AnalogDevice.objects.all()
    serializer_class = AnalogDeviceSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOfDeviceInRoom]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return AnalogDevice.objects.all()

        return AnalogDevice.objects.filter(room__owner=user)

    def perform_create(self, serializer):
        user = self.request.user
        room = serializer.validated_data['room']

        if user.is_staff or user == room.owner:
            serializer.save()
        else:
            raise PermissionDenied("You cannot create a device in a room you don't own or you are not an admin.")

    def perform_update(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("You are not allowed to change the room of the device.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_staff:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.user == instance.room.owner:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("You are not authorized to delete this device.", status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['patch'])
    def activate(self, request, pk=None):
        """
        Activate or deactivate an AnalogDevice.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Set the 'active' field based on the value in the request data
        # If 'active' is present in the request data, set it; otherwise, toggle the current state
        if 'active' in serializer.validated_data:
            instance.active = serializer.validated_data['active']
        else:
            instance.active = not instance.active

        instance.save()

        return Response({'status': 'success', 'active': instance.active}, status=status.HTTP_200_OK)


class DigitalDeviceViewSet(viewsets.ModelViewSet):
    queryset = DigitalDevice.objects.all()
    serializer_class = DigitalDeviceSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOfDeviceInRoom]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return DigitalDevice.objects.all()

        return DigitalDevice.objects.filter(room__owner=user)

    def perform_create(self, serializer):
        user = self.request.user
        room = serializer.validated_data['room']

        if user.is_staff or user == room.owner:
            serializer.save()
        else:
            raise PermissionDenied("You cannot create a device in a room you don't own or you are not an admin.")

    def perform_update(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("You are not allowed to change the room of the device.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_staff:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.user == instance.room.owner:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("You are not authorized to delete this device.", status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['patch'])
    def activate(self, request, pk=None):
        """
        Activate or deactivate an AnalogDevice.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Set the 'active' field based on the value in the request data
        # If 'active' is present in the request data, set it; otherwise, toggle the current state
        if 'active' in serializer.validated_data:
            instance.active = serializer.validated_data['active']
        else:
            instance.active = not instance.active

        instance.save()

        return Response({'status': 'success', 'active': instance.active}, status=status.HTTP_200_OK)


class SmartDeviceViewSet(viewsets.ModelViewSet):
    queryset = SmartDevice.objects.all()
    serializer_class = SmartDeviceSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOfDeviceInRoom]

    def get_queryset(self):
        user = self.request.user

        # If the user is an admin, show all smart devices
        if user.is_staff:
            return SmartDevice.objects.all()

        # If the user is not an admin, show only smart devices in their room
        return SmartDevice.objects.filter(room__owner=user)

    def perform_create(self, serializer):
        user = self.request.user
        room = serializer.validated_data['room']

        if user.is_staff or user == room.owner:
            serializer.save()
        else:
            raise PermissionDenied("You cannot create a device in a room you don't own or you are not an admin.")

    def perform_update(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("You are not allowed to change the room of the device.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_staff:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.user == instance.room.owner:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("You are not authorized to delete this device.", status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['patch'])
    def activate(self, request, pk=None):
        """
        Activate or deactivate an AnalogDevice.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Set the 'active' field based on the value in the request data
        # If 'active' is present in the request data, set it; otherwise, toggle the current state
        if 'active' in serializer.validated_data:
            instance.active = serializer.validated_data['active']
        else:
            instance.active = not instance.active

        instance.save()

        return Response({'status': 'success', 'active': instance.active}, status=status.HTTP_200_OK)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Room.objects.all()

        return Room.objects.filter(owner=user)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return RoomCreationSerializer
        return RoomSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user == self.get_object().owner or self.request.user.is_staff:
            serializer.save()
        else:
            return Response("You are not the owner or an admin of this room.", status=status.HTTP_403_FORBIDDEN)


class AnalogValuesViewSet(viewsets.ModelViewSet):
    queryset = AnalogValues.objects.all()
    serializer_class = AnalogValuesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return AnalogValues.objects.all()

        return AnalogValues.objects.filter(device__room__owner=user)

    def perform_create(self, serializer):
        user = self.request.user
        device = serializer.validated_data['device']

        if user.is_staff or user == device.room.owner:
            serializer.save()
        else:
            raise PermissionDenied(
                "You cannot create a value for a device in a room you don't own or you are not an admin.")

    def perform_update(self, serializer):
        if self.request.user == serializer.validated_data['device'].room.owner:
            serializer.save()
        else:
            raise PermissionDenied("You are not allowed to change the value of the device.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_staff:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.user == instance.device.room.owner:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("You are not authorized to delete this value.", status=status.HTTP_403_FORBIDDEN)


class DigitalValuesViewSet(viewsets.ModelViewSet):
    queryset = DigitalValues.objects.all()
    serializer_class = DigitalValuesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # If the user is an admin, show all digital values
        if user.is_staff:
            return DigitalValues.objects.all()

        # If the user is not an admin, show only digital values for devices in their room
        return DigitalValues.objects.filter(device__room__owner=user)

    def perform_create(self, serializer):
        user = self.request.user
        device = serializer.validated_data['device']

        if user.is_staff or user == device.room.owner:
            serializer.save()
        else:
            raise PermissionDenied(
                "You cannot create a value for a device in a room you don't own or you are not an admin.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_staff:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.user == instance.device.room.owner:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("You are not authorized to delete this value.", status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):
        if self.request.user == serializer.validated_data['device'].room.owner:
            serializer.save()
        else:
            raise PermissionDenied("You are not allowed to change the value of the device.")


class SmartValuesViewSet(viewsets.ModelViewSet):
    queryset = SmartValues.objects.all()
    serializer_class = SmartValuesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # If the user is an admin, show all smart values
        if user.is_staff:
            return SmartValues.objects.all()

        # If the user is not an admin, show only smart values for devices in their room
        return SmartValues.objects.filter(device__room__owner=user)

    def perform_create(self, serializer):
        user = self.request.user
        device = serializer.validated_data['device']

        if user.is_staff or user == device.room.owner:
            serializer.save()
        else:
            raise PermissionDenied(
                "You cannot create a value for a device in a room you don't own or you are not an admin.")

    def perform_update(self, serializer):
        # Check if the user is the owner of the device's room
        if self.request.user == serializer.validated_data['device'].room.owner:
            serializer.save()
        else:
            raise PermissionDenied("You are not allowed to change the value of the device.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_staff:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.user == instance.device.room.owner:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("You are not authorized to delete this value.", status=status.HTTP_403_FORBIDDEN)
