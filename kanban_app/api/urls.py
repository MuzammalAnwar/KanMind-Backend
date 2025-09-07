from django.urls import path, include
from .views import BoardListCreateView, BoardDetailView


urlpatterns = [
    path('boards/', BoardListCreateView.as_view(), name='boards-list-create'),
    path('boards/<int:pk>', BoardDetailView.as_view(),
         name='board-detail-view'),
]
