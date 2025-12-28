from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect

from .models import Post
from .filters import PostFilter
from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'posts'
    filterset_class = PostFilter
    ordering = ['-dateCreation']
    paginate_by = 10
   
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class BasePostView(LoginRequiredMixin, PermissionRequiredMixin):
    model = Post
    form_class = PostForm
    permission_required = []
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NewsCreateView(BasePostView, CreateView):
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post', kwargs={'pk': self.object.pk})


class ArticleCreateView(BasePostView, CreateView):
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',)
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post', kwargs={'pk': self.object.pk})


class PostUpdateView(BasePostView, UpdateView):
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)
    
    def get_success_url(self):
        return reverse_lazy('post', kwargs={'pk': self.object.pk})


class PostDeleteView(BasePostView, DeleteView):
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.delete_post',)

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs['pk'])
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect('news_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        
        if context['object'].categoryType == 'NW':
            context['content_type'] = 'новость'
        else:
            context['content_type'] = 'статья'
        
        return context
