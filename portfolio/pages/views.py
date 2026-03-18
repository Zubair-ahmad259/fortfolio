from django.shortcuts import render, redirect
from django.contrib import messages
from projects.models import Project
from datetime import datetime
import os

def home(request):
    """Home page view"""
    featured_projects = Project.objects.filter(featured=True)[:3]
    context = {
        'projects': featured_projects,
        'name': 'Zubair Ahmad',
        'title': 'Python Developer & Django Enthusiast',
    }
    return render(request, 'home.html', context)

def about(request):
    """About page view"""
    context = {
        'name': 'Zubair Ahmad',
        'title': 'Python Developer & Django Enthusiast',
        'email': 'zubair@zephyr.dev',
        'bio': "I'm a passionate Python Developer with over 3 years of experience in building web applications. I specialize in Django and modern web technologies, creating solutions that are not only functional but also elegant and user-friendly.",
        'skills': ['Python', 'Django', 'JavaScript', 'HTML5', 'CSS3', 'PostgreSQL', 'Git', 'Docker', 'AWS'],
        'hobbies': ['Reading Tech Blogs', 'Open Source', 'Traveling', 'Photography', 'Music'],
        'experience': [
            {
                'position': 'Senior Python Developer',
                'company': 'Tech Innovations Inc.',
                'years': '2023 - Present',
                'description': 'Leading development of scalable web applications using Django.'
            },
            {
                'position': 'Django Developer',
                'company': 'Digital Solutions Ltd.',
                'years': '2021 - 2023',
                'description': 'Developed and maintained Django web applications.'
            },
            {
                'position': 'Junior Web Developer',
                'company': 'StartUp Hub',
                'years': '2020 - 2021',
                'description': 'Built responsive websites.'
            }
        ],
        'education': [
            {
                'degree': 'B.Sc. in Computer Science',
                'school': 'University of Technology',
                'year': '2020'
            }
        ]
    }
    return render(request, 'about.html', context)

def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        # Save to text file (works immediately, no email setup needed)
        try:
            # Create submissions directory if it doesn't exist
            submissions_dir = 'contact_submissions'
            if not os.path.exists(submissions_dir):
                os.makedirs(submissions_dir)
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'{submissions_dir}/contact_{timestamp}.txt'
            
            # Save the data
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"CONTACT FORM SUBMISSION\n")
                f.write(f"{'='*50}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Name: {name}\n")
                f.write(f"Email: {email}\n")
                f.write(f"Phone: {phone}\n")
                f.write(f"Subject: {subject}\n")
                f.write(f"{'='*50}\n")
                f.write(f"Message:\n{message}\n")
                f.write(f"{'='*50}\n")
            
            # Also append to a single file for easy viewing
            with open('all_contacts.txt', 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Name: {name}\n")
                f.write(f"Email: {email}\n")
                f.write(f"Phone: {phone}\n")
                f.write(f"Subject: {subject}\n")
                f.write(f"Message: {message}\n")
                f.write(f"{'='*50}\n")
            
            # Success message
            messages.success(request, 'Thank you for your message! I will get back to you soon.')
            
        except Exception as e:
            # Error message
            messages.error(request, f'There was an error saving your message. Please try again.')
            print(f"Error saving contact form: {e}")  # For debugging
        
        return render(request, 'contect.html')
    
    return render(request, 'contect.html')
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

# Option A: Using decorator (recommended)
@staff_member_required
def view_contacts(request):
    """View all contact submissions (admin only)"""
    submissions = []
    try:
        with open('all_contacts.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            submissions = content.split('='*50)
    except FileNotFoundError:
        submissions = ['No submissions yet']
    
    return render(request, 'view_contacts.html', {'submissions': submissions})