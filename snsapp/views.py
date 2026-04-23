from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import Post,Connection


class Home(LoginRequiredMixin, ListView):
   """HOMEページで、自分以外のユーザー投稿をリスト表示"""
   model = Post
   template_name = 'list.html'

   def get_queryset(self):
       #リクエストユーザーのみ除外
       return Post.objects.exclude(user=self.request.user)\
        .select_related('user')\
        .prefetch_related('like')
      
   
class MyPost(LoginRequiredMixin, ListView):
   """自分の投稿のみ表示"""
   model = Post
   template_name = 'list.html'

   def get_queryset(self):
        #自分の投稿に限定
        return Post.objects.filter(user=self.request.user)\
        .select_related('user')\
        .prefetch_related('like')


class DetailPost(LoginRequiredMixin, DetailView):
   """投稿詳細ページ"""
   model = Post
   template_name = 'detail.html'

   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['connection'] = Connection.objects.get_or_create(user=self.request.user)
        return context

class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
   """投稿編集ページ"""
   model = Post
   template_name = 'update.html'
   fields = ['title', 'content']

   def get_success_url(self,  **kwargs):
       """編集完了後の遷移先"""
       pk = self.kwargs["pk"]
       return reverse_lazy('detail', kwargs={"pk": pk})
   
   def test_func(self, **kwargs):
       """アクセスできるユーザーを制限"""
       pk = self.kwargs["pk"]
       post = Post.objects.get(pk=pk)
       return (post.user == self.request.user) 
   
class CreatePost(LoginRequiredMixin, CreateView):
   """投稿フォーム"""
   model = Post
   template_name = 'create.html'
   fields = ['title', 'content']
   success_url = reverse_lazy('mypost')

   def form_valid(self, form):
       """投稿ユーザーをリクエストユーザーと紐付け"""
       form.instance.user = self.request.user
       return super().form_valid(form)


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
   """投稿編集ページ"""
   model = Post
   template_name = 'delete.html'
   success_url = reverse_lazy('mypost')

   def test_func(self, **kwargs):
       """アクセスできるユーザーを制限"""
       pk = self.kwargs["pk"]
       post = Post.objects.get(pk=pk)
       return (post.user == self.request.user) 

###############################################################
#いいね処理
class LikeBase(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)

        liked = False

        if request.user in post.like.all():
            post.like.remove(request.user)
        else:
            post.like.add(request.user)
            liked = True

        return JsonResponse({
            'liked': liked,
            'like_count': post.like.count()
        })
###############################################################


###############################################################
#フォロー処理
class FollowBase(LoginRequiredMixin, View):
    """フォローのベース。リダイレクト先を以降で継承先で設定"""
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        target_user = Post.objects.get(pk=pk).user

        my_connection, created = Connection.objects.get_or_create(user=self.request.user)

        if target_user in my_connection.following.all():
            my_connection.following.remove(target_user)
        else:
            my_connection.following.add(target_user)

class FollowHome(FollowBase):
    """HOMEページでフォローした場合"""
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return redirect('home')

class FollowDetail(FollowBase):
    """詳細ページでフォローした場合"""
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk'] 
        return redirect('detail', pk)
###############################################################


class FollowList(LoginRequiredMixin, ListView):
    """フォローしたユーザーの投稿をリスト表示"""
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        """フォローリスト内にユーザーが含まれている場合のみクエリセット返す"""
        my_connection = Connection.objects.get_or_create(user=self.request.user)
        all_follow = my_connection[0].following.all()
        return Post.objects.filter(user__in=all_follow)\
        .select_related('user')\
        .prefetch_related('like')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['connection'] = Connection.objects.get_or_create(user=self.request.user)
        return context
# Create your views here.
