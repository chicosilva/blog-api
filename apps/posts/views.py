from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.posts.filters import ProductFilter
from apps.posts.models import Post

from apps.posts.serializers import PostSerializer
from apps.shared.service import SharedService


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminUser]
    filterset_class = ProductFilter

    def destroy(self, request, *args, **kwargs):
        SharedService().set_canceled(instance=self.get_object(),
                                     user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
