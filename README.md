# Teacher Portal

A modern Django web app for school staff to manage students, subjects, and teachers efficiently.  
Includes robust authentication, student CRUD, subject management, CSV teacher upload, and a secure password reset flow.

---

## 🚀 Features

- **Secure Teacher Login**
- **Student Management**: Add, edit, delete, and view students with subject and marks.
- **Subject Management**: Select from dropdown or add new subjects on the fly (auto-capitalized).
- **Teacher CSV Upload**: Principal can bulk-upload teachers via CSV.
- **Forgot Password**: OTP-based password reset (email integration).
- **Role-based Access**: Only staff can upload teacher CSV.
- **Modern UI/UX**: Responsive, clear error messages, modal dialogs.
- **Security**: CSRF protection, password hashing, and more.

---

## 📝 Requirements

- Python 3.8+
- Django 4.x or 5.x
- (Optional) pandas (for CSV password hash update)
- SMTP credentials (for real email sending)

---

## ⚡️ Quick Start

- git clone https://github.com/yourusername/teacher-portal.git
- cd teacher-portal
- python -m venv env
- source env/bin/activate # On Windows: env\Scripts\activate
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver


---

## 📬 Email Setup (Forgot Password)

**Development/Test (no real emails sent):**

In `settings.py`, use:

- EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
- Emails will print in your terminal.

**Production (send real emails):**

1. Use Gmail SMTP (recommended for testing):
    ```
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'your_email@gmail.com'
    EMAIL_HOST_PASSWORD = 'your_app_password'  # 16-char Google App Password
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    ```
2. [How to get a Gmail App Password](https://support.google.com/accounts/answer/185833?hl=en)

**Update these settings before using the forgot password flow with real emails.**

---

## 📦 CSV Upload (Teacher Bulk Add)

- Only staff/principal can access this feature.
- Upload a CSV with columns: `username,email,first_password`
- System checks for duplicate usernames/emails and skips existing users.
- **CSV instructions:**
    - All usernames/emails must be unique.
    - Passwords should be strong.
    - Example:
        ```
        username,email,first_password
        teacher1,teacher1@example.com,TempPass123
        teacher2,teacher2@example.com,InitPass456
        ```
- On upload, new users are created. Existing users are not overwritten for safety.

**Advantages:**
- Fast onboarding of multiple teachers.
- No manual entry for each teacher.
- Secure: existing accounts are never overwritten.

---

## 📚 Subject Dropdown & Add New

- All subjects must be entered for each student.
- Select from dropdown for consistency.
- If a subject is missing, click **"Add new subject..."** and enter the name.
- **Subject names are auto-formatted:** First letter of each word is uppercase (e.g., "Computer Science").

---

## 🧑‍🎓 Student Name & Marks Validation

- **Names:** Must be in the format "Firstname I I" or "Firstname I" (e.g., "Arun S S" or "Arun S"), where initials are single uppercase letters, separated by spaces, no dots.
- **Marks:** Must be between 0 and 100 (inclusive).
- **No duplicates:** Adding a student with the same name (case-insensitive) and subject shows a warning; use the edit button to update marks.

---

## 🛡️ Additional Enhancements (Beyond Requirements)

- **Case-insensitive duplicate check** for student names.
- **Strict name and marks validation** (not specified in requirements).
- **User-friendly error messages** for login, student add/edit, and CSV upload.
- **Login warns if username is not in the database.**
- **Initials shown in a circle** beside student names in the UI.
- **All forms and AJAX requests are CSRF-protected.**

---

## 🧪 Test Flow

See [`test_teacher_flow.md`](test_teacher_flow.md) for a full list of test cases, including positive/negative scenarios for login, student CRUD, subject management, CSV upload, forgot password, and security.

---

## 📝 CSV & Email Testing Instructions

- For **development**, use the console email backend (`EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`) and any dummy email address for testing forgot password. No real emails will be sent.
- For **production/real email testing**, update your SMTP settings with a real email and app password.

---

## 🚦 How to Publish Your Code

1. **Push your code to GitHub:**
    ```
    git init
    git add .
    git commit -m "Initial commit: Teacher Portal"
    git remote add origin https://github.com/yourusername/teacher-portal.git
    git branch -M main
    git push -u origin main
    ```
2. **Add your README.md and test_teacher_flow.md to the repo.**
3. **(Optional) Add a screenshot or GIF of your UI to the README.**

---

## 📢 Header: Additional Use Cases & Notes

- **CSV upload by principal**: Enables safe, fast teacher onboarding. No risk of overwriting existing accounts.
- **Subject dropdown**: Prevents typos and enforces consistency. "Add new subject" allows flexibility.
- **Student add/edit logic**: If a student with the same name and subject exists, marks are not overwritten by default; editing is explicit.
- **Validation**: Names and marks are validated even though not required in the original spec, for data quality.
- **Login**: Warns if username is not found, improving user experience.

---

## 📄 License

MIT License (add a LICENSE file if you wish).

---

## 🙋‍♂️ Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📬 Contact

For questions, open an issue or contact [sivakumark31199@example.com].
