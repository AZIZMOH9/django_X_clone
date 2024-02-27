from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import twitts
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from users.models import follow
# Create your views here.



#################################################
def say_hello(Request):
    return render(Request,'blog/home.html',{"dict":twitts.objects.all()})



def messages(Request):
    return render(Request,'blog/massages.html')


#################################################
class TwittsList(ListView):
    model = twitts
    paginate_by = 4  
    template_name='blog/home.html'
    context_object_name='dict'
    ordering = ['-date']

    

    def get_queryset(self):
        user = self.request.user
        followedss=follow.objects.filter(follower=user)
        i=[i.followed for i in followedss]
        context=[]
        for k in i:
            context.append(twitts.objects.filter(name=k))

        
        return [item for sublist in context for item in sublist]
    


class TwittsDetail(DetailView):
    model = twitts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context




class UserPostListView(ListView):
    model = twitts
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'dict'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        user1=get_object_or_404(User, username=self.kwargs.get('username'))
        followers_=follow.objects.filter(followed=user1)
        followerd_=follow.objects.filter(follower=user1)
        k= [i.follower for i in followers_]
        e=len(k)
        i=len([i.followed for i in followerd_])
        context.update({
            'user1': user1,
            'k':k,
            'e':e,
            'i':i
        })
        return context
    

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        
        return twitts.objects.filter(name=user).order_by('-date')
    
def view_flls(Request,username):
    person=User.objects.get(username=username)
    followingssss=follow.objects.filter(follower=person)
    k=[i.followed for i in followingssss]
    
    
    return render(Request,'blog/view_followes.html',{'follows':k})

def view_fllss(Request,username):
    person=User.objects.get(username=username)
    followingssss=follow.objects.filter(followed=person)
    k=[i.follower for i in followingssss]
    
    
    return render(Request,'blog/view_followed.html',{'follows':k})

@login_required
def follows(Request,username):
    followed=User.objects.get(username=username)
    follows=Request.user

    if Request.method == "POST":
        action = Request.POST['follow']
        if action == "unfollow":
            fs=follow.objects.get(follower=follows,followed=followed)
            fs.delete()
        elif action == "follow":
            fs=follow(follower=follows,followed=followed)
            fs.save()
        
        return redirect(Request.META.get('HTTP_REFERER', '/'))
    
    



class CreateTwitt(LoginRequiredMixin,CreateView):

    model = twitts
    fields = ['twitt']
    def form_valid(self, form):
        form.instance.name = self.request.user
        return super().form_valid(form)
    

class UpdateTwitt(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = twitts
    fields = ['twitt']

    def form_valid(self, form):
        form.instance.name = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.name:
            return True
        return False
    

class DeleteTwitt(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = twitts
    success_url = '/blog'
    def form_valid(self, form):
        post = self.get_object()
        post.name = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.name:
            return True
        return False
    

def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        
        data=User.objects.filter(username=q)
    else:
        data = User.objects.all()
    context = {
        'data': data
    }
    return render(request, 'blog/search.html', context)


    