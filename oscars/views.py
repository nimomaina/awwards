from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,Http404
from .forms import *
from .models import *




def home(request):
    screenshots = Project.objects.all()
    current_user = request.user
    return render(request, 'home.html',locals())

@login_required(login_url='/accounts/login/')
def upload_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            add=form.save(commit=False)
            add.save()
            return redirect('home')
    else:
        form = ProjectForm()


    return render(request,'upload_project.html',locals())


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


def edit(request):
    profile = User.objects.get(username=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('update_profile')
    else:
        form = ProfileForm()
    return render(request, 'edit_profile.html', locals())

def search_results(request):
    profile= Profile.objects.all()
    project= Project.objects.all()
    if 'Project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        searched_project = Project.search_by_profile(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',locals())

    else:
        message = "You haven't searched for any term"
        return render(request,'search.html',{"message":message})

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
    return render(request,'vote.html',locals())



def Vote(request):
    profile = User.objects.get(username=request.user)
    return render(request,'vote.html',locals())

def view_vote(request,project_id):
    user = User.objects.get(username=request.user)
    project = Project.objects.get(pk=project_id)
    vote = Votes.objects.filter(project_id=project_id)
    print(vote)
    return render(request,'project.html',locals())



@login_required(login_url='/accounts/login/')
def vote(request,project_id):

   project = Project.objects.get(pk=project_id)
   vote = Votes.objects.filter(project_id=project_id).all()
   print([r.project_id for r in vote])
   rateform = VotesForm()

   return render(request,"projects.html", locals())






