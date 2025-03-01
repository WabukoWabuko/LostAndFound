from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item, Message, Category
from .serializers import ItemSerializer, MessageSerializer, CategorySerializer
import os
from django.conf import settings

class ItemListCreate(generics.ListCreateAPIView):
    queryset = Item.objects.all().order_by('-created_at')
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Public can view, authenticated users can post

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Item.objects.filter(created_by__isnull=True)  # Public items only
        return Item.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_anonymous:
            raise permissions.PermissionDenied("You must be logged in to post items.")
        images = self.request.FILES.getlist('images', [])  # Handle multiple images
        image_paths = []
        for image in images[:4]:  # Limit to 4 images
            path = os.path.join('items', f'{serializer.instance.id}_{image.name}')
            with open(os.path.join(settings.MEDIA_ROOT, path), 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            image_paths.append(f'/media/{path}')
        serializer.save(created_by=self.request.user, images=image_paths)

class ItemDetail(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MessageListCreate(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can chat

    def get_queryset(self):
        item_id = self.request.query_params.get('item_id')
        if not self.request.user.is_authenticated:
            raise permissions.PermissionDenied("You must be logged in to view chats.")
        return Message.objects.filter(item_id=item_id, receiver=self.request.user) | Message.objects.filter(item_id=item_id, sender=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise permissions.PermissionDenied("You must be logged in to send messages.")
        serializer.save(sender=self.request.user)

class SearchItems(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        item_type = request.query_params.get('type', '')
        category_id = request.query_params.get('category', '')
        location = request.query_params.get('location', '')
        items = Item.objects.all()
        if query:
            items = items.filter(title__icontains=query) | items.filter(description__icontains=query)
        if item_type:
            items = items.filter(item_type=item_type)
        if category_id:
            items = items.filter(category_id=category_id)
        if location:
            items = items.filter(location__icontains=location)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
