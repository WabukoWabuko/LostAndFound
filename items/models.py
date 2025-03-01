from django.db import models

class Item(models.Model):
    TYPE_CHOICES = [('lost', 'Lost'), ('found', 'Found')]
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    item_type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    contact = models.CharField(max_length=100)  # e.g., phone or email
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
