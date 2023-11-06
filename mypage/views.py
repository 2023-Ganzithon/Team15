from django.shortcuts import render, redirect
from datetime import datetime, timezone
from user.models import Attendance, CustomUser
from post.models import Post
from challenge.models import OngoingChallenge

def mypage_view(request):
    if request.user.is_authenticated:
        nowuser = CustomUser.objects.get(username = request.user.username)
        attended = False
        current_date = datetime.now()
        year = current_date.year
        month = current_date.month
        day = current_date.day
        nickname = nowuser.nickname
        coin = nowuser.coin
        date = (current_date - nowuser.createdAt.replace(tzinfo=None)).days
        postcnt = Post.objects.filter(userId = nowuser).count()
        challenge = ""
        bookmark = ""
        c_empty = True
        b_empty = True
        if OngoingChallenge.objects.filter(userId = nowuser).exists():
            c_empty = False
            challenge = OngoingChallenge.objects.filter(userId = nowuser).latest('cDate')
        if Post.objects.filter(bookmark = nowuser).exists():
            bookmark = Post.objects.filter(bookmark = nowuser).latest('id')
            b_empty = False
        if Attendance.objects.filter(userId = nowuser, attDate__year=year, attDate__month=month, attDate__day=day).exists():
            attended = True
        # POST 요청 시 출석체크 후 마이페이지 로딩(attended = True일 때는 화면에서 아예 출석체크 버튼 비활성화해서 post 못 하게 하기)
        if request.method == 'POST':
            att = Attendance(userId=nowuser)
            att.save()
        # GET 요청 시 마이페이지 로딩
        context = {
            'nickname' : nickname,
            'coin' : coin,
            'date' : date,
            'postcnt' : postcnt,
            'attended' : attended,
            'challenge' : challenge,
            'bookmark' : bookmark,
            'c_empty' : c_empty,
            'b_empty' : b_empty
        }
        return render(request, 'mypage.html', context)
    return redirect('/') # 로그인 페이지로 이동


def attendance_view(request):
    if request.user.is_authenticated:
        nowuser = CustomUser.objects.get(username = request.user.username)
        nickname = nowuser.nickname
        current_date = datetime.today()
        year = current_date.year
        month = current_date.month
        attendances = Attendance.objects.filter(userId = nowuser, attDate__year=year, attDate__month=month)
        context = {
            'nickname' : nickname,
            'attendances' : attendances
        }
        return render(request, 'attendance.html', context)
    return redirect('/') # 로그인 페이지로 이동


def challenge_view(request):
    if request.user.is_authenticated:
        nowuser = CustomUser.objects.get(username = request.user.username)
        nickname = nowuser.nickname
        challenges = OngoingChallenge.objects.filter(userId = nowuser)
        context = {
            'nickname' : nickname,
            'challenges' : challenges
        }
        return render(request, 'challenge.html', context)
    return redirect('/') # 로그인 페이지로 이동
        
        
def bookmark_view(request):
    if request.user.is_authenticated:
        nowuser = CustomUser.objects.get(username = request.user.username)
        nickname = nowuser.nickname
        bookmarks = Post.objects.filter(bookmark = nowuser)
        context = {
            'nickname' : nickname,
            'bookmarks' : bookmarks
        }
        return render(request, 'bookmark.html', context)
    return redirect('/') # 로그인 페이지로 이동