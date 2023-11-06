from django.shortcuts import render, redirect
from post.models import *
from .models import *
from django.db.models import Count

def mainpage_view(request):
    week_material = Material.objects.get(id=WeeklyMaterial.objects.last().matId.id).material
    most_liked = Post.objects.annotate(count=Count('like')).order_by('-count')[:3]
    most_buyed = Post.objects.annotate(count=Count('buy')).order_by('-count')[:3]
    context = {
        'week_material' : week_material,
        'most_liked' : most_liked,
        'most_buyed' : most_buyed
    }
    return render(request, 'main.html', context)