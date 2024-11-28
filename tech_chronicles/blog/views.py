#!/usr/bin/env python3
""" blog views """
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST


def post_list(request):
    """ Returns all published posts """
    post_list = Post.published.all()

    # pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer, get the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page_number is out of range, get the last page
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    """ Returns a specific post based on post id """
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post, publish__year=year,
                             publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()

    return render(request, 'blog/post/detail.html',
                  {'post': post, 'comments': comments,'form': form})


def post_share(request, post_id):
    """ Share posts through emails """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
        post_url = request.build_absolute_uri(post.get_absolute_url())
        subject = (f"{cd['name']} ({cd['email']}) "
                   f"recommends you read {post.title}")
        message = (f"Read {post.title} at {post_url}\n\n"
                   f"{cd['name']}\'s comments: {cd['comments']}")
        send_mail(subject=subject, message=message, from_email=None,
                  recipient_list=[cd['to']])
        sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html',
                  {'post': post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
    """ Handles comments on blog posts """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # a comment was posted
    form = CommentForm(data=request.POST)

    if form.is_valid():
        # create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # assign the post to the comment
        comment.post = post
        # save the comment to the database
        comment.save()
    
    return render(request, 'blog/post/comment.html',
                  {'post': post, 'form': form, 'comment': comment})


class PostListView(ListView):
    """ Alternative post list view """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
