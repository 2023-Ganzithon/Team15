from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import auth
User = get_user_model()

def signup_view(request):
    #GET 요청시 HTML 응답
    if request.method == 'GET':
        return render(request, 'signup.html')
    
    else:
        #POST 요청시 데이터 확인 후 회원 생성
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'],
            )
            
            return redirect('/')#메인페이지로 이동(수정필요)
        return render(request, 'signup.html')#회원가입 실패시
        

def login_view(request):
    if request.method == 'GET':#로그인 HTML응답
        pass
    else:
        pass