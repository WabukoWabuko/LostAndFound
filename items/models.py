from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self): return self.name

class Item(models.Model):
    TYPE_CHOICES = [('lost', 'Lost'), ('found', 'Found')]
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    item_type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    images = models.JSONField(default=list, blank=True)  # Store multiple image paths as a list
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow null for public viewing
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.title

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"{self.sender} to {self.receiver} about {self.item}"
