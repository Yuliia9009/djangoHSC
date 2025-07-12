from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

class Region(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TSC(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="tscs")
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.region.name} — {self.name}"

class VehicleType(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="searches", null=True, blank=True)
    digits = models.CharField(max_length=4, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    selected_tsc = models.ForeignKey(TSC, on_delete=models.SET_NULL, null=True, blank=True)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    results_count = models.IntegerField(default=0)

# class AvailableResult(models.Model):
#     user_search = models.ForeignKey(UserSearch, on_delete=models.CASCADE)
#     region = models.ForeignKey(Region, on_delete=models.CASCADE)
#     vehicle_type = models.ForeignKey(VehicleType, on_delete=models.SET_NULL, null=True)
#     plate_number = models.CharField(max_length=10)
#     found_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plate_number} ({self.region.name})"

class SearchSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    selected_tsc = models.ForeignKey(TSC, null=True, blank=True, on_delete=models.SET_NULL)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    digits = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    last_checked = models.DateTimeField(null=True, blank=True)

class AvailableResult(models.Model):
    subscription = models.ForeignKey(SearchSubscription, related_name='available_results', on_delete=models.CASCADE, null=True, blank=True)
    plate = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    found_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.plate

class Meta:
    unique_together = ('user', 'digits', 'region', 'selected_tsc', 'vehicle_type')