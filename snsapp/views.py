from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import Post, Follow



class Home(LoginRequiredMixin, ListView):
   """HOMEページで、自分以外のユーザー投稿をリスト表示"""
   model = Post
   template_name = 'list.html'

   def get_queryset(self):
       #リクエストユーザーのみ除外
       return Post.objects.exclude(user=self.request.user)\
        .select_related('user')\
        .prefetch_related('like')
   
   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['following_users'] = Follow.objects.filter(
        follower=self.request.user
    ).values_list('following', flat=True)
    return context
      
   
class MyPost(LoginRequiredMixin, ListView):
   """自分の投稿のみ表示"""
   model = Post
   template_name = 'list.html'

   def get_queryset(self):
        #自分の投稿に限定
        return Post.objects.filter(user=self.request.user)\
        .select_related('user')\
        .prefetch_related('like')
   
   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['following_users'] = Follow.objects.filter(
        follower=self.request.user
    ).values_list('following', flat=True)
    return context


class DetailPost(LoginRequiredMixin, DetailView):
   """投稿詳細ページ"""
   model = Post
   template_name = 'detail.html'

   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['following_users'] = Follow.objects.filter(
        follower=self.request.user
    ).values_list('following', flat=True)
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
    def post(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']

        # フォロー対象ユーザー取得
        target_user = get_object_or_404(User, pk=user_id)

        # 自分自身はフォローできない
        if target_user == request.user:
            return JsonResponse({'error': 'cannot follow yourself'}, status=400)

        # 自分のフォロー情報取得
        

        followed = False

        # フォロー切り替え
        follow = Follow.objects.filter(
            follower=request.user,
            following=target_user
        )
        if follow.exists():
            follow.delete()
            followed = False
        else:
            Follow.objects.create(
                follower=request.user,
                following=target_user
            )
            followed = True

        return JsonResponse({
            'followed': followed
        })
    

class FollowToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        target_user = get_object_or_404(User, pk=self.kwargs['pk'])

        if target_user == request.user:
            return JsonResponse({'error': 'cannot follow yourself'}, status=400)

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user
        )

        if not created:
            follow.delete()
            followed = False
        else:
            followed = True

        return JsonResponse({
            'followed': followed
        })

###############################################################


class FollowList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        following_users = Follow.objects.filter(
            follower=self.request.user
        ).values_list('following', flat=True)

        return Post.objects.filter(
            user__in=following_users
        ).select_related('user').prefetch_related('like')
# Create your views here.
