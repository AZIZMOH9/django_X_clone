from typing import Any
from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import chat,message
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
# Create your views here.


class ChatsList(ListView,LoginRequiredMixin):
    model = chat
    paginate_by = 10  
    template_name='chat/chat_list.html'
    context_object_name='dict'
    
    def get_queryset(self):
        user1 = self.request.user
        sender=chat.objects.filter(sender=user1)
        reciver=chat.objects.filter(reciver=user1)
        cont=[(i.reciver,i.pk) for i in sender]
        cont1=[(i.sender,i.pk) for i in reciver]
        context=cont1+cont
        
        return context

def messages(Request):
    return render(Request,'blog/massages.html')

class MessagesList(ListView,LoginRequiredMixin,):
    model = chat
    paginate_by = 10  
    template_name='chat/message.html'
    context_object_name='dict'

    def get_context_data(self, **kwargs):
        context = super( MessagesList,self).get_context_data(**kwargs)
        context.update({
            'pk': self.kwargs['pk'],
        })
        return context
    

    def get_queryset(self):
        messages=message.objects.filter(cht_id=self.kwargs['pk'])
        return messages.order_by('date')
    


class SendMessage(CreateView,LoginRequiredMixin):
    model = message
    fields = ['mess']
    template_name='message.html'
    

    def form_valid(self, form):
        form.instance.sender = self.request.user
        chats=chat.objects.get(pk=self.kwargs['pk'])
        if chats.reciver==self.request.user:
            form.instance.reciver = chats.sender
        else:
            form.instance.reciver = chats.reciver
        
        form.instance.chat =  chats
        form.instance.cht_id=self.kwargs['pk']
        return super().form_valid(form)
    

    def get_success_url(self):
        return reverse('chat-view', kwargs={'pk': self.kwargs['pk']})
   



@login_required
def Start_conv(Request,username):
    followed=User.objects.get(username=username)
    follows=Request.user

    
    if chat.objects.filter(sender=follows,reciver=followed).exists():
        chats=chat.objects.get(sender=follows,reciver=followed)
        id=chats.pk
    elif chat.objects.filter(sender=followed,reciver=follows).exists():
        chats=chat.objects.get(sender=followed,reciver=follows)
        id=chats.pk
    else:
        fs=chat(sender=followed,reciver=follows)
        fs.save()
        chats=chat.objects.get(sender=followed,reciver=follows)
        id=fs.pk
        
    return redirect(reverse('chat-view', kwargs={'pk': id}))