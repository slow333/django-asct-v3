from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from users import views as user_views
from blog import views as blog_views
import debug_toolbar

admin.site.site_header = "ASCT 관리자 페이지" # H1 헤더 및 로그인 양식 상단 텍스트
admin.site.site_title = "Automated System Check Tool" # 브라우저 페이지 <title> 태그 접미사
admin.site.index_title = "관리자 대시보드에 오신 것을 환영합니다" 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', user_views.register, name='register'),
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # path('password-reset/', 
    #     auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), 
    #     name='password_reset'),
    # path('password-reset/done/', 
    #     auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
    #     name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>', 
    #     auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
    #     name='password_reset_confirm'),
    # path('password-reset-complete', 
    #     auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
    #     name='password_reset_complete'),
    path('profile/', user_views.profile_view, name='profile'),
    path('', blog_views.index, name='main-home'),
    path('apps/idols/', include('idols.urls')),
    path('apps/blog/', include('blog.urls')),
    path('apps/asct/', include('asct.urls')),
    path('apps/store/', include('store.urls')),
    path('apps/library/', include('library.urls')),
    path('docs/', include('docs.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# '/'를 '/app/library/'로 redirect 함
urlpatterns += [
    path('', RedirectView.as_view(url='/app/library/', permanent=True))
]