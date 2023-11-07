from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect

from main.models import Material, WeeklyMaterial
from post.models import Post, Video, Comment


# 게시글 전체 조회
def post_list_view(request):

    # 필터링을 위한 재료 목록
    materials = WeeklyMaterial.objects.all()

    # 게시글 전체 조회
    if request.method == 'GET':
        posts = Post.objects.all().order_by('-regTime')

    return render(request, 'post_list.html', context={'posts':posts, 'materials':materials})


# 게시글 필터링
def post_filtered_view(request):

    # 필터링을 위한 재료 목록
    materials = WeeklyMaterial.objects.all()

    materialText = request.POST.get('material')
    status = request.POST.get('status')


    if materialText != 'all':
        # 재료 객체 찾기
        material = get_object_or_404(Material, material=materialText)
        weeklyMaterial = WeeklyMaterial.objects.filter(matId=material)

        posts = Post.objects.filter(material=weeklyMaterial) # 1차 필터링
        if status != 'all':
            posts = posts.annotate(count=Count(status)).order_by('-count') # 2차 필터링
        else:
            posts = posts

    else:
        posts = Post.objects.all()
        if status != 'all':
            posts = posts.annotate(count=Count(status)).order_by('-count')
        else:
            posts = posts

    return render(request, 'post_list.html', context={'posts':posts, 'materials':materials, 'status':status})


# 게시글 생성
@login_required
def post_create_view(request):

    material = WeeklyMaterial.objects.latest("week")

    # 생성 폼 반환
    if request.method == 'GET':
        return render(request, 'post_form.html')

    # 게시글, 비디오 생성
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        videoKey = request.POST.get('videoKey')

        post = Post.objects.create(
            userId=request.user,
            material=material,
            title=title,
            content=content,
            image=image
        )

        # 비디오키는 필수 아님
        if videoKey:
            Video.objects.create(
                postId=post,
                videoKey=videoKey
            )

        return redirect('post:post_list')

    return render(request, 'post_form.html')


def determine_edit_mode(user, postId):
    if postId:
        post = get_object_or_404(Post, pk=postId)

        # 게시글의 작성자와 현재 사용자를 비교하여 수정 권한을 확인
        if post.userId == user:
            return True  # 수정 모드
    return False  # 작성 모드

# 게시글 수정
@login_required
def post_update_view(request, postId):
    # 게시글 찾기
    post = get_object_or_404(Post, pk=postId)
    video = Video.objects.get(postId=post)
    comments = Comment.objects.filter(postId=post)
    edit_mode = determine_edit_mode(request.user, postId)

    # 수정 폼 반환
    if request.method == 'GET':
        return render(request, "post_form.html", context={"post":post, "video":video, "edit_mode":edit_mode})

    if request.method == 'POST':
        # 수정
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        videoKey = request.POST.get('videoKey')

        if image is None:
            # 새로운 이미지가 제출되지 않은 경우 기존 이미지 유지
            image = post.image

        post.title = title
        post.content = content
        post.image = image

        if videoKey:
            video = get_object_or_404(Video, postId=post)
            video.videoKey=videoKey

        post.save()
        video.save()

        return render(request, "post_detail.html", context={"post": post, "comments":comments, "video":video})

# 게시글 상세 조회
def post_detail_view(request, postId):

    post = get_object_or_404(Post, pk=postId)
    comments = Comment.objects.filter(postId=post)
    video = get_object_or_404(Video, postId=post)

    return render(request, "post_detail.html", context={"post": post, "comments":comments, "video":video})

# 게시글 삭제
def post_delete_view(request, postId):
    post = get_object_or_404(Post, pk=postId)
    post.delete()

    return redirect('post:post_list')

# 댓글 생성
@login_required
def comment_create_view(request, postId):
    post = get_object_or_404(Post, pk=postId)
    content = request.POST.get('content')
    anonymousText = request.POST.get('anonymous')

    if anonymousText == 'on': # 익명 여부 체크
        anonymous = True # 익명
    else:
        anonymous = False # 실명

    Comment.objects.create(
        userId=request.user,
        postId=post,
        content=content,
        anonymous=anonymous
    )

    return redirect('post:post_detail', postId=postId)



# 댓글 삭제
def comment_delete_view(request, commentId):
    comment = get_object_or_404(Comment, pk=commentId)
    post = comment.postId
    comment.delete()

    comments = Comment.objects.filter(postId=post)

    return render(request, "post_detail.html", context={"post": post, "comments":comments})
