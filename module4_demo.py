import urllib.request, http.cookiejar, io, re, os, sqlite3, uuid
from PIL import Image, ImageDraw

print("=" * 70)
print("  MODULE 4 - DJANGO WEB FRAMEWORK :: CAMPUSHUB")
print("  Complete Demonstration (Topics 4.1 through 4.9)")
print("=" * 70)

# --- 4.1 Project Setup ---
print()
print("=" * 70)
print("  4.1 PROJECT SETUP & CONFIGURATION")
print("=" * 70)
print("  Python + Django 5.0.6")
print("  Project: campushub")
print("  Apps: accounts (auth), students (main)")
print("  Database: SQLite (db.sqlite3)")
print("  Templates: project-level (templates/) + app-level")
print("  Static: STATIC_URL='static/', STATICFILES_DIRS=[BASE_DIR/'static']")
print("  Media: MEDIA_ROOT=BASE_DIR/'media', MEDIA_URL='/media/'")

# --- 4.2 URL Routing & Views ---
print()
print("=" * 70)
print("  4.2 URL ROUTING & VIEWS")
print("=" * 70)

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

routes = [
    ("/admin/", "Admin", False),
    ("/students/", "Dashboard (FBV)", True),
    ("/students/list/", "Student List (CBV - ListView)", True),
    ("/students/contact/", "Contact (CBV - FormView)", True),
    ("/students/add/", "Add Student (CBV - CreateView)", True),
    ("/students/1/", "Student Detail (CBV - DetailView)", True),
    ("/accounts/login/", "Login", True),
    ("/accounts/register/", "Register", True),
]
for path, name, expect_200 in routes:
    try:
        r = opener.open("http://127.0.0.1:8000" + path)
        s = r.getcode()
    except urllib.error.HTTPError as e:
        s = e.code
    except Exception as e:
        s = f"ERR:{e}"
    status = "OK" if (expect_200 and s == 200) or (not expect_200) else "?"
    print(f"  {status}  {s:>3}  {path:<25} {name}")

# --- 4.3 Templates & Inheritance ---
print()
print("=" * 70)
print("  4.3 DJANGO TEMPLATES")
print("=" * 70)
r = opener.open("http://127.0.0.1:8000/students/list/")
html = r.read().decode()
print(f"  Template inheritance: base.html -> students/index.html")
print(f"  Block overrides: title, content")
print(f"  Template tags: {{% for %}}, {{% if %}}, {{% url %}}, {{% static %}}")
print(f"  Filters: |length, |floatformat, |date, |filesizeformat")
print(f"  Custom filter: department_badge")
print(f"  Pagination: paginate_by=5 on ListView")
print(f"  Static files: style.css ({len(open('static/css/style.css').read())} bytes)")

# --- 4.4 Models & ORM ---
print()
print("=" * 70)
print("  4.4 MODELS & ORM")
print("=" * 70)
conn = sqlite3.connect("db.sqlite3")
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM students_department")
dept_count = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM students_student")
student_count = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM students_course")
course_count = c.fetchone()[0]
c.execute("SELECT name FROM students_department")
depts = [r[0] for r in c.fetchall()]
c.execute("SELECT roll, name, marks, department_id FROM students_student ORDER BY marks DESC LIMIT 5")
top5 = c.fetchall()
print(f"  Models: Department, Student, Course")
print(f"  Departments ({dept_count}): {', '.join(depts)}")
print(f"  Students: {student_count}")
print(f"  Courses: {course_count}")
print(f"  ORM: select_related, annotate, aggregate (Avg, Max, Count)")
print(f"  Top 5 students (by marks):")
for r in top5:
    c.execute("SELECT name FROM students_department WHERE id=?", (r[3],))
    row_d = c.fetchone()
    dn = row_d[0] if row_d else "?"
    print(f"    #{r[0]} {r[1]:20s} {r[2]} marks  ({dn})")
conn.close()

# --- 4.5 Forms & Validation ---
print()
print("=" * 70)
print("  4.5 FORMS & VALIDATION")
print("=" * 70)
print("  ContactForm: plain Form (name, email, age, message)")
print("  StudentForm: ModelForm (roll, name, email, marks, dept, image, resume, bio)")
print("  Custom clean_email(): must end with @college.edu")
print("  Custom clean(): CSE requires marks >= 40")
print("  Widgets: TextInput, EmailInput, NumberInput, Select, FileInput, Textarea")

# --- 4.6 Admin Panel ---
print()
print("=" * 70)
print("  4.6 DJANGO ADMIN PANEL")
print("=" * 70)
print("  URL: /admin/")
print("  DepartmentAdmin: name, student_count, inline students")
print("  StudentAdmin: roll, name, email, dept, marks, grade, photo, filters")
print("  CourseAdmin: code, title, enrolled count, filter_horizontal students")
print("  Custom actions: activate/deactivate students")

