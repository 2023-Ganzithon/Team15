from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect

from main.models import Material, WeeklyMaterial
from post.models import Post, Comment

# 유저 별 좋아요 / 살래요 / 북마크 누른 게시글 리스트
def post_list_status(request):
    liked_posts = Post.objects.filter(like=request.user)
    buy_posts = Post.objects.filter(buy=request.user)
    bookmarked_posts = Post.objects.filter(bookmark=request.user)

    return liked_posts, buy_posts, bookmarked_posts

# 특정 게시글에 좋아요 / 살래요 / 북마크 누른 유저 리스트
def post_list_status_user(post):
    liked_user = post.like.all()  # 게시글에 좋아요 누른 유저
    buy_user = post.buy.all()  # 게시글에 살래요 누른 유저
    bookmarked_user = post.bookmark.all()  # 게시글에 북마크 누른 유저

    return liked_user, buy_user, bookmarked_user

# post_form.html의 작성하기 / 수정하기 버튼 변경 위한 메소드
def determine_edit_mode(user, postId):
    if postId:
        post = get_object_or_404(Post, pk=postId)

        # 게시글의 작성자와 현재 사용자를 비교하여 수정 권한을 확인
        if post.userId == user:
            return True  # 수정 모드
    return False  # 작성 모드

# 게시글 전체 조회
def post_list_view(request):
    # 필터링을 위한 재료 목록
    materials = Material.objects.all()

    # 게시글 전체 조회
    if request.method == 'GET':
        posts = Post.objects.all()
        liked_posts, buy_posts, bookmarked_posts = post_list_status(request)

        context = {
            'posts': posts,
            'liked_posts': liked_posts,
            'buy_posts': buy_posts,
            'bookmarked_posts': bookmarked_posts,
            'materials': materials
        }

        return render(request, 'post_list.html', context)




# 게시글 상세 조회
def post_detail_view(request, postId):

    post = get_object_or_404(Post, pk=postId)
    comments = Comment.objects.filter(postId=post)

    liked_user, buy_user, bookmarked_user = post_list_status_user(post)

    context = {
        "post": post,
        "comments": comments,
        "liked_user": liked_user,
        "buy_user": buy_user,
        "bookmarked_user": bookmarked_user,
    }

    return render(request, "post_detail.html", context)


# 게시글 필터링
def post_filtered_view(request):

    materialText = request.POST.get('material') # 재료
    status = request.POST.get('status') # 최신순 / 좋아요 / 살래요

    if materialText != 'all':  # 재료 지정한 경우
        # 재료 객체 찾기
        material = get_object_or_404(Material, material=materialText)
        weeklyMaterial = WeeklyMaterial.objects.filter(matId=material)

        posts = Post.objects.filter(material__in=weeklyMaterial)  # 1차 필터링
    else:  # 전체 재료인 경우
        posts = Post.objects.all()

    if status != 'all':  # 좋아요/살래요 순이면
        posts = posts.annotate(count=Count(status)).order_by('-count')  # 2차 필터링
    else:  # 최신순인 경우
        posts = posts.order_by('-regTime')

    # 필터링을 위한 재료 목록
    materials = Material.objects.all()
    liked_posts, buy_posts, bookmarked_posts = post_list_status(request)

    context = {
        'posts': posts,
        'liked_posts': liked_posts,
        'buy_posts': buy_posts,
        'bookmarked_posts': bookmarked_posts,
        'materials': materials
    }

    return render(request, 'post_list.html', context)


# 게시글 생성
def post_create_view(request):
    if request.user.is_authenticated:
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

            Post.objects.create(
                userId=request.user,
                material=material,
                title=title,
                content=content,
                image=image,
                videoKey=videoKey
            )

            return redirect('post:post_list')
        return render(request, 'post_form.html')

    return redirect('user:login')


# 게시글 수정
def post_update_view(request, postId):
    if request.user.is_authenticated:
        # 게시글 찾기
        post = get_object_or_404(Post, pk=postId)
        comments = Comment.objects.filter(postId=post)
        edit_mode = determine_edit_mode(request.user, postId)

        # 수정 폼 반환
        if request.method == 'GET':
            return render(request, "post_form.html", context={"post":post, "edit_mode":edit_mode})

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
            post.videoKey = videoKey

            post.save()

            return render(request, "post_detail.html", context={"post": post, "comments":comments})

    return redirect('user:login')


# 게시글 삭제
def post_delete_view(request, postId):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=postId)
        post.delete()

        return redirect('post:post_list')

    return redirect('user:login')


# 댓글 생성
def comment_create_view(request, postId):
    if request.user.is_authenticated:
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

    return redirect('user:login')


# 댓글 삭제
def comment_delete_view(request, commentId):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=commentId)
        post = comment.postId
        comment.delete()

        comments = Comment.objects.filter(postId=post)

        return render(request, "post_detail.html", context={"post": post, "comments":comments})

    return redirect('user:login')


# 좋아요 / 살래요 / 북마크
def post_status_view(request, postId, status):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = request.user
            post = get_object_or_404(Post, pk=postId)
            comments = Comment.objects.filter(postId=post)

            liked_user, buy_user, bookmarked_user = post_list_status_user(post)

            # 상태 변경
            if (status == 'like_cancel'):
                post.like.remove(user)
            elif (status == 'like'):
                post.like.add(user)

            if (status == 'buy_cancel'):
                post.buy.remove(user)
            elif (status == 'buy'):
                post.buy.add(user)

            if (status == 'bookmark_cancel'):
                post.bookmark.remove(user)
            elif (status == 'bookmark'):
                post.bookmark.add(user)

            context = {
                "post": post,
                "comments": comments,
                "liked_user": liked_user,
                "buy_user": buy_user,
                "bookmarked_user": bookmarked_user,
            }

        return render(request, "post_detail.html", context)

    return redirect('user:login')


# 동영상 전체 조회 (숏폼)
def video_list_view(request):
    if request.method == 'GET':
        # 비디오 키를 가지고 있는 게시글만 가져옴
        posts = Post.objects.filter(videoKey__isnull=False)
        comments = Comment.objects.all()

        posts_status = []

        for post in posts:
            post = post
            liked_user, buy_user, bookmarked_user = post_list_status_user(post)

            post_status = {
                'post':post,
                'liked_user':liked_user,
                'buy_user':buy_user,
                'bookmarked_user':bookmarked_user
            }

            posts_status.append(post_status)

        context = {
            "comments": comments,
            "posts_status":posts_status
        }

        return render(request, "video_list.html", context)