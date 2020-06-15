from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .forms import EmailPostForm

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post


def home(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 2) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
   
    context = {
        'page_number': page,
        'page_obj': posts
    }
   
    return render(request, 'blog/home.html', context)

    """
        We Chainge this way to anther way allow us to use query manger.

        tis is old way.
   
        class PostListView(ListView):
            model = Post
            template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
            context_object_name = 'posts'
            ordering = ['-date_posted']
            paginate_by = 5

    """



class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                    status='published',
                                    date_posted__year=year,
                                    date_posted__month=month,
                                    date_posted__day=day)
    context = {
        'object': post
    }
    return render(request, 'blog/post_detail.html', context)

"""
    we test anther way herer

class PostDetailView(DetailView):
    model = Post

"""

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def post_share(request, slug):
    # Retrieve post by id
    post = get_object_or_404(Post, slug=slug, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
            post.get_absolute_url())
            subject = f"{cd['name']} recommends you read "f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n"f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post': post, 'form': form, 'sent': sent})


