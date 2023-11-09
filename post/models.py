from django.db import models

# 게시글
class Post(models.Model):
    userId = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)
    material = models.ForeignKey('main.WeeklyMaterial', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    regTime = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=False, upload_to='')
    videoKey = models.CharField(null=True, max_length=20)

    like = models.ManyToManyField('user.CustomUser', related_name="like_posts", blank=True)
    buy = models.ManyToManyField('user.CustomUser', related_name="buy_posts", blank=True)
    bookmark = models.ManyToManyField('user.CustomUser', related_name="bookmark_posts", blank=True)

    def __str__(self):
        return self.title

# 댓글
class Comment(models.Model):
    userId = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)
    postId = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    content = models.TextField()
    regTime = models.DateTimeField(auto_now_add=True)
    anonymous = models.BooleanField(default=True) # True = 익명 / False = 실명

    def __str__(self):
        return self.postId.title
