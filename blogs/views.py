from django.views.generic import ListView

from django.shortcuts import render

from blogs.models import Blog, BlogStatus, Category, Tag




class BlogListView(ListView):
    model = Blog
    template_name = 'blogs/blogs-list.html'
    context_object_name = 'blogs'
    paginate_by = 6

    def get_queryset(self):
        return Blog.objects.filter(status=BlogStatus.PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent=None)
        context['tags'] = Tag.objects.all()
        context['recent_posts'] = Blog.objects.filter(status=BlogStatus.PUBLISHED)
        return context



class BlogDetailView(ListView):
    model = Blog
    template_name = 'blogs/blog-detail.html'
    context_object_name = 'blog'

    def get_queryset(self):
        return Blog.objects.filter(id=self.kwargs['pk'], status=BlogStatus.PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_queryset().first()
        context['categories'] = Category.objects.filter(parent=None)
        context['tags'] = Tag.objects.all()
        context['recent_posts'] = Blog.objects.order_by('-created_at')[:2]
        context['related_news'] = Blog.objects.filter(categories__in=blog.categories.values_list('id', flat=True)).exclude(
            id=blog.id).distinct()[:3]
        return context