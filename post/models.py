from django.db import models

# 게시글
class Post(models.Model):
    userId = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    regTime = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=False)

    like = models.ManyToManyField('user.CustomUser', related_name="like_posts")
    buy = models.ManyToManyField('user.CustomUser', related_name="buy_posts")
    bookmark = models.ManyToManyField('user.CustomUser', related_name="bookmark_posts")

# 댓글
class Comment(models.Model):
    userId = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)
    postId = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    content = models.TextField()
    anonymous = models.BooleanField(default=True) # True = 익명 / False = 실명


# 동영상
class Video(models.Model):
    postId = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    videoKey = models.CharField(max_length=5000)