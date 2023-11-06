from django.utils import timezone

from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect

from main.models import Material, WeeklyMaterial
from post.models import Post


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
def post_create_view(request):

    user = request.user
    material = WeeklyMaterial.objects.latest("week")

    # 생성 폼
    if request.method == 'GET':
        return render(request, 'post_form.html')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        Post.objects.create(
            userId=request.user,
            material=material,
            title=title,
            content=content,
            regTime=timezone.now(),
            image=image
        )

        return redirect('post:post_list')

    return render(request, 'post_form.html')


# 게시글 수정






