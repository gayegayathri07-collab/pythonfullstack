from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.db.models import Avg, Max, Min, Count, Q, Sum
from django.utils import timezone
from datetime import timedelta
from .models import Student, Department, Course, Attendance
from .forms import ContactForm, StudentForm

def landing(request):
    dept_stats = Department.objects.annotate(n=Count('students'), avg_marks=Avg('students__marks'))
    total_students = Student.objects.count()
    total_depts = Department.objects.count()
    top_students = Student.objects.select_related('department').order_by('-marks')[:6]
    latest_students = Student.objects.select_related('department').order_by('-admitted')[:6]

    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    total_att = Attendance.objects.filter(date__gte=week_ago).count()
    present_att = Attendance.objects.filter(date__gte=week_ago, present=True).count()
    attendance_pct = round((present_att / total_att * 100)) if total_att else 85

    testimonials = []
    for s in Student.objects.exclude(bio='').order_by('-marks')[:4]:
        testimonials.append({
            'name': s.name,
            'dept': s.department.name if s.department else '',
            'quote': s.bio[:200],
            'image': s.image.url if s.image else None,
            'marks': s.marks,
        })

    return render(request, "students/landing.html", {
        'dept_stats': dept_stats,
        'total_students': total_students,
        'total_depts': total_depts,
        'top_students': top_students,
        'latest_students': latest_students,
        'testimonials': testimonials,
        'attendance_pct': attendance_pct,
        'avg_marks': Student.objects.aggregate(avg=Avg('marks'))['avg'] or 0,
    })

def dashboard(request):
    students = Student.objects.select_related('department').all()
    dept_stats = Department.objects.annotate(n=Count('students'), avg_marks=Avg('students__marks'))

    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    total_attendance = Attendance.objects.filter(date__gte=week_ago).count()
    present_attendance = Attendance.objects.filter(date__gte=week_ago, present=True).count()
    attendance_pct = round((present_attendance / total_attendance * 100)) if total_attendance else 0

    dept_attendance = []
    for dept in Department.objects.all():
        dept_students = dept.students.all()
        total = Attendance.objects.filter(student__in=dept_students, date__gte=week_ago).count()
        present = Attendance.objects.filter(student__in=dept_students, date__gte=week_ago, present=True).count()
        dept_attendance.append({
            'name': dept.name,
            'pct': round((present / total * 100)) if total else 0,
        })

    stats = {
        'total_students': students.count(),
        'avg_marks': Student.objects.aggregate(avg=Avg('marks'))['avg'] or 0,
        'top_marks': Student.objects.aggregate(top=Max('marks'))['top'] or 0,
        'total_depts': Department.objects.count(),
        'dept_stats': dept_stats,
        'attendance_pct': attendance_pct,
        'dept_attendance': dept_attendance,
    }

    add_form = StudentForm()
    contact_form = ContactForm()
    add_success = None
    contact_success = None

    if request.method == 'POST':
        if 'add_student' in request.POST:
            add_form = StudentForm(request.POST, request.FILES)
            if add_form.is_valid():
                add_form.save()
                add_success = "Student added successfully!"
                add_form = StudentForm()
            return render(request, "students/dashboard.html", {
                "students": students, "stats": stats,
                "add_form": add_form, "contact_form": contact_form,
                "add_success": add_success, "contact_success": contact_success,
            })
        elif 'contact_submit' in request.POST:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                data = contact_form.cleaned_data
                contact_success = f"Thanks {data['name']}! We received your message."
                contact_form = ContactForm()
            return render(request, "students/dashboard.html", {
                "students": students, "stats": stats,
                "add_form": add_form, "contact_form": contact_form,
                "add_success": add_success, "contact_success": contact_success,
            })

    return render(request, "students/dashboard.html", {
        "students": students,
        "stats": stats,
        "add_form": add_form,
        "contact_form": contact_form,
        "add_success": add_success,
        "contact_success": contact_success,
    })

def add_contact(request):
    add_form = StudentForm()
    contact_form = ContactForm()
    add_success = contact_success = add_error = None

    if request.method == 'POST':
        if 'add_student' in request.POST:
            add_form = StudentForm(request.POST, request.FILES)
            if add_form.is_valid():
                add_form.save()
                add_success = "Student added successfully!"
                add_form = StudentForm()
            else:
                add_error = "Please correct the errors below."
        elif 'contact_submit' in request.POST:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                data = contact_form.cleaned_data
                contact_success = f"Thanks {data['name']}! We received your message."
                contact_form = ContactForm()

    return render(request, 'students/add_contact.html', {
        'add_form': add_form, 'contact_form': contact_form,
        'add_success': add_success, 'contact_success': contact_success,
        'add_error': add_error,
    })

class StudentListView(ListView):
    model = Student
    template_name = 'students/index.html'
    context_object_name = 'students'
    paginate_by = 5

    def get_queryset(self):
        qs = Student.objects.select_related('department').all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q)
        return qs

class StudentDetailView(DetailView):
    model = Student
    template_name = 'students/detail.html'
    context_object_name = 's'
    pk_url_kwarg = 'pk'

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/form_student.html'
    success_url = reverse_lazy('students:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Add Student'
        return context

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/form_student.html'
    success_url = reverse_lazy('students:index')
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = f"Edit {self.object.name}"
        return context

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('students:index')
    pk_url_kwarg = 'pk'

class ContactView(FormView):
    template_name = 'students/form_contact.html'
    form_class = ContactForm

    def form_valid(self, form):
        data = form.cleaned_data
        return HttpResponse(f"Thanks {data['name']}! We received your message.")
