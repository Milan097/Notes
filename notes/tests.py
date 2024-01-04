from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from myuser.models import MyUser
from notes.models import Note, Share
from notes.serializer import NoteSerializer
from django.contrib.auth.hashers import make_password

class NotesViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = MyUser.objects.create(username='notes_testuser', password=make_password('testpassword'))
        self.client.force_authenticate(user=self.user)

        self.note_data = {
            "title": "Test Note",
            "content": "This is a test note",
        }
        self.note = Note.objects.create(author=self.user, **self.note_data)

        self.share_with_user = MyUser.objects.create(username='shareuser', password=make_password('sharepassword'))

    def test_list_notes(self):
        response = self.client.get('/api/notes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_note(self):
        response = self.client.get('/api/notes/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_note(self):
        response = self.client.post('/api/notes/', data=self.note_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_note(self):
        updated_data = {"title": "Updated Note", "content": "Updated content"}
        response = self.client.put('/api/notes/1/', data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_note(self):
        response = self.client.delete('/api/notes/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_share_note(self):
        data = {"share_with": self.share_with_user.id}
        response = self.client.post('/api/notes/1/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
