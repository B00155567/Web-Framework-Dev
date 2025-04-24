from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from .models import Module, Enrollment, Resource, ForumPost, Progress, Certificate
from .forms import ModuleForm, ResourceForm, ForumPostForm, UserRegistrationForm
import uuid

# Handle user registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the Training Management System.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'training/register.html', {'form': form})

# Show home page with user's modules
def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            modules = Module.objects.filter(instructor=request.user)
        else:
            enrollments = Enrollment.objects.filter(student=request.user)
            modules = [e.module for e in enrollments]
        return render(request, 'training/home.html', {'modules': modules})
    return render(request, 'training/home.html')

# Handle user login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'training/login.html', {'form': form})

# Handle user logout
def logout_view(request):
    logout(request)
    return redirect('home')

# Show list of all active modules
@login_required
def module_list(request):
    modules = Module.objects.filter(is_active=True)
    return render(request, 'training/module_list.html', {'modules': modules})

# Create a new module (staff only)
@login_required
def module_create(request):
    if not request.user.is_staff:
        messages.error(request, 'Only instructors can create modules.')
        return redirect('module_list')
    
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.instructor = request.user
            module.save()
            messages.success(request, 'Module created successfully.')
            return redirect('module_detail', pk=module.pk)
    else:
        form = ModuleForm()
    return render(request, 'training/module_form.html', {'form': form})

# Show details of a specific module
@login_required
def module_detail(request, pk):
    module = get_object_or_404(Module, pk=pk)
    is_enrolled = Enrollment.objects.filter(student=request.user, module=module).exists()
    return render(request, 'training/module_detail.html', {
        'module': module,
        'is_enrolled': is_enrolled
    })

# Enroll in a module
@login_required
def enroll(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    if not Enrollment.objects.filter(student=request.user, module=module).exists():
        Enrollment.objects.create(student=request.user, module=module)
        messages.success(request, 'Successfully enrolled in the module.')
    return redirect('module_detail', pk=module_id)

# Unenroll from a module
@login_required
def unenroll(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    enrollment = Enrollment.objects.filter(student=request.user, module=module).first()
    if enrollment:
        enrollment.delete()
        messages.success(request, 'Successfully unenrolled from the module.')
    return redirect('module_detail', pk=module_id)

# Show list of resources for a module
@login_required
def resource_list(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    resources = Resource.objects.filter(module=module)
    return render(request, 'training/resource_list.html', {
        'module': module,
        'resources': resources
    })

# Upload a new resource (staff only)
@login_required
def resource_upload(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    if not request.user.is_staff and module.instructor != request.user:
        messages.error(request, 'Only instructors can upload resources.')
        return redirect('resource_list', module_id=module_id)
    
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.module = module
            resource.uploaded_by = request.user
            resource.save()
            messages.success(request, 'Resource uploaded successfully.')
            return redirect('resource_list', module_id=module_id)
    else:
        form = ResourceForm()
    return render(request, 'training/resource_form.html', {'form': form, 'module': module})

# Show forum posts for a module
@login_required
def forum_list(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    posts = ForumPost.objects.filter(module=module).order_by('-created_at')
    return render(request, 'training/forum_list.html', {
        'module': module,
        'posts': posts
    })

# Create a new forum post
@login_required
def forum_post_create(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.module = module
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully.')
            return redirect('forum_list', module_id=module_id)
    else:
        form = ForumPostForm()
    return render(request, 'training/forum_post_form.html', {'form': form, 'module': module})

# Show user's progress in all modules
@login_required
def progress_list(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    for enrollment in enrollments:
        resources = Resource.objects.filter(module=enrollment.module)
        progress_dict = {}
        for resource in resources:
            progress_obj, created = Progress.objects.get_or_create(
                enrollment=enrollment,
                resource=resource
            )
            progress_dict[resource.id] = progress_obj
        
        # Check if all resources are completed
        all_completed = all(progress.completed for progress in progress_dict.values())
        if all_completed and not enrollment.completed:
            enrollment.completed = True
            enrollment.completion_date = timezone.now()
            enrollment.save()
        
        enrollment.progress_dict = progress_dict
    return render(request, 'training/progress_list.html', {'enrollments': enrollments})

# Mark a resource as completed
@login_required
def mark_resource_complete(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    enrollment = get_object_or_404(Enrollment, student=request.user, module=resource.module)
    progress, created = Progress.objects.get_or_create(
        enrollment=enrollment,
        resource=resource
    )
    if not progress.completed:
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()
        
        # Check if all resources are completed
        all_resources = Resource.objects.filter(module=resource.module)
        completed_resources = Progress.objects.filter(
            enrollment=enrollment,
            resource__in=all_resources,
            completed=True
        )
        if completed_resources.count() == all_resources.count():
            enrollment.completed = True
            enrollment.completion_date = timezone.now()
            enrollment.save()
            messages.success(request, 'Module completed! You can now generate a certificate.')
        else:
            messages.success(request, 'Resource marked as completed.')
    return redirect('progress_list')

# Show list of user's certificates
@login_required
def certificate_list(request):
    certificates = Certificate.objects.filter(enrollment__student=request.user)
    return render(request, 'training/certificate_list.html', {'certificates': certificates})

# Generate a certificate for a completed module
@login_required
def generate_certificate(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id, student=request.user)
    if enrollment.completed and not hasattr(enrollment, 'certificate'):
        certificate = Certificate.objects.create(
            enrollment=enrollment,
            certificate_number=str(uuid.uuid4())[:8].upper()
        )
        messages.success(request, 'Certificate generated successfully.')
    return redirect('certificate_list')

# Edit a module (staff only)
@login_required
def module_edit(request, pk):
    module = get_object_or_404(Module, pk=pk)
    if not request.user.is_staff:
        messages.error(request, 'Only instructors can edit modules.')
        return redirect('module_list')
    
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            messages.success(request, 'Module updated successfully.')
            return redirect('module_detail', pk=module.pk)
    else:
        form = ModuleForm(instance=module)
    return render(request, 'training/module_form.html', {'form': form})

# Show details of a forum post
@login_required
def forum_post_detail(request, module_id, post_id):
    post = get_object_or_404(ForumPost, pk=post_id, module_id=module_id)
    return render(request, 'training/forum_post_detail.html', {'post': post})

# Edit a forum post
@login_required
def forum_post_edit(request, module_id, post_id):
    post = get_object_or_404(ForumPost, pk=post_id, module_id=module_id)
    
    # Check if user has permission to edit the post
    if not (request.user.is_staff or post.author == request.user):
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('forum_post_detail', module_id=module_id, post_id=post_id)
    
    if request.method == 'POST':
        form = ForumPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('forum_post_detail', module_id=module_id, post_id=post_id)
    else:
        form = ForumPostForm(instance=post)
    
    return render(request, 'training/forum_post_form.html', {
        'form': form,
        'module': post.module,
        'is_edit': True
    }) 