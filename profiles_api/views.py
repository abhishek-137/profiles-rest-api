from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import response
from profiles_api import serializers, models, permissions
from rest_framework import status
# for authentication for api login
from rest_framework.authentication import TokenAuthentication

from rest_framework import filters

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated


class Hello_ApiView(APIView):

    serializer_class = serializers.HelloSerializer

    def get(self, request, pk=None):
        return response({"a": "b"})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            return response("fhello {name}")

        else:
            return response(serializer.errors,
                            status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        return response({"menthod": "put"})

    def patch(self, request, pk=None):
        return response({"menthod": "Patch"})

    def delete(self, request, pk=None):
        return response({"menthod": "delete"})


class HelloViewSet(viewsets.ViewSet):
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        return response({"a": "b"})

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            return response("fhello {name}")

        else:
            return response(serializer.errors,
                            status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        return response({"menthod": "get"})

    def update(self, request, pk=None):
        return response({"menthod": "Put"})

    def partial_update(self, request, pk=None):
        return response({"menthod": "patch"})

    def destroy(self, request, pk=None):
        return response({"menthod": "delete"})


"""
    1. /post -register
    2. /get -all
    3. /get -specific id
    4. /put-details
    5. /patch-details
    6. /delete -pkid

    /api/profile -1,2
    /api/profile/profile_id- 3 4 5 6
"""


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')


class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permissions.UpdateOwnStatus, IsAuthenticated
    )

# IsAuthenticatedOrReadOnly enables user to view  feed without being autenticated
# while IsAuthenticated restricts user to view feed if he is not authenticated or have not logged in

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)
