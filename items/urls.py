from django.urls import path
from .views import ItemListCreate, ItemDetail, MessageListCreate, SearchItems, CategoryList

urlpatterns = [
    path('items/', ItemListCreate.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),
    path('messages/', MessageListCreate.as_view(), name='message-list-create'),
    path('search/', SearchItems.as_view(), name='search-items'),
    path('categories/', CategoryList.as_view(), name='category-list'),
]
