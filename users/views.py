from django.shortcuts import render, get_object_or_404
from .forms import  (
    CustomUserCreationForm, 
    ProfileUpdateForm,
    ProfileImageForm,
    )
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView, 
    View, 
    TemplateView,
    )
from .utilities import send_invitation, send_invitation_accepted
from django.urls import reverse_lazy
from .models import CustomUser, Profile, Team
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
import random
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic.list import MultipleObjectMixin



class CreateUser(SuccessMessageMixin,CreateView):
    form_class = CustomUserCreationForm
    model = CustomUser
    success_url = reverse_lazy("login")
    template_name = 'users/registration.html'
    success_message = "%(email)s был создан!"
    
    
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            email=self.object.email,
        )
        
class ProfileDetailView(DetailView):
    template_name = 'users/profile.html'
    model = Profile
    
    def get_context_data(self, **kwards):
        ctx = super(ProfileDetailView, self).get_context_data(**kwards)
        ctx['target'] = Profile.objects.get(pk=self.kwargs['pk'])
        return ctx
    
class UserTeamView(ListView):
    template_name = 'teams/user-teams.html'
    model = Profile
    paginate_by = 4
    
    def get_context_data(self, **kwards):
        ctx = super(UserTeamView, self).get_context_data(**kwards)
        ctx['target'] = Profile.objects.get(pk=self.kwargs['pk'])
        return ctx
    
    
class TeamDetailView(DetailView):
    template_name = 'teams/team.html'
    model = Team
        
    def get_context_data(self, **kwards):
        ctx = super(TeamDetailView, self).get_context_data(**kwards)
        ctx['team'] = Team.objects.get(pk=self.kwargs['pk'])
        return ctx


class BaseView(ListView):
    model = Team
    template_name = 'users/home.html'
    context_object_name = "target"
    paginate_by = 16


def update_profile(request, user_id):
    users_ind = get_object_or_404(CustomUser, pk=user_id)
    if request.user.is_authenticated and request.user.id == user_id:
        if request.method == "POST":
            profileForm = ProfileUpdateForm(request.POST, instance=request.user.profile)
            imageForm = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
            if profileForm.is_valid() and imageForm.is_valid():
                profileForm.save()
                imageForm.save()
                if profileForm.has_changed() or imageForm.has_changed():
                    messages.success(request, 'Информация обновлена!')
                return redirect('profile', pk=user_id)
        else:
            profileForm = ProfileUpdateForm(instance=request.user.profile)
            imageForm = ProfileImageForm(instance=request.user.profile)
        data = {
            'user': users_ind,
            'profileForm': profileForm,
            'imageForm': imageForm,
        }
    else:
        return redirect('login')
    return render(request, 'users/update_profile.html', data)


def search_results_users(request):
    if request.is_ajax():
        res = None
        game = request.POST.get('game')
        qs = Profile.objects.filter(Q(full_name__icontains=game) | Q(email__icontains=game))
        if len(qs) > 0 and len(game) > 0:
            data = []
            for pos in qs:
                item = {
                    'pk': pos.pk,
                    'img': str(pos.img.url),
                    'full_name': pos.full_name,
                    'email': pos.email
                }
                data.append(item)
            res = data
        else:
            res = 'Не найдено'
        return JsonResponse({'data': res})
    return render(request, 'teams/team_create.html',)


def add_team(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        count_of_players = request.POST.get('count_of_players')
        
        if name and description and count_of_players:
            team = Team.objects.create(name=name, description=description, count_of_players=count_of_players, owner=request.user)
            team.members.add(request.user)
            team.save()
            
            profile = request.user.profile
            profile.active_team_id = team.id
            profile.teams.add(team)
            profile.save()
            
            return redirect('user-teams', profile.id)
    return render(request, 'teams/team_create.html')


def update_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id, members__in=[request.user])
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        count_of_players = request.POST.get('count_of_players')
        if name and description and count_of_players:
            team.name = name
            team.description = description
            team.count_of_players = count_of_players
            team.save()
            messages.success(request, f'Команда {team.name} была успешно обновлена!')
            return redirect('home')
    return render(request, 'users/update_team.html', {'team': team})


# def invite(request):
#     team = get_object_or_404(Team, pk=request.user.profile.active_team_id, members__in=[request.user])
    
#     if request.method == 'POST':
#         email = request.POST.get('email')
        
#         if email:
#             invitations = Invite.objects.filter(team=team, email=email)
            
#             if not invitations:
#                 code = ''.join(random.choice('abcdefghhijklmnopqrstuvwxyz1234567890') for i in range(4))
#                 invitation = Invite.objects.create(team=team, email=email, code=code)
                
#                 messages.info(request, 'Пользователь был приглашен')
                
#                 send_invitation(email, code, team)
                
#                 return redirect('team', team_id=team.id)
#             else:
#                 messages.info(request, 'Пользователь уже приглашён')
#     return render(request, 'users/invite.html', {'team': team})

def password_reset_request(request):
    if request.method == "POST":
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_email = CustomUser.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    subject = 'Запрос на восстановление пароля'
                    email_template_name = 'users/email_message.txt'
                    parameters = {
                        'name' : user.profile.full_name,
                        'email' : user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'TeamFinder',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }   
                    email = render_to_string(email_template_name, parameters)
                    try:
                        send_mail(subject,email, '', [user.email], fail_silently=False)
                    except:
                        return HttpResponse('Invalid Header')
                    return redirect('password_reset_done')
            else:
                messages.error(request, 'Этот email ещё не зарегестрирован!')
    else:
        password_form = PasswordResetForm()
    context = {
        'password_form': password_form,
    }
    return render(request, 'users/pass_reset.html', context)
    

# def create_team(request):
#     if request.method == "POST":
#         teamForm = TeamCreateForm(request.POST, instance=request.user.profile.teams)
#         if teamForm.is_valid():
#             teamForm.save()
#             messages.success(request, 'Команда успешно создана!')
#             return redirect('home')
#     else:
#         teamForm = TeamCreateForm(request.POST)
#         messages.error(request, 'Что-то пошло не так...')
#     data = {
#         'teamForm' : teamForm,
#     }
#     return render(request, 'users/team_create.html', data)




# class CreateTeamView(SuccessMessageMixin, CreateView):
#     model = Team
#     success_url = reverse_lazy("home")
#     template_name = 'users/team_create.html'
#     success_message = "%(name)s был успешно создана!"
#     form_class = TeamCreateForm
    
    
#     def get_context_data(self, **kwards):
#         ctx = super(CreateTeamView, self).get_context_data(**kwards)
#         return ctx
    
#     def get_success_message(self, cleaned_data):
#         return self.success_message % dict(
#             cleaned_data,
#             email=self.object.name,
#         )
        
#     def form_valid(self, form):
#         team = self.kwargs.get('id')
#         form.instance.owner = self.request.user
#         team.members.add(self.request.user)
#         team.save()
#         return super().form_valid(form)
    
        
#     def form_invalid(self, form):
#         messages.add_message(self.request, messages.ERROR, "Ошибка формы")
#         return super().form_invalid(form)
    
