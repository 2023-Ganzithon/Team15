from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.db.models import Q
from user.models import Attendance, CustomUser
from post.models import Post
from challenge.models import OngoingChallenge

def mypage_view(request):
    if request.user.is_authenticated:
        nowuser = CustomUser.objects.get(username = request.user.username)
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
        challenges = OngoingChallenge.objects.filter(userId = nowuser)
        try:
            challenge_rate = len(challenges.filter(cCheck=True))/len(challenges) * 100
        except:
            challenge_rate = 0
        if challenges.filter(cDate__year=year, cDate__month=month, cDate__day=day).exists():
            c_empty = False
            challenge = challenges.filter(cDate__year=year, cDate__month=month, cDate__day=day).latest('id')
        if Post.objects.filter(bookmark = nowuser).exists():
            bookmark = Post.objects.filter(bookmark = nowuser).latest('id')
            b_empty = False
        # GET 요청 시 마이페이지 로딩
        context = {
            'nickname' : nickname,
            'coin' : coin,
            'date' : date,
            'postcnt' : postcnt,
            'challenge' : challenge,
            'bookmark' : bookmark,
            'c_empty' : c_empty,
            'b_empty' : b_empty,
            'challenge_rate' : challenge_rate
        }
        return render(request, 'mypage.html', context)
    return redirect('user:login') # 로그인 페이지로 이동


def attendance_view(request):
    if request.user.is_authenticated:
        attended = False
        current_date = datetime.now()
        year = current_date.year
        month = current_date.month
        day = current_date.day
        nowuser = CustomUser.objects.get(username = request.user.username)
        nickname = nowuser.nickname
        
        days_until_monday = (current_date.weekday()) % 7  # 월요일까지 남은 일 수
        if days_until_monday == 0:
            week_start = current_date - timedelta(hours=current_date.hour, minutes=current_date.minute, seconds=current_date.second)
        else:
            week_start = current_date - timedelta(days=days_until_monday, hours=current_date.hour, minutes=current_date.minute, seconds=current_date.second)
        week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
        
        if Attendance.objects.filter(userId = nowuser, attDate__year=year, attDate__month=month, attDate__day=day).exists():
            attended = True
        else:
            if request.method == 'POST':
                att = Attendance(userId=nowuser)
                att.save()
                nowuser.coin += 1
                month_count = len(Attendance.objects.filter(userId = nowuser, attDate__year=year, attDate__month=month))
                if month_count % 7 == 0 and month_count != 0:
                    nowuser.coin += 5
                attendances = Attendance.objects.filter(Q(userId = nowuser) & Q(attDate__gte=week_start) & Q(attDate__lte=week_end))
                context = {
                    'nickname' : nickname,
                    'attendances' : attendances,
                    'attended' : attended
                }
                return render(request, 'attendance.html', context)

        attendances = Attendance.objects.filter(Q(userId = nowuser) & Q(attDate__gte=week_start) & Q(attDate__lte=week_end))
        context = {
            'nickname' : nickname,
            'attendances' : attendances,
            'attended' : attended
        }
        return render(request, 'attendance.html', context)
    return redirect('user:login') # 로그인 페이지로 이동


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
    return redirect('user:login') # 로그인 페이지로 이동
        
        
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
    return redirect('user:login') # 로그인 페이지로 이동