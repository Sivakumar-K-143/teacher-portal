"""Views for the Teacher Portal app."""

import os
import re
import csv
import json
import random
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.files.storage import default_storage
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.admin.views.decorators import staff_member_required
from .models import Student, Subject, PasswordResetCode

def is_valid_student_name(name):
    parts = name.strip().split()
    if len(parts) < 2:
        return False
    if not re.match(r'^[A-Z][a-z]+$', parts[0]):
        return False
    for part in parts[1:]:
        if not re.match(r'^[A-Z]$', part):
            return False
    return True


def login_view(request):
    """Login view for teachers."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Username not found in the database.')
            return render(request, 'portal/login.html')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Password invalid or username and password do not match.')
        return render(request, 'portal/login.html')
    return render(request, 'portal/login.html')

def logout_view(request):
    """Logout view."""
    logout(request)
    return redirect('login')

@login_required
def home(request):
    """Home view: student listing."""
    students = Student.objects.select_related('subject').all()
    subjects = Subject.objects.all()
    return render(request, 'portal/home.html', {
        'students': students,
        'subjects': subjects,
    })

@login_required
def get_subjects(request):
    """API to get all subjects."""
    subjects = list(Subject.objects.values_list('name', flat=True))
    return JsonResponse({'subjects': subjects})

@login_required
@csrf_exempt
@require_POST
def add_student(request):
    """Add a new student or update marks if exists."""
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        subject_name = data.get('subject', '').strip()
        marks = data.get('marks')
        if not name or not subject_name or marks is None:
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)
        try:
            marks = int(marks)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Marks must be a number.'}, status=400)
        if marks < 0 or marks > 100:
            return JsonResponse({'status': 'error', 'message': 'Marks must be between 0 and 100.'}, status=400)

        # Normalize name (capitalize first name, initials uppercase)
        name_parts = name.strip().split()
        name_normalized = ""
        if name_parts:
            name_normalized = name_parts[0].capitalize() + (" " + " ".join([p.upper() for p in name_parts[1:]]) if len(name_parts) > 1 else "")

        # Validate name format
        if not is_valid_student_name(name_normalized):
            return JsonResponse({'status': 'error', 'message': 'Name should be like "Arun S S" or "Arun S". Initials must be single uppercase letters with spaces, no dots.'}, status=400)

        subject, _ = Subject.objects.get_or_create(name=subject_name)

        # Case-insensitive check for existing student with same subject
        if Student.objects.filter(name__iexact=name_normalized, subject=subject).exists():
            return JsonResponse({'status': 'error', 'message': 'Student with this name and subject already exists (case-insensitive).'}, status=400)

        student = Student.objects.create(name=name_normalized, subject=subject, marks=marks)
        return JsonResponse({'status': 'created', 'student_id': student.id, 'marks': student.marks, 'subject': subject.name})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
@csrf_exempt
@require_POST
def edit_student(request, student_id):
    """Edit an existing student."""
    student = get_object_or_404(Student, id=student_id)
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        subject_name = data.get('subject', '').strip()
        marks = data.get('marks')
        if not name or not subject_name or marks is None:
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)
        try:
            marks = int(marks)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Marks must be a number.'}, status=400)
        if marks < 0 or marks > 100:
            return JsonResponse({'status': 'error', 'message': 'Marks must be between 0 and 100.'}, status=400)

        # Normalize name
        name_parts = name.strip().split()
        name_normalized = ""
        if name_parts:
            name_normalized = name_parts[0].capitalize() + (" " + " ".join([p.upper() for p in name_parts[1:]]) if len(name_parts) > 1 else "")

        # Validate name format
        if not is_valid_student_name(name_normalized):
            return JsonResponse({'status': 'error', 'message': 'Name should be like "Arun S S" or "Arun S". Initials must be single uppercase letters with spaces, no dots.'}, status=400)

        subject, _ = Subject.objects.get_or_create(name=subject_name)
        # Case-insensitive unique check (exclude current student)
        if Student.objects.exclude(id=student_id).filter(name__iexact=name_normalized, subject=subject).exists():
            return JsonResponse({'status': 'error', 'message': 'Student with this name and subject already exists (case-insensitive).'}, status=400)

        student.name = name_normalized
        student.subject = subject
        student.marks = marks
        student.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
@csrf_exempt
@require_POST
def delete_student(request, student_id):
    """Delete a student."""
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return JsonResponse({'status': 'deleted'})

@csrf_exempt
@require_POST
def send_reset_code(request):
    """Send OTP code for password reset."""
    email = request.POST.get('email')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Email not found.'})
    code = f"{random.randint(100000, 999999)}"
    PasswordResetCode.objects.create(user=user, code=code)
    send_mail(
        'Your Password Reset Code',
        f'Your password reset code is: {code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    return JsonResponse({'status': 'ok'})

def update_csv_password(username, new_password_hash):
    """Update the CSV file with the new password hash."""
    csv_path = os.path.join(settings.MEDIA_ROOT, 'uploads/teachers.csv')
    if not os.path.exists(csv_path):
        return
    df = pd.read_csv(csv_path)
    df.loc[df['username'] == username, 'first_password'] = new_password_hash
    df.to_csv(csv_path, index=False)

@csrf_exempt
@require_POST
def verify_reset_code_and_update_password(request):
    """Verify OTP and update the user's password."""
    email = request.POST.get('email')
    code = request.POST.get('code')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    if password1 != password2:
        return JsonResponse({'status': 'error', 'message': 'Passwords do not match.'})
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Email not found.'})
    try:
        reset_code = PasswordResetCode.objects.filter(user=user, code=code, is_used=False).latest('created_at')
        if reset_code.is_expired():
            return JsonResponse({'status': 'error', 'message': 'Code expired.'})
    except PasswordResetCode.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid or expired code.'})
    reset_code.is_used = True
    reset_code.save()
    user.set_password(password1)
    user.save()
    update_csv_password(user.username, user.password)
    return JsonResponse({'status': 'ok'})

