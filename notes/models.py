from django.db import models
from django.utils import timezone
from django.contrib.postgres.indexes import GinIndex
from myuser.models import MyUser


class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)


class Note(models.Model):
    title = models.CharField(max_length=50) 
    content = models.TextField() 
    tags = models.ManyToManyField(Tag, related_name='notes', blank=True)  # For future use, if we want to search based on tags
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True, related_name="notes")
    updated_on = models.DateTimeField(default=timezone.now, db_index=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            GinIndex(name='content_index', fields=['content',], opclasses=['gin_trgm_ops']), 
            GinIndex(name='title_index', fields=['title',],opclasses=['gin_trgm_ops'] )
        ]
    
    def __str__(self) -> str:
        return f"{self.author_id} - {self.title}"


class Share(models.Model):
    shared_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="shared_by")
    shared_with = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="shared_with")
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="share")
    shared_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.shared_by_id}:{self.shared_with_id} - {self.title}"
