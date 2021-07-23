from django.db import models
from account.models import CustomUser

# Create your models here.


class Blog(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    writer = models.CharField(max_length=20)
    pub_date = models.DateTimeField()
    body = models.TextField()
    image = models.ImageField(upload_to="blog/", blank=True, null=True)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:10]


class Comment(models.Model):
    post = models.ForeignKey(
        Blog, related_name='comments', on_delete=models.CASCADE)
    writer = models.CharField(max_length=20)
    comment = models.TextField()
    # 들어갈 내용들 : 댓글 작성자, 댓글 내용, 댓글 작성 시간

    def approve(self):
        self.save()

    def __str__(self):
        return self.comment
