from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.db.models import Q
from user.models import Attendance, CustomUser
from post.models import Post
from main.models import WeeklyMaterial
from challenge.models import OngoingChallenge
from django.db.models import F, FloatField, ExpressionWrapper, Subquery, OuterRef, IntegerField
from django.db.models import Sum, Count

def mypage_view(request):
    if request.user.is_authenticated:
        nowuser = CustomUser.objects.get(username = request.user.username)
        
        # 현재 사용자의 백분위 구하기
        users = CustomUser.objects.annotate(
            post_count = Subquery(
                Post.objects.filter(userId=OuterRef('id')).values('userId').annotate(count=Count('id')).values('count')[:1],
                output_field=IntegerField()
            ),
            challenge_count = Subquery(
                OngoingChallenge.objects.filter(userId=OuterRef('id'), cCheck=True).values('userId').annotate(count=Count('id')).values('count')[:1],
                output_field=IntegerField()
            ),
            total_score=ExpressionWrapper(
                F('post_count') * 0.4 + F('challenge_count') * 0.6,
                output_field=FloatField()
            )
        )
        
        # 스코어를 기준으로 내림차순 정렬
        sorted_users = users.order_by('-total_score')
        
        # 현재 로그인된 사용자의 스코어
        postcnt = Post.objects.filter(userId = nowuser).count()
        challenges = OngoingChallenge.objects.filter(userId = nowuser, cCheck = True)
        challengecnt = challenges.count()
        current_user_score = postcnt * 0.4 + challengecnt * 0.6
        
        # 현재 로그인된 사용자의 스코어가 전체 사용자 중 어느 위치에 있는지 계산
        current_user_rank = sorted_users.filter(total_score__gt=current_user_score).count() + 1

        # 전체 사용자 수
        total_users = users.count()

        # 상위 몇 퍼센트에 속하는지 계산
        top_percentage = (current_user_rank / total_users) * 100
        
        current_date = datetime.now()
        coin_message = []
        
        # 월요일인지 확인 후 랭킹 내에 들었을 시 코인 지급
        if current_date.weekday() == 0:
            ranked = Post.objects.filter(material=WeeklyMaterial.objects.order_by('-week')[-2]).annotate(count=Count('like')).order_by('-count')[:3].values_list('id', flat=True)
            user_posts = Post.objects.filter(userId = nowuser, material=WeeklyMaterial.objects.order_by('-week')[-2]).values_list('id', flat=True)
            
            coin_list = [500, 300, 100]
            for i in range(3):
                if ranked[i] in user_posts:
                    nowuser.coin += coin_list[i]
                    coin_message.append(f"지난주 {i+1}등 게시글 작성!\n{coin_list[i]}원 지급 완료!")
            nowuser.save()
        
        year = current_date.year
        month = current_date.month
        day = current_date.day
        nickname = nowuser.nickname
        coin = nowuser.coin
        date = (current_date - nowuser.createdAt.replace(tzinfo=None)).days
        challenge = ""
        bookmark = ""
        c_empty = True
        b_empty = True
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
            'date' : date+1,
            'postcnt' : postcnt,
            'challenge' : challenge,
            'bookmark' : bookmark,
            'c_empty' : c_empty,
            'b_empty' : b_empty,
            'challenge_rate' : challenge_rate,
            'top_percentage' : top_percentage,
            'coin_message' : coin_message
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
        attend_msg = ""
        
        # 해당 주 월~일 날짜 계산
        days_until_monday = (current_date.weekday())  # 월요일까지 남은 일 수
        if days_until_monday == 0:
            week_start = current_date - timedelta(hours=current_date.hour, minutes=current_date.minute, seconds=current_date.second)
        else:
            week_start = current_date - timedelta(days=days_until_monday, hours=current_date.hour, minutes=current_date.minute, seconds=current_date.second)
        week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
    
            
        if request.method == 'POST' and attended == False:
            attend_msg = ""
            att = Attendance(userId=nowuser)
            att.save()
            nowuser.coin += 1
            month_count = len(Attendance.objects.filter(userId = nowuser, attDate__year=year, attDate__month=month))
            if month_count % 7 == 0 and month_count != 0:
                nowuser.coin += 5
                attend_msg = "{month_count}번째 출석으로 5코인 추가 지급!"
            nowuser.save()
            
        # 이미 출석 완료했는지 확인
        if Attendance.objects.filter(userId = nowuser, attDate__year=year, attDate__month=month, attDate__day=day).exists():
            attended = True
        attendances = Attendance.objects.filter(Q(userId = nowuser) & Q(attDate__gte=week_start) & Q(attDate__lte=week_end))
        context = {
            'nickname' : nickname,
            'attendances' : attendances,
            'attended' : attended,
            'attended_msg' : attend_msg
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