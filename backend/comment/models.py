# # from time import timezone
# from django.db import models
# from authors.models import AppUser
# from django.utils import timezone
# import uuid
# from posts.models import Post



# class Comment(models.Model):

#     CONTENT_CHOICE = [
#         ("text/markdown","text/markdown"), 
#         ("text/plain","text/plain"),
#         ("application/base64","application/base64"),
#         ("image/png;base64","image/png;base64"),
#         ("image/jpeg;base64","image/jpeg;base64")
#     ]

#     comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     type = models.CharField(default="comment",max_length=7, editable=False)
#     comment = models.TextField()
#     id = models.URLField(max_length=2048, blank=True, null=True, editable=False)
#     contentType = models.CharField(max_length=30, choices=CONTENT_CHOICE, default='text/plain')
#     author = models.ForeignKey(AppUser, on_delete=models.CASCADE)
#     url = models.URLField(max_length=500,editable=False,null=True,blank=True)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment_for_post")
#     published = models.DateTimeField("Published",default=timezone.now)
    
    
#     def get_type(self):
#         return self.contentType

#     def get_id(self):
#         return self.id
    
#     def save(self, *args, **kwargs):
#         self.url = str(self.post.url) + "/comments/" + str(self.comment_id)
#         self.id = self.url
#         super().save(*args, **kwargs)
