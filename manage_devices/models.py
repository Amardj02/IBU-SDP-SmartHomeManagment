from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AnalogDevice(models.Model):
    mac_address = models.CharField(max_length=17)
    name = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='analog_devices')
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"Analog Device for {self.name}"


class DigitalDevice(models.Model):
    mac_address = models.CharField(max_length=17)
    name = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='digital_devices')
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"Digital Device for {self.name}"


class SmartDevice(models.Model):
    protocol_name = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=17)
    name = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='smart_devices')
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"Smart Device for {self.name}"


class AnalogValues(models.Model):
    device = models.ForeignKey('AnalogDevice', on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return f"{self.device.name} - Analog Value: {self.value}"


class DigitalValues(models.Model):
    device = models.ForeignKey('DigitalDevice', on_delete=models.CASCADE)
    value = models.BooleanField()

    def __str__(self):
        return f"{self.device.name} - Digital Value: {self.value}"


class SmartValues(models.Model):
    device = models.ForeignKey('SmartDevice', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.device.name} - Smart Value: {self.value}"


class Settings(models.Model):
    broker_ip = models.GenericIPAddressField()

    def __str__(self):
        return f"Settings for Broker: {self.broker_ip}"
