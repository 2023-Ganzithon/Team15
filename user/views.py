from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model,login,logout
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
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
                
            return redirect('test')#메인페이지로 이동(수정필요)
        return render(request, 'signup.html',{'error': '회원가입 실패'})#회원가입 실패시
        

def login_view(request):
    if request.method == 'GET':#로그인 HTML응답
        return render(request, 'login.html')
    else:#POST
        form =AuthenticationForm(request, request.POST)
        if form.is_valid():#로그인 인증 성공
            login(request, form.user_cache)
            return redirect('test')#메인 페이지로 이동(수정필요)
        else:#로그인 실패
           return render(request, 'login.html', {'error': 'username or password is incorrect.'})
        
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('test')#메인페이지로 이동(수정필요)

def test_view(request):
    return render(request, 'test.html')