from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView

def post_list(request):
    posts = Post.published.all()
    return render(request,
	          'blog/list.html',
	          {'posts': posts})

# def post_detail(request, year, month, day, post):
#     post = get_object_or_404(Post, slug=post,
# 			     status='published',
# 			     publish__year=year,
# 			     publish__month=month,
# 			     publish__day=day)
#     return render(request,
# 		  'blog/detail.html',
# 		  {'post': post})


from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post,
							 status='published',
							 publish__year=year,
							 publish__month=month,
							 publish__day=day)

	# Список активных комментариев к этой записи
	comments = post.comments.filter(active=True)
	comments_vote = post.comments.filter(active=True)
	new_comment = None
	if request.method == 'POST':
		# Комментарий был опубликован
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			# Создайте объект Comment, но пока не сохраняйте в базу данных
			new_comment = comment_form.save(commit=False)
			# Назначить текущий пост комментарию
			new_comment.post = post
			# Сохранить комментарий в базе данных
			new_comment.save()
		#print('jjjjjjjjjjjjjjjj',comments.count())
	else:
		comment_form = CommentForm()
	return render(request,
				  'blog/detail.html',
				  {'post': post,
				   'comments': comments,
				   'new_comment': new_comment,
				   'comment_form': comment_form})

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#
# def post_list(request):
# 	object_list = Post.published.all()
# 	paginator = Paginator(object_list, 3)  # 3 поста на каждой странице
# 	page = request.GET.get('page')
# 	try:
# 		posts = paginator.page(page)
# 	except PageNotAnInteger:
# 		# Если страница не является целым числом, поставим первую страницу
# 		posts = paginator.page(1)
# 	except EmptyPage:
# 		# Если страница больше максимальной, доставить последнюю страницу результатов
# 		posts = paginator.page(paginator.num_pages)
# 	return render(request,
# 				  'blog/list.html',
# 				  {'page': page,
# 				   'posts': posts})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/list.html'


from .forms import EmailPostForm


def post_share(request, post_id):
	# Получить пост по id
	post = get_object_or_404(Post, id=post_id, status='published')
	if request.method == 'POST':
		# Форма была отправлена
		form = EmailPostForm(request.POST)
		if form.is_valid():
			# Поля формы прошли проверку
			cd = form.cleaned_data
		# ... отправить письмо
	else:
		form = EmailPostForm()
	return render(request, 'blog/share.html', {'post': post,
													'form': form})


from django.contrib.postgres.search import SearchVector
from .forms import EmailPostForm, CommentForm, SearchForm

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(
                search=SearchVector('title', 'body'),
            ).filter(search=query)
    return render(request,
                  'blog/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})