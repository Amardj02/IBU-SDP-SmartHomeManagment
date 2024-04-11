from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Room, AnalogDevice, DigitalDevice, SmartDevice, AnalogValues, DigitalValues, SmartValues


class AnalogDeviceSerializer(serializers.HyperlinkedModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = AnalogDevice
        fields = ('url', 'id', 'mac_address', 'name', 'ip', 'room', 'active')

    def create(self, validated_data):
        if (self.context['request'].user == validated_data['room'].owner) or self.context['request'].user.is_staff:
            return super().create(validated_data)
        raise serializers.ValidationError("You cannot create a device in a room you don't own.")

    def update(self, instance, validated_data):
        if self.context['request'].user.is_staff:
            instance.room = validated_data.get('room', instance.room)

        instance.name = validated_data.get('name', instance.name)
        instance.mac_address = validated_data.get('mac_address', instance.mac_address)
        instance.ip = validated_data.get('ip', instance.ip)
        instance.save()
        return instance


class DigitalDeviceSerializer(serializers.HyperlinkedModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = DigitalDevice
        fields = ('url', 'id', 'mac_address', 'name', 'ip', 'room', 'active')

    def create(self, validated_data):
        if (self.context['request'].user == validated_data['room'].owner) or self.context['request'].user.is_staff:
            return super().create(validated_data)
        raise serializers.ValidationError("You cannot create a device in a room you don't own.")

    def update(self, instance, validated_data):
        if self.context['request'].user.is_staff:
            instance.room = validated_data.get('room', instance.room)

        instance.name = validated_data.get('name', instance.name)
        instance.mac_address = validated_data.get('mac_address', instance.mac_address)
        instance.ip = validated_data.get('ip', instance.ip)
        instance.save()
        return instance


class SmartDeviceSerializer(serializers.HyperlinkedModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = SmartDevice
        fields = ('url', 'id', 'protocol_name', 'mac_address', 'name', 'ip', 'room', 'active')

    def create(self, validated_data):
        if (self.context['request'].user == validated_data['room'].owner) or self.context['request'].user.is_staff:
            return super().create(validated_data)
        raise serializers.ValidationError("You cannot create a device in a room you don't own.")

    def update(self, instance, validated_data):
        if self.context['request'].user.is_staff:
            instance.room = validated_data.get('room', instance.room)

        instance.name = validated_data.get('name', instance.name)
        instance.mac_address = validated_data.get('mac_address', instance.mac_address)
        instance.ip = validated_data.get('ip', instance.ip)
        instance.save()
        return instance


class AnalogValuesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnalogValues
        fields = ('url', 'id', 'device', 'value')


class DigitalValuesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DigitalValues
        fields = ('url', 'id', 'device', 'value')


class SmartValuesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SmartValues
        fields = ('url', 'id', 'device', 'value')


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    devices = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('id', 'name', 'owner', 'devices')

    def get_devices(self, room):
        device_list = []

        analog_devices = AnalogDevice.objects.filter(room=room)
        digital_devices = DigitalDevice.objects.filter(room=room)
        smart_devices = SmartDevice.objects.filter(room=room)

        for device in analog_devices:
            device_data = {
                'id': device.id,
                'type': 'Analog',
                'name': device.name,
                'ip': device.ip,
                'value': None
            }

            latest_value = AnalogValues.objects.filter(device=device).order_by('-id').first()
            if latest_value:
                device_data['value'] = latest_value.value

            device_list.append(device_data)

        for device in digital_devices:
            device_data = {
                'id': device.id,
                'type': 'Digital',
                'name': device.name,
                'ip': device.ip,
                'value': None
            }

            latest_value = DigitalValues.objects.filter(device=device).order_by('-id').first()
            if latest_value:
                device_data['value'] = latest_value.value

            device_list.append(device_data)

        for device in smart_devices:
            device_data = {
                'id': device.id,
                'type': 'Smart',
                'name': device.name,
                'ip': device.ip,
                'value': None
            }

            latest_value = SmartValues.objects.filter(device=device).order_by('-id').first()
            if latest_value:
                device_data['value'] = latest_value.value

            device_list.append(device_data)

        return device_list

class RoomCreationSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Room
        fields = ('name', 'owner')
