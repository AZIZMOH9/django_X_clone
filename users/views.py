from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from blog.models import twitts
from .form import userregisteringform,UpdateProfile,UpdateUser
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import follow


def register(Request):
    if Request.method == 'POST':
        form=userregisteringform(Request.POST)
        if form.is_valid():
            form.save()
            name=form.cleaned_data.get('username')
            messages.success(Request, f'Account created for {name}!')
            return redirect('blog-home')
    else:
        form=userregisteringform()
    return render(Request,'users/register.html',{"form":form})



@login_required
def profile(Request):
    user=Request.user
    followers_=follow.objects.filter(followed=user)
    followerd_=follow.objects.filter(follower=user)
    k= [i.follower for i in followers_]
    e=len(k)
    i=len([i.followed for i in followerd_])
    dict=twitts.objects.filter(name=Request.user)
    paginator = Paginator(dict, 2)  

    page_number = Request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context={'dict':page_obj,'page_obj':page_obj,'e':e,'i':i}
    return render(Request,'users/profile.html',context)





@login_required
def UpdateProfiles(Request):

    if Request.method == 'POST':
        u_from=UpdateUser(Request.POST,instance=Request.user)
        p_from=UpdateProfile(Request.POST,Request.FILES,instance=Request.user.profile)
        if u_from.is_valid() and p_from.is_valid():
            u_from.save()
            p_from.save()
            name=u_from.cleaned_data.get('username')
            messages.success(Request, f'your user information has been updated {name}!')
            return redirect('profile')
    else:
        u_from=UpdateUser(instance=Request.user)
        p_from=UpdateProfile(instance=Request.user.profile)
    return render(Request,'users/profile_edit.html',{"u_form":u_from,"p_from":p_from})


