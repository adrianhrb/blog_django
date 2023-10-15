from django.shortcuts import get_object_or_404, render

from blog.models import Post


def post_list(request):
    """This view display all the published posts on the blog"""
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, id):
    """This function display a the single post that is requested by the user"""
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    return render(request, 'blog/post/detail.html', {'post': post})
