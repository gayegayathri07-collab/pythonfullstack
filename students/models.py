from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

def validate_file_size(f):
    if f.size > 2 * 1024 * 1024:
        raise ValidationError("File too large (max 2 MB).")

class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    roll       = models.IntegerField(unique=True)
    name       = models.CharField(max_length=50)
    email      = models.EmailField(unique=True)
    marks      = models.IntegerField(default=0)
    is_active  = models.BooleanField(default=True)
    admitted   = models.DateField(auto_now_add=True)
    bio        = models.TextField(blank=True)
    image      = models.ImageField(upload_to='students/photos/', blank=True, default='students/avatar.svg')
    resume     = models.FileField(
        upload_to='students/resumes/', blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx']), validate_file_size])
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   related_name='students')

    class Meta:
        ordering = ['-marks']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and self.image.name != 'students/avatar.svg':
            from PIL import Image
            img = Image.open(self.image.path)
            if img.height > 600 or img.width > 600:
                img.thumbnail((600, 600))
                img.save(self.image.path, optimize=True, quality=80)

    def __str__(self):
        return f"{self.roll} – {self.name}"

class Course(models.Model):
    title    = models.CharField(max_length=80)
    code     = models.CharField(max_length=20, unique=True)
    students = models.ManyToManyField(Student, related_name='courses')

    def __str__(self):
        return self.title

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField(auto_now_add=True)
    present = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['student', 'date']

    def __str__(self):
        return f"{self.student.name} - {'Present' if self.present else 'Absent'} on {self.date}"