@staff_member_required
@require_http_methods(["GET", "POST"])
def upload_teachers_csv(request):
    """
    Upload and process a CSV file of new teachers.
    - Only adds users if username and email do not already exist in DB.
    - Does NOT update or overwrite any existing user.
    - All username, email, and password fields must be unique within the file.
    - Skipped users (already exist or error) are reported.
    - Always overwrites the previous teachers.csv in media/uploads/.
    """
    if request.method == 'POST':
        upload_dir = 'uploads'
        filename = 'teachers.csv'
        filepath = os.path.join(upload_dir, filename)
        full_path = os.path.join(settings.MEDIA_ROOT, filepath)

        # Delete old file if it exists to ensure overwrite
        if default_storage.exists(filepath):
            default_storage.delete(filepath)

        # Save the new file as teachers.csv
        file = request.FILES['csv_file']
        default_storage.save(filepath, file)

        # Now open the file for reading
        with default_storage.open(filepath, 'rb') as f:
            content = f.read().decode('utf-8')
            reader = csv.DictReader(content.splitlines())
            required_fields = {'username', 'email', 'first_password'}
            if not required_fields.issubset(reader.fieldnames):
                messages.error(request, 'CSV must contain username, email, and first_password columns.')
                return render(request, 'portal/upload_teachers.html')

            # Collect all usernames, emails, and passwords for duplicate check
            usernames = []
            emails = []
            passwords = []
            rows = list(reader)
            for row in rows:
                usernames.append(row['username'].strip())
                emails.append(row['email'].strip())
                passwords.append(row['first_password'].strip())

            # Check for duplicates in each field within the CSV
            duplicate_usernames = set([x for x in usernames if usernames.count(x) > 1])
            duplicate_emails = set([x for x in emails if emails.count(x) > 1])
            duplicate_passwords = set([x for x in passwords if passwords.count(x) > 1])

            if duplicate_usernames or duplicate_emails or duplicate_passwords:
                error_msgs = []
                if duplicate_usernames:
                    error_msgs.append(f"Duplicate usernames: {', '.join(duplicate_usernames)}")
                if duplicate_emails:
                    error_msgs.append(f"Duplicate emails: {', '.join(duplicate_emails)}")
                if duplicate_passwords:
                    error_msgs.append(f"Duplicate passwords: {', '.join(duplicate_passwords)}")
                messages.error(request, "Every field (username, email, password) must be unique. " + " ".join(error_msgs))
                return render(request, 'portal/upload_teachers.html')

            added = []
            skipped = []
            for row in rows:
                username = row['username'].strip()
                email = row['email'].strip()
                plain_password = row['first_password'].strip()
                print(f"Processing row: username={username}, email={email}, password={plain_password}")
                # Skip if username or email already exists in DB
                if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                    print(f"Skipping existing user: {username}")
                    skipped.append(username)
                    continue
                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=plain_password,
                        is_active=True,
                    )
                    added.append(username)
                    print(f"Added user: {username}")
                except Exception as e:
                    print(f"Error adding user {username}: {e}")
                    skipped.append(username)
        return render(request, 'portal/upload_teachers.html', {'success': True, 'added': added, 'skipped': skipped})
    return render(request, 'portal/upload_teachers.html')
