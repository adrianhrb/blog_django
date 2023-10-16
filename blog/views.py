from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm, SearchForm
from .models import Post

# from django.views.generic import ListView


# class PostListViews(ListView):
#     """Alternative post_list view by using a class, not a function"""
#
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'


def post_list(request: HttpRequest, tag_slug: str = None) -> HttpResponse:
    """This view display all the published posts on the blog"""
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, 'blog/post/list.html', dict(posts=posts, tag=tag))


def post_detail(request: HttpRequest, year: int, month: int, day: int, post: Post) -> HttpResponse:
    """This function display a the single post that is requested by the user"""
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    form = CommentForm()
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by(
        '-same_tags', '-publish'
    )[:4]
    return render(
        request,
        'blog/post/detail.html',
        dict(post=post, comments=comments, form=form, similar_posts=similar_posts),
    )


def post_share(request: HttpRequest, post_id: int) -> HttpResponse:
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # In this step form was submitted
        form = EmailPostForm(data=request.POST)
        if form.is_valid():
            # Form fields passed the validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} recommends you to read {post.title}'
            message = (
                f'Read {post.title} at {post_url}\n\n{cd["name"]}\'s comments: {cd["comments"]}'
            )
            send_mail(subject, message, 'adrian.herrera.br@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', dict(post=post, form=form, sent=sent))


@require_POST
def post_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request, 'blog/post/comment.html', dict(post=post, comment=comment, form=form))


def post_search(request: HttpRequest) -> HttpResponse:
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = (
                Post.published.annotate(similarity=TrigramSimilarity('title', query))
                .filter(similarity__gt=0.1)
                .order_by('-similarity')
            )

    return render(request, 'blog/post/search.html', dict(form=form, query=query, results=results))
