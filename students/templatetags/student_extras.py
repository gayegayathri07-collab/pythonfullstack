from django import template

register = template.Library()

@register.filter
def department_badge(dept):
    badges = {
        "CSE": "badge-cse",
        "ECE": "badge-ece",
        "ME": "badge-me",
        "EEE": "badge-eee",
    }
    cls = badges.get(dept, "")
    return f'<span class="badge {cls}">{dept}</span>'
