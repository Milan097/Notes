from rest_framework import permissions, viewsets, throttling, status
from rest_framework.response import Response
from notes.models import Note, Share, MyUser
from notes.serializer import NoteSerializer
from rest_framework.decorators import action, api_view, permission_classes
from django.db.models import Q
from django_ratelimit.decorators import ratelimit


class ThrottleModel(throttling.AnonRateThrottle):
    THROTTLE_RATES = {
        'anon': '2/minute',  # 2 requests per minute for anonymous users
        'user': '5/minute',  # 5 requests per minute for authenticated users
    }


class NotesViewSet(viewsets.ModelViewSet):
    throttle_classes = (ThrottleModel,)
    permission_classes = (permissions.IsAuthenticated, )
    http_method_names = ['get', 'list', 'post', 'put',  'head', 'delete']
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def list(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            
            # Get all notes of current user
            notes = self.get_queryset().filter(author_id=user_id)
            notes = NoteSerializer(notes, many=True).data

            # Get all notes shared_with the current user
            shared_notes = Share.objects.filter(shared_with__id=user_id).values_list('note_id', flat=True)
            shared_notes = self.get_queryset().filter(id__in=shared_notes)
            shared_notes = NoteSerializer(shared_notes, many=True).data

            response = {
                "my_notes": notes,
                "shared_with_me": shared_notes
            }

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Internal server error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        user_id = request.user.id
        instance = self.get_object()

        # Verifying if the note should be accessible by this user or not
        if user_id and (instance.author_id == user_id or instance.shared_with.id == user_id):
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response(data="Note is not accessible for you !!!", status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        user_id = request.user.id
        instance = self.get_object()

        # Verifying if the note should be editable by this user or not
        if user_id and instance.author_id == user_id:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data="Note is not editable by you !!!", status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        user_id = request.user.id
        instance = self.get_object()
        
        # Verifying if the note should be editable by this user or not
        if user_id and instance.author_id == user_id:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data="Note is not editable by you !!!", status=status.HTTP_401_UNAUTHORIZED)
        
    @action(methods=["POST"], detail=True)
    def share(self, request, *args, **kwargs):
        user_id = request.user.id
        share_with_user_id = request.data.get('share_with')
        try:
            share_with_user = MyUser.objects.get(id=share_with_user_id)
        except:
            return Response("Please provide valid user details with whom you want to share the note.", status=status.HTTP_400_BAD_REQUEST)
        
        if user_id == share_with_user_id:
            return Response("Can not share the note with yourself.", status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()

        # Verifying if the note should be editable by this user or not
        if user_id and instance.author_id == user_id:
            share_obj, created = Share.objects.get_or_create(
                shared_by=request.user, shared_with=share_with_user, note=instance)
            
            if not created:
                return Response(f"This Note is already shared with {share_with_user.username}!!!", status=status.HTTP_200_OK)
            else:
                return Response(f"Shared the Note {share_with_user.username}!!!", status=status.HTTP_200_OK)
        else:
            return Response(data="Note is not sharable by you !!!", status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
@ratelimit(key='ip', rate='25/m', block=True)
def search(request):
    search_query = request.query_params.get('q', '').strip()

    user_id = request.user.id
            
    # Get all notes of current user
    notes = Note.objects.filter(author_id=user_id).filter(
        Q(content__icontains=search_query) | Q(title__icontains=search_query))
    notes = NoteSerializer(notes, many=True).data

    # Get all notes shared_with the current user
    shared_notes = Share.objects.filter(shared_with__id=user_id).values_list('note_id', flat=True)
    shared_notes = Note.objects.filter(id__in=shared_notes).filter(
        Q(content__icontains=search_query) | Q(title__icontains=search_query))
    shared_notes = NoteSerializer(shared_notes, many=True).data

    response = {
        "my_notes": notes,
        "shared_with_me": shared_notes
    }
    return Response(response, status=status.HTTP_200_OK)
