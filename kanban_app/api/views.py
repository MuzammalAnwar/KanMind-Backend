from django.db.models import Count, Q
from rest_framework import generics, permissions
from kanban_app.models import Board
from tasks_app.models import Task
from .serializers import BoardSerializer, BoardDetailSerializer
from .permissions import IsBoardOwnerOrMember


class BoardListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardSerializer

    def get_queryset(self):
        u = self.request.user
        return Board.objects.filter(Q(owner=u) | Q(members=u)).distinct()


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsBoardOwnerOrMember]
    serializer_class = BoardDetailSerializer
    queryset = Board.objects.all()
