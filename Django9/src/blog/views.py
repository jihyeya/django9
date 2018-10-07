from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Post,PostImage,PostFile
from django.contrib.auth.mixins import LoginRequiredMixin



#제네릭뷰 : 장고에서 제공하는 여러가지 기능을 수행하는 뷰클래스
#class 뷰이름(제네릭뷰 상속):
#상속받은 제네릭뷰클래스의 변수/메소드를 수정해 사용
#단, 해당 제네릭뷰가 어떤 기능을 수행하는지 정확히 알아야함
#어떤 변수/메소드를 사용할 수 있는지 알아야함
#ListView : 특정 객체의 목록을 다루는 기능을 하는 뷰클래스
class Index(ListView):
    #template_name : HTML 경로를 문자열로 저장
    template_name = 'blog/index.html'
    #model         : 모델클래스를 저장
    model = Post
    #context_object_name : 템플릿에 넘겨줄 리스트 이름
    context_object_name = 'post_list'
    #paginate_by : 한페이지에 몇개의 객체가 보여질지 정수값을 저장
    paginate_by = 5

from django.views.generic.detail import DetailView
#DetailView : 특정 모델클래스의 하나의 객체를 템플릿에게 전달할때 사용하는 뷰클래스
class Detail(DetailView):
    template_name = 'blog/detail.html'
    model = Post
    context_object_name = 'obj'
from django.views.generic.edit import FormView
from .forms import PostForm  
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
#FormView : 특정 폼 클래스를 템플릿에게 전달하고 GET/POST을 나눠서 처리할때 사용하는 뷰클래스
#LoginRequiredMixin : 사용자의 로그인 유무를 판별해 비로그인상태의 사용자는 로그인페이지로 변경 
class PostRegister(FormView, LoginRequiredMixin):
    form_class= PostForm  #폼클래스명
    template_name = 'blog/postRegister.html'
    context_object_name = 'form'
    #사용자가 POST방식으로 요청했을때 데이터 유효성을 검사한 뒤 호출되는 메소드
    def form_valid(self, form):
        obj = form.save(commit=False) #Post 객체로 변환
        obj.author = self.request.user#유저정보 채우기
        obj.save()                      #객체를 데이터베이스에 저장
        #사용자가 저장요청한 이미지파일, 파일 객체 생성
        for f in self.request.FILES.getlist('images'):
            image = PostImage(post=obj, image=f)
            image.save()
        #완성한 글의 URL로 이동
        for f in self.request.FILES.getlist('files'):
            image = PostFile(post=obj, file=f)
            image.save()
        return HttpResponseRedirect(reverse('blog:detail', args=(obj.id,)) )
    
    
    
    
    
   #검색 기능 구현
def searchP(request):
    #<input type= "input" name= "quert"/ >
    #GET요청으로 온 데이터에 name이 query인 데이터를 추출 
    #웹요청으로 온 데이터는 무조건 문자열 처리가 됨
    q= request.GET.get('query', '') # query로 데이터가 안 온 경우, 빈문자열 ('')을 반환
    #q에 들어있는 문자열을 포함한 제목을 가진 POst 객체를 검색
    #contains 명령: 해당 변수에 문자열 안에 우변값이 포함되어 있는지 확인
    list =Post.objects.filter(headline__contains=q)
    return render(request,'blog/search.html', { 'List:list'})
    
    
    
    
    
    
    