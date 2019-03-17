from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,Http404
from .forms import *
from .models import *



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def home(request):
    screenshots = Project.objects.all()
    return render(request, 'home.html',{"screenshots":screenshots})


def add_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            add=form.save(commit=False)
            add.save()
            return redirect('home')
    else:
        form = ProjectForm()


    return render(request,'project.html',locals())


@login_required(login_url='/accounts/login/')
def profile(request, username):
    projo = Project.objects.all()
    profile = User.objects.get(username=username)
    # print(profile.id)
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    projo = Project.get_profile_projects(profile.id)
    title = f'@{profile.username} awwward projects and screenshots'

    return render(request, 'profile.html', locals())


@login_required(login_url='/accounts/login/')
def edit(request):
    profile = User.objects.get(username=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('edit_profile')
    else:
        form = ProfileForm()
    return render(request, 'edit_profile.html', locals())



@login_required(login_url='/accounts/login')
def vote_project(request,project_id):
    project = Project.objects.get(pk=project_id)
    profile = User.objects.get(username=request.user)
    if request.method == 'POST':
        voteform = VotesForm(request.POST, request.FILES)
        print(voteform.errors)
        if voteform.is_valid():
            rating = voteform.save(commit=False)
            rating.project = project
            rating.user = request.user
            rating.save()
            return redirect('vote',project_id)
    else:
        voteform = VotesForm()
    return render(request,'votes.html',locals())