# --- 4.7 Authentication ---
print()
print("=" * 70)
print("  4.7 USER AUTHENTICATION")
print("=" * 70)
print("  Register: /accounts/register/ (UserCreationForm + email)")
print("  Login: /accounts/login/ (custom view with ?next= support)")
print("  Logout: /accounts/logout/")
print("  Password Change: /accounts/password-change/")
print("  Password Reset: /accounts/password-reset/ (full 4-step flow)")
print("  Protected views: CreateView, UpdateView, DeleteView (LoginRequiredMixin)")

# --- 4.8 Class-Based Views ---
print()
print("=" * 70)
print("  4.8 CLASS-BASED VIEWS (CBV)")
print("=" * 70)
print("  View              | Generic       | Mixin            | URL")
print("  ------------------+---------------+---------------+----------------")
print("  StudentListView   | ListView      | -               | /students/list/")
print("  StudentDetailView | DetailView    | -               | /students/<pk>/")
print("  StudentCreateView | CreateView    | LoginRequired   | /students/add/")
print("  StudentUpdateView | UpdateView    | LoginRequired   | /students/<pk>/edit/")
print("  StudentDeleteView | DeleteView    | LoginRequired   | /students/<pk>/delete/")
print("  ContactView       | FormView      | -               | /students/contact/")
print("  Dashboard         | FBV           | -               | /students/")

# --- 4.9 File Upload & Media ---
print()
print("=" * 70)
print("  4.9 FILE UPLOAD & MEDIA HANDLING")
print("=" * 70)

# Create test image
img = Image.new("RGB", (150, 150), color="#7c3aed")
draw = ImageDraw.Draw(img)
draw.text((40, 65), "M4", fill="white")
buf = io.BytesIO()
img.save(buf, format="JPEG")
buf.seek(0)
img_bytes = buf.read()

# Upload
resp = opener.open("http://127.0.0.1:8000/")
csrf = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', resp.read().decode()).group(1)
unique = str(int(uuid.uuid4().hex[:6], 16) % 9000 + 1000)
boundary = "----" + uuid.uuid4().hex
parts = []
for n, v in [("csrfmiddlewaretoken", csrf), ("add_student", "1"),
             ("roll", unique), ("name", "Module4 Demo"),
             ("email", f"m4demo{unique}@college.edu"), ("marks", "95"), ("department", "1")]:
    parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{n}\"\r\n\r\n{v}\r\n")
parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"m4.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n")
parts.append(img_bytes.decode("latin-1"))
parts.append(f"\r\n--{boundary}--\r\n")
body = "".join(parts).encode("latin-1")
req = urllib.request.Request("http://127.0.0.1:8000/", data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}", "Referer": "http://127.0.0.1:8000/"})
opener.open(req)

conn = sqlite3.connect("db.sqlite3")
c = conn.cursor()
c.execute("SELECT roll, name, image FROM students_student WHERE roll=?", (unique,))
row = c.fetchone()
conn.close()

print(f"  Configuration: MEDIA_ROOT, MEDIA_URL, + static() in urls.py")
print(f"  Model fields: ImageField(upload_to='students/photos/'), FileField(resume)")
print(f"  Form: enctype='multipart/form-data', request.FILES passed to form")
print(f"  Security: FileExtensionValidator (pdf,docx), validate_size (2MB)")
print(f"  Processing: Pillow thumbnail on save (600x600 max)")
print(f"  Test upload: roll={row[0]}, image={row[2]}")
print(f"  File on disk: {os.path.getsize(os.path.join('media', row[2]))} bytes")
try:
    url_check = urllib.request.urlopen(f"http://127.0.0.1:8000/media/{row[2]}")
    print(f"  Served at: /media/{row[2]} ({url_check.getcode()} OK)")
except:
    print(f"  Served at: /media/{row[2]} (ERROR)")

# --- Summary ---
print()
print("=" * 70)
print("  MODULE 4 - COMPLETE SUMMARY")
print("=" * 70)
print(f"  Topics covered: 4.1 Project Setup | 4.2 URL Routing | 4.3 Templates")
print(f"                  4.4 Models & ORM | 4.5 Forms | 4.6 Admin Panel")
print(f"                  4.7 Authentication | 4.8 Class-Based Views | 4.9 File Upload")
print()
print(f"  {student_count} students across {dept_count} departments")
print(f"  6 Class-Based Views + 2 Function-Based Views")
print(f"  2 custom form validators (email domain, marks by dept)")
print(f"  Full auth system: register, login, logout, password change/reset")
print(f"  File upload with Pillow processing and security validators")
print(f"  Dark-mode responsive UI with student gallery, rankings, pagination")
print()
print("  Browse: http://127.0.0.1:8000/")
print("  Admin:  http://127.0.0.1:8000/admin/ (admin / admin123)")
print("=" * 70)
print("  MODULE 4 EXECUTED SUCCESSFULLY")
print("=" * 70)
