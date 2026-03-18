from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Project

def project_list(request):
    """Display all projects with pagination"""
    projects_list = Project.objects.all().order_by('-created_at')
    
    # Pagination - show 6 projects per page
    paginator = Paginator(projects_list, 6)
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    
    context = {
        'projects': projects,
        'page_obj': projects,
    }
    return render(request, 'projects/project_list.html', context)

def project_detail(request, project_id):
    """Display single project details"""
    project = get_object_or_404(Project, id=project_id)
    
    # Get related projects (same technology or category)
    related_projects = Project.objects.exclude(id=project_id).filter(
        technologies__icontains=project.technologies.split(',')[0].strip()
    )[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'projects/project_detail.html', context)