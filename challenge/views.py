from django.shortcuts import render,redirect
from django.utils import timezone
import random
from .models import challenge, OngoingChallenge
from datetime import datetime
from user.models import CustomUser
#챌린지 홈 + 주제 선택


def challenge_home(request):
    
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    day = current_date.day
    user=request.user
    clist=challenge.objects.all()
    if OngoingChallenge.objects.filter(userId = user, cDate__year=year, cDate__month=month, cDate__day=day).exists():
        new= OngoingChallenge.objects.filter(userId=user, cDate__year=year, cDate__month=month, cDate__day=day).last()
        newid=new.id
        if OngoingChallenge.objects.filter(pk=newid, cImage ='').exists():
            pass
        else:
            return redirect('challenge:challenge_detail',Id=new.id)
        
            
        
        
        
    else:
        cname= random.choice(clist)
        context={"cId": cname}
        
        new= OngoingChallenge.objects.create(
            userId=request.user,
            cId = cname,
        )
        newid=new.id   
    update=OngoingChallenge.objects.get(pk=newid)
    
    cname=update.cId
    id=update.id
    context={"cId": cname,"id": id}

    if request.method == 'GET':#html응답
        return render(request, 'challenge_home.html', context)
    else:#post 재선택
        cSelect = request.user
        if(cSelect.cSelect>0):
            
            cname= random.choice(clist)
            cSelect.cSelect -=1
            cSelect.save()
            context={"cId":cname,"id":id}
            
            update.cId = cname
            update.save()
        return render(request, 'challenge_home.html', context)


#챌린지 사진 업로드
def challenge_upload(request, Id):
    user = request.user
    global cname
    upload= OngoingChallenge.objects.get(pk=Id)
    context={"cId":upload.cId,"id":upload.id}
    
    # 생성 폼
    if request.method == 'GET':
        return render(request, 'challenge_upload.html',context)

    if request.method == 'POST':
        #아마 주제도 포함
        image = request.FILES.get('cImage')
        
        upload.cDate=timezone.now()
        upload.cImage=image
         
        upload.save()

        return redirect('challenge:challenge_detail',Id=upload.id)

    return render(request, 'challenge_upload.html')


#챌린지 사진 업로드 후 확인
def challenge_detail(request, Id):
    chall=OngoingChallenge.objects.get(pk=Id)
    user = request.user
    
    if request.method == 'POST' and chall.cCheck == True and chall.uCheck == False:
        check=True
        chall.uCheck=True
        chall.save()
        user.coin+=1
        user.save()
    context = {
        "cImage": chall.cImage,
        "cDate": chall.cDate,
        "cCheck": chall.cCheck,
        "cId": chall.cId,
        "userId":chall.userId,
        "check":chall.uCheck,
        
    }

    return render(request, "challenge_detail.html", context)
