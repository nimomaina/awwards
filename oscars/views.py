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

    profile = User.objects.get(username=username)
    print(profile.id)
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    user = request.user
    profile = User.objects.get(username=username)
    project = Project.get_by_id(profile.id)
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
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search')
        searched_project = Project.search_by_project(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',locals())

    else:
        message = "You haven't searched for any term"
        return render(request,'search.html',{"message":message})


def project(request, project_id):
    try:
        project = Project.objects.get(id = project_id)
    except DoesNotExist:
        raise Http404()
    return render(request,"project.html", {"project":project})



# def vote_project(request,project_id):
#     new_votes = Votes.objects.all().filter(project_id=project.id)
#
#     if request.method == 'POST':
#         form = VotesForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.project = project
#             review.user = request.user
#             review.save()
#
#     else:
#         form = VotesForm()
#
#     return render(request, 'vote.html',locals())
#
#





