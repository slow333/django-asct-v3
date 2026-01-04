from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class LoginView(generic.View):
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, f'로그인 했습니다.({username})')
            return redirect('main-home')
        else:
            messages.info(request, ('id와 password를 확인해주세요.'))
            return redirect('users:login')

class LogoutView(generic.View):
    def post(self, request, *args, **kwargs):
        auth.logout(request)
        return redirect('todos:index')
    
# class UserEditView(generic.UpdateView, LoginRequiredMixin):
#     # form_class = UserChangeForm
#     template_name = 'users/edit-profile.html'
#     success_url = reverse_lazy('blog:index')

#     def get_object(self):
#         return self.request.user
#     def get(self, request, *args, **kwargs):
#         u_form = UserChangeForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile, request.FILES, request.POST) # type: ignore
#         context = {
#             'u_form': u_form,
#             'p_form': p_form,
#         }
#         return render(request, self.template_name, context)

class UserRegisterView(generic.CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

class UserEditView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'users/edit-profile.html'
    
    # def get_object(self):
    #     return self.request.user
    
    def get(self, request, *args, **kwargs):
        u_form = UserUpdateForm(instance=request.user) # type: ignore
        # u_form = UserChangeForm(instance=request.user) # 전체를 보여줌
        p_form = ProfileUpdateForm(instance=request.user.profile) # type: ignore
        context = {
            'u_form': u_form,
            'p_form': p_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user) # type: ignore
        # u_form = UserChangeForm(request.POST, instance=request.user) # 전체를 보여줌
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) # type: ignore
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile이 업데이트 되었습니다.')
            return redirect('users:edit-profile')
        
        context = {
            'u_form': u_form,
            'p_form': p_form,
        }
        return render(request, self.template_name, context)
