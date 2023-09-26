from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Blog
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import linebreaksbr
from .forms import BlogForm
from django.db.models import Q
from django.db.models.functions import Lower
from django.utils.text import slugify
from datetime import datetime


def all_blogs(request):
    blogs = Blog.objects.all()
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('blogs'))

        queries = Q(title__icontains=query) | Q(content__icontains=query)
        blogs = blogs.filter(queries)

    context = {
        'blogs': blogs,
        'search_term': query,
    }
    template = 'blog/blogs.html'

    return render(request, template, context)


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    content_paragraphs = linebreaksbr(blog.content).split('<br>')

    content_paragraphs = [p.strip() for p in content_paragraphs if p.strip()]

    context = {
        'blog': blog,
        'content_paragraphs': content_paragraphs,
    }
    template = 'blog/blog_detail.html'
    return render(request, template, context)


@login_required
def delete_blog(request, slug):
    """delete a blog"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can do that.')
        return redirect(reverse('home'))

    blog = get_object_or_404(Blog, slug=slug)
    blog.delete()

    messages.success(request, 'Blog post deleted.')
    return redirect(reverse('blogs'))


@login_required
def add_blog(request):
    """Add a blog post"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, initial={'author': request.user})
        if form.is_valid():
            blog = form.save(commit=False)
            blog.slug = slugify(blog.title)
            blog.blog_time = datetime.now().time()
            blog.author = request.user
            blog.save()
            messages.success(request, 'Successfully added blog post!')
            return redirect(reverse('blog_detail', kwargs={'slug': blog.slug}))
        else:
            messages.error(request, 'Failed to add Blog post. Please ensure the form is valid.')
    else:
        form = BlogForm(initial={'author': request.user})

    template = 'blog/add_blog.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_blog(request, slug):
    """Edit a blog post"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can do that.')
        return redirect(reverse('home'))

    blog = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post edited successfully.')
            return redirect(reverse('blog_detail', args=[slug]))
        else:
            messages.error(request, 'Failed to edit Blog post. Please ensure the form is valid.')
    else:
        form = BlogForm(instance=blog)
        messages.info(request, f'You are editing { blog.title }')

    template = 'blog/edit_blog.html'
    context = {
        'form': form,
        'blog': blog,
    }

    return render(request, template, context)
