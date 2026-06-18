from django.contrib import admin
from django.utils.html import format_html
from .models import Department, Student, Course

class StudentInline(admin.TabularInline):
    model = Student
    extra = 1

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_count')
    search_fields = ('name',)
    inlines = [StudentInline]

    @admin.display(description='Students')
    def student_count(self, obj):
        return obj.students.count()

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll', 'name', 'email', 'department', 'marks', 'grade', 'is_active', 'show_image')
    search_fields = ('name', 'email', 'department__name')
    list_filter = ('department', 'is_active', 'admitted')
    ordering = ('-marks',)
    list_per_page = 25
    list_editable = ('marks',)
    fieldsets = (
        ('Identity', {'fields': ('roll', 'name', 'email', 'image')}),
        ('Academics', {'fields': ('department', 'marks', 'bio')}),
        ('Status', {'fields': ('is_active',), 'classes': ('collapse',)}),
    )

    @admin.display(description='Grade')
    def grade(self, obj):
        if obj.marks >= 75:
            return 'A'
        if obj.marks >= 60:
            return 'B'
        return 'C'

    @admin.display(description='Photo')
    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="40" height="40" style="border-radius:50%; object-fit:cover;">', obj.image.url)
        return ''

@admin.action(description="Mark selected students inactive")
def deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.action(description="Mark selected students active")
def activate(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'student_count')
    search_fields = ('title', 'code')
    filter_horizontal = ('students',)

    @admin.display(description='Enrolled')
    def student_count(self, obj):
        return obj.students.count()
