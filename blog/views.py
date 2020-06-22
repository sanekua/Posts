from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from .models import Post
from django.contrib.postgres.search import SearchVector
from .forms import EmailPostForm, CommentForm, SearchForm


def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post,
							 status='published',
							 publish__year=year,
							 publish__month=month,
							 publish__day=day)

	comments = post.comments.filter(active=True)
	new_comment = None
	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.save()
	else:
		comment_form = CommentForm()
	return render(request, 'blog/detail.html',{
		'post': post,
		'comments': comments,
		'new_comment': new_comment,
		'comment_form': comment_form
	})


class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 6
	template_name = 'blog/list.html'


def post_share(request, post_id):
	post = get_object_or_404(Post, id=post_id, status='published')
	if request.method == 'POST':
		form = EmailPostForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
	else:
		form = EmailPostForm()
	return render(request, 'blog/share.html', {'post': post, 'form': form})


def post_search(request):
	form = SearchForm()
	query = None
	results = []
	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data['query']
			results = Post.objects.annotate(search=SearchVector('title', 'body'),).filter(search=query)
	return render(request, 'blog/search.html', {'form': form, 'query': query, 'results': results})


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'slug', 'author', 'publish', 'status', 'link', 'body']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
