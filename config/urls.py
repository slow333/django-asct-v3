from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from users import views as user_views
from asct import views as asct_views
import debug_toolbar

admin.site.site_header = "ASCT 관리자 페이지" # H1 헤더 및 로그인 양식 상단 텍스트
admin.site.site_title = "Automated System Check Tool" # 브라우저 페이지 <title> 태그 접미사
admin.site.index_title = "관리자 대시보드에 오신 것을 환영합니다" 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('', asct_views.index, name='main-home'),
    path('apps/idols/', include('idols.urls')),
    path('apps/blog/', include('blog.urls')),
    path('apps/asct/', include('asct.urls')),
    path('apps/store/', include('store.urls')),
    path('apps/library/', include('library.urls')),
    path('apps/polls/', include('polls.urls')),
    path('apps/events/', include('events.urls')),
    path('docs/', include('docs.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# '/'를 '/app/library/'로 redirect 함
# urlpatterns += [
#     path('', RedirectView.as_view(url='/apps/library/', permanent=True))
# ]