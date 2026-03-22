from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Project
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime

def add_project_form(request):
    """Simple form to add projects to database (admin only)"""
    return render(request, 'projects/add_project.html')

@staff_member_required
def save_project(request):
    """Save project to DATABASE"""
    if request.method == 'POST':
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        technologies = request.POST.get('technologies', '')
        url = request.POST.get('url', '')
        github_url = request.POST.get('github_url', '')
        featured = request.POST.get('featured') == 'on'
        
        # Create and save to DATABASE
        project = Project(
            title=title,
            description=description,
            technologies=technologies,
            url=url,
            github_url=github_url,
            featured=featured
        )
        
        # Handle image upload if present
        if 'image' in request.FILES:
            project.image = request.FILES['image']
        
        project.save()
        
        messages.success(request, f'Project "{title}" added successfully to DATABASE!')
        return redirect('project_list')
    
    return redirect('add_project_form')
def project_list(request):
    """Display all projects from database with pagination"""
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
    
    # Get related projects
    tech = project.technologies.split(',')[0].strip() if project.technologies else ''
    related_projects = Project.objects.exclude(id=project_id).filter(
        technologies__icontains=tech
    )[:3] if tech else []
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'projects/project_detail.html', context)