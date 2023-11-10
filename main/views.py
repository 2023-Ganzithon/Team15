from django.shortcuts import render, redirect
from post.models import *
from .models import *
from user.models import CustomUser
from django.db.models import Count

def mainpage_view(request):
    week_material = Material.objects.get(id=WeeklyMaterial.objects.last().matId.id).material
    most_liked = Post.objects.filter(material=WeeklyMaterial.objects.last()).annotate(count=Count('like')).order_by('-count')[:3]
    most_buyed = Post.objects.filter(material=WeeklyMaterial.objects.last()).annotate(count=Count('buy')).order_by('-count')[:3]
    context = {
        'week_material' : week_material,
        'most_liked' : most_liked,
        'most_buyed' : most_buyed
    }
    return render(request, 'main.html', context)


def sort_like_view(request):
    week_material = WeeklyMaterial.objects.last()
    likes = Post.objects.filter(material=week_material).annotate(count=Count('like')).order_by('-count')
    if request.user.is_authenticated:
        nowuser = CustomUser.objects.get(username = request.user.username)
        user_liked = Post.objects.filter(material=week_material, like=nowuser)
        user_buyed = Post.objects.filter(material=week_material, buy=nowuser)
        user_bookmarked = Post.objects.filter(material=week_material, bookmark=nowuser)

        context = {
            'week_material' : week_material,
            'likes' : likes,
            'user_liked' : user_liked,
            'user_buyed' : user_buyed,
            'user_bookmarked' : user_bookmarked
        }
        return render(request, 'sort_like.html', context)
    context = {
            'week_material' : week_material,
            'likes' : likes,
            'user_liked' : "",
            'user_buyed' : "",
            'user_bookmarked' : ""
    }
    return render(request, 'sort_like.html', context)


def sort_buy_view(request):
    week_material = WeeklyMaterial.objects.last()
    buys = Post.objects.filter(material=week_material).annotate(count=Count('buy')).order_by('-count')
    if request.user.is_authenticated:
        nowuser = CustomUser.objects.get(username = request.user.username)
        user_liked = Post.objects.filter(material=week_material, like=nowuser)
        user_buyed = Post.objects.filter(material=week_material, buy=nowuser)
        user_bookmarked = Post.objects.filter(material=week_material, bookmark=nowuser)

        context = {
            'week_material' : week_material,
            'buys' : buys,
            'user_liked' : user_liked,
            'user_buyed' : user_buyed,
            'user_bookmarked' : user_bookmarked
        }
        return render(request, 'sort_buy.html', context)
    context = {
            'week_material' : week_material,
            'buys' : buys,
            'user_liked' : "",
            'user_buyed' : "",
            'user_bookmarked' : ""
    }
    return render(request, 'sort_buy.html', context)