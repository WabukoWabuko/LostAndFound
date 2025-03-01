from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item, Category
from .serializers import ItemSerializer, CategorySerializer
import os
from django.conf import settings

class ItemListCreate(generics.ListCreateAPIView):
    queryset = Item.objects.all().order_by('-created_at')
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Public can view, authenticated can post

    def get_queryset(self):
        return Item.objects.all()  # Public can view all items

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
    permission_classes = [permissions.AllowAny]  # Public can view details

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]  # Public can view categories

class SearchItems(APIView):
    permission_classes = [permissions.AllowAny]  # Public can search

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
