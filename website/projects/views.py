from django.shortcuts import render
from projects.models import Project

# Create your views here.
def project_index(request):
    projects = Project.objects.all().order_by('title')
    context = {
        'projects': projects
    }
    return render(request, 'project_index.html', context)

def project_detail(request, slug):
    project = Project.objects.get(slug=slug)
    context = {
        'project': project
    }
    return render(request, 'project_detail.html', context)

def project_category(request, category):
    projects = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        "category": category,
        "projects": projects
    }
    return render(request, "blog_category.html", context)