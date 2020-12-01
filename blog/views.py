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

#############################

# from django.db import models
#
#
# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#
#
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)


#
# from django.http import HttpResponseRedirect
# from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
# from django.views import generic
#
# from .models import Choice, Question
#
# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Question.objects.order_by('-pub_date')[:5]
#
#
# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'
#
#
# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/results.html'
#
#
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:  results', args=(question.id,)))