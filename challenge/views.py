from django.shortcuts import render,redirect
from django.utils import timezone
import random
from .models import challenge, OngoingChallenge
from user.models import CustomUser
#챌린지 홈 + 주제 선택
first = 1

def challenge_home(request):
    global first
    user=request.user
    clist=challenge.objects.all()
    
    if first == 1:
        cname= random.choice(clist)
        context={"cId": cname}
        first=0
        OngoingChallenge.objects.create(
            userId=request.user,
            cId = cname,
        )   
    update= OngoingChallenge.objects.last()
    cname=update.cId
    context={"cId": cname}

    if request.method == 'GET':#html응답
        return render(request, 'challenge_home.html', context)
    else:#post
        cSelect = request.user
        if(cSelect.cSelect>0):
            cname= random.choice(clist)
            cSelect.cSelect -=1
            cSelect.save()
            context={"cId":cname}
            update= OngoingChallenge.objects.last()
            update.cId = cname
            update.save()
        return render(request, 'challenge_home.html', context)


#챌린지 사진 업로드
def challenge_upload(request):
    user = request.user
    global cname
    upload= OngoingChallenge.objects.last()
    context={"cId":upload.cId}
    
    # 생성 폼
    if request.method == 'GET':
        return render(request, 'challenge_upload.html',context)

    if request.method == 'POST':
        #아마 주제도 포함
        image = request.FILES.get('cImage')
        
        upload.cDate=timezone.now()
        upload.cImage=image
         
        upload.save()

        return redirect('challenge:challenge_detail')

    return render(request, 'challenge_upload.html')


#챌린지 사진 업로드 후 확인
def challenge_detail(request, cId):
    chall=OngoingChallenge.objects.get(pk=cId)

    context = {
        "cImage": chall.cImage,
        "cDate": chall.cDate,
        "cCheck": chall.cCheck,
        "cId": chall.cId,
        "userId":chall.userId,
    }

    return render(request, "challenge_detail.html", context)
