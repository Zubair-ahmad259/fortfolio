from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Project
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
import os
import json

def add_project_form(request):
    """Simple form to add projects (admin only)"""
    return render(request, 'projects/add_project.html')

@staff_member_required
def save_project(request):
    """Save project to file (no database)"""
    if request.method == 'POST':
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        technologies = request.POST.get('technologies', '')
        url = request.POST.get('url', '')
        github_url = request.POST.get('github_url', '')
        
        # Create projects directory if it doesn't exist
        projects_dir = 'projects_data'
        if not os.path.exists(projects_dir):
            os.makedirs(projects_dir)
        
        # Save to JSON file
        project_data = {
            'id': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'title': title,
            'description': description,
            'technologies': technologies,
            'url': url,
            'github_url': github_url,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'featured': request.POST.get('featured') == 'on'
        }
        
        # Read existing projects
        all_projects_file = 'all_projects.json'
        if os.path.exists(all_projects_file):
            with open(all_projects_file, 'r', encoding='utf-8') as f:
                all_projects = json.load(f)
        else:
            all_projects = []
        
        # Add new project
        all_projects.append(project_data)
        
        # Save back
        with open(all_projects_file, 'w', encoding='utf-8') as f:
            json.dump(all_projects, f, indent=2, ensure_ascii=False)
        
        messages.success(request, f'Project "{title}" added successfully!')
        return redirect('add_project_form')
    
    return redirect('add_project_form')

def get_all_projects():
    """Helper function to get all projects from file"""
    all_projects_file = 'all_projects.json'
    if os.path.exists(all_projects_file):
        with open(all_projects_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

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