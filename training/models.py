# Import necessary modules
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Module model - represents a training module
class Module(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modules_taught')
    created_at = models.DateTimeField(default=timezone.now)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# Enrollment model - tracks which students are enrolled in which modules
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'module')

    def __str__(self):
        return f"{self.student.username} - {self.module.title}"

# Resource model - represents learning materials in a module
class Resource(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='resources/')
    uploaded_at = models.DateTimeField(default=timezone.now)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# ForumPost model - represents discussion posts in a module
class ForumPost(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='forum_posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Progress model - tracks which resources a student has completed
class Progress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='progress')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('enrollment', 'resource')

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.resource.title}"

# Certificate model - represents certificates earned by students
class Certificate(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    issued_at = models.DateTimeField(default=timezone.now)
    certificate_number = models.CharField(max_length=50, unique=True)
    pdf_file = models.FileField(upload_to='certificates/', null=True, blank=True)

    def __str__(self):
        return f"Certificate for {self.enrollment.student.username} - {self.enrollment.module.title}" 