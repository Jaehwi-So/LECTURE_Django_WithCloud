# 앱 설정 및 세팅
### 가상환경 구축 및 세팅
pip install django
django-admin startproject my_django_project
### 데이터베이스 초기설정
python manage.py migrate - 초기 db.sqlite3이 생성됨
python manage.py createsuperuser - 관리자 계정 생성
### 앱 만들기
python manage.py startapp blog
- settings.py에 App을 추가해주어야 함
### 데이터베이스 마이그레이션
python manage.py makemigrates
python manage.py migrate

# 기본적인 모델 설정
### 1. 모델 생성
```
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField()
```
### 2. 마이그레이팅
- python manage.py makemigrations
- python manage.py migrate
### 3. admin.py 모델 등록
- admin.py에 등록
- admin.site.register(Post)
### 4. URL과 View 연결하기
1. URL에 사용할 패턴과 views.py의 메서드 연결
2. views.py에서 사용할 템플릿과 연결

# models.py : 모델 정의하기
### 1. DateTime 자동 저장
```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```
### 2. Model의 대표값 설정
- __str__을 오버라이딩하여 객체의 대표가 될 내용 설정
### 3. Model의 메서드 추가
- get_absolute_url을 생성해 상세보기 페이지로 이동하는 URL 설정
- 사용하려는 메서드를 모델에 넣으면 View에서 사용 가능
### 4. 이미지 업로드 컬럼 추가
- settings.py와 urls.py에 MEDIA_URL 설정 필요
- 이미지 업로드 컬럼 추가
```python
head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
```
- 파일 업로드 컬럼 추가
```python
file_upload = models.FileField(upload_to='blog/images/%Y/%m/%d/', blank=True)
```
- 업로드 파일 속성
  * file_upload.name : 파일명
  * file_upload.url : 파일경로
### 5. Slug 필드 추가
- 숫자인 pk 대신 읽을 수 있는 텍스트로 URL을 구성할 때 사용
```html
models.SlugField(max_length=2000, unique=True, allow_unicode=True)
```
### 6. 각종 속성
- blank=True : 해당 필드를 작성하지 않아도 됨(폼에서 비어있어도 됨), 유효성 검사때 사용
- null=True : Nullable 허용
- unique=True : Unique 속성
- on_delete=models.CASCADE : 연관 레코드가 삭제될 때 함께 삭제
- on_delete=models.SET_NULL : 연관 레코드가 삭제될 때 해당 필드를 NULL로 설정
- allow_unicode=True : Slug 필드에서의 한글 URL 유니코드 허용
### 7. CBV 컨텍스트에 데이터 담아서 보내기
```python
def get_context_data(self, **kwargs):
    context = super(PostList, self).get_context_data()
    context['categories'] = Category.objects.all()
    context['no_category_post_count'] = Post.objects.filter(category=None).count()
    return context
```
### 8. 관계 설정
```python
    # N:1 관계연결
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    # N:M 관계연결
    tags = models.ManyToManyField(Tag, blank=True)   # null=True를 설정필요없음
```

# urls.py
### 1. URL 패턴
```python
urlpatterns = [
    path('', views.index),
    path('<int:pk>', views.post_detail)
]
```
### 2. MEDIA URL(파일업로드)와 Static Path 연결하기
```html
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

# views.py
### 1. FBV
   - MYMODEL.objects.all() : Table의 모든 값 선택
   - .order_by('-pk') : PK DESC 정렬, -는 역순
   - render : 템플릿과 컨텍스트로 넘겨줄 값 설정
```python
def post_list(request):
    posts = Post.objects.all().order_by('-pk')
    return render(
        request,
        'blog/post_list.html',
        {
            'posts': posts
        }
    )
```
### 2. CBV
- ListView, DetailView, CreateView, UpdateView
```python
class PostList(ListView):
    model = Post
    ordering = '-pk'

    # render시 아래의 별도 설정이 없을 시 경로는 post_list.html, 모델은 자동으로 post_list로 할당됨
    template_name = 'blog/post_list.html'   #템플릿 설정
```
### 3. Model Query
- SELECT ONE : Tag.objects.get(slug = slug)
- SELECT LIST : Post.objects.filter(category = category)
- 연관되어 있는 셋 조회 : post_list = tag.post_set.all()
### 4. 인증 미들웨어
- class PostCreate(LoginRequiredMixin, CreateView):
### 5. form_valied
- POST 요청에서 유효한 폼이 제공되면 데이터를 확인 및 처리하여 결과 반환
```python
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog')
```
### 6. dispatch
- 요청이 처리되기 전에 호출되는 메서드. HTTP 메서드에 따라 적절한 메서드 호출\
- 인증 및 권한 관리와 같은 전처리 작업을 수행함
```python
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
```
### 7. request
- request.method :Request Method
- request.POST : Form에 입력한 데이터를 담고있는 POST 요청객체
- request.user : 세션의 사용자
  * is_authenticated : 인증이 되었는가?
  * is_superadmin, is_staff : 권한이 ~인가?

# Settings.py
### 1. Timezone 설정
- TIME_ZONE = 'Asia/Seoul'
- USE_TZ = False
### 2. Static File path 설정
- STATIC_URL = "static/"
### 3. 업로드 이미지 관리 및 Path 설정
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '_media')

# admin.py 
- 관리자 페이지 설정
### 1. 모델 등록
```html
admin.site.register(Post)
```
### 2. 모델 생성 시 자동완성
```html
class AutoSlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, AutoSlugAdmin)
```

# form.py
### 1. 사용할 폼 클래스 생성
```python
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)   #입력
```

# 템플릿 문법
### 1. for
```html
{% for p in post_list %}
 <p class="card-text">{{ p.content }}</p>
{% endfor %}
```
### 2. static path
```html
{% load static %}
//...
<img src="{% static 'images/lena.jpg' %}">
```
### 3. 템플릿 필터
```html
첫 100개 문자 <p class="card-text">{{ p.content | truncatechars:100}}</p>
첫 45개 단어 <p class="card-text">{{ p.content | truncatewords:45}}</p>
```
### 4. 템플릿 모듈화

- 부모 템플릿 상속
```html
{% extends 'blog/base.html' %}
```

- 블록 영역 구분(부모 자식 모두)
```html
{% block main_area %}

{% endblock %}
```

- 다른 템플릿 포함
```html
{% include 'blog/navbar.html' %}
```