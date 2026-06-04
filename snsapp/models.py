from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
   title = models.CharField(max_length=100)
   content = models.TextField()
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   #like追加
   like = models.ManyToManyField(User, related_name='related_post', blank=True)
   created_at = models.DateTimeField(auto_now_add=True)


   def __str__(self):
       return self.title

   class Meta:
       ordering = ["-created_at"]     #投稿順にクエリを取得


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        related_name='following_rel',
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User,
        related_name='followers_rel',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} -> {self.following}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content