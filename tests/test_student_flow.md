# Teacher Portal - Test Flow

## 1. Login Functionality

### Positive
- [ ] Login with valid teacher credentials → Redirects to home screen.

### Negative
- [ ] Login with invalid username → Shows "Username not found in the database."
- [ ] Login with invalid password → Shows "Password invalid or username and password do not match."

---

## 2. Student Listing & CRUD

### Positive
- [ ] Home page lists all students with Name, Subject, Marks, Actions.
- [ ] Add new student with valid name (one or more words, each capitalized), subject, and marks (any integer) → Student appears in list.
- [ ] Add student with existing name and subject → Marks are added to the existing student's marks (positive or negative), and a success message is shown.
- [ ] Add student with existing name but new subject → New row is created.
- [ ] Edit student inline (change name, subject, marks) → Updates in list.
- [ ] Delete student → Row is removed.

### Negative
- [ ] Add student with non-integer marks (e.g., "abc", "10.5") → Error shown.
- [ ] Add student with empty fields → Error shown.
- [ ] Edit student with non-integer marks → Error shown.
- [ ] Delete non-existent student (simulate) → Handled gracefully.
- [ ] Add student with name not matching capitalization format (e.g., "arun", "arun Kumar", "arunkumar s") → Error shown.

---

## 3. Subject Dropdown

- [ ] All standard subjects visible in dropdown.
- [ ] Add a new subject via popup → Subject appears in dropdown next time.
- [ ] Subject name auto-formats to capitalize first letter of each word.

---

## 4. Forgot Password Flow

### Positive
- [ ] Click "Forgot password?", enter valid email → OTP sent (check console or email).
- [ ] Enter correct OTP and new password (twice) → Password updated, can log in with new password.

### Negative
- [ ] Enter unknown email → Error shown.
- [ ] Enter incorrect OTP → Error shown.
- [ ] Enter mismatched passwords → Error shown.

---

## 5. Teacher CSV Upload (Principal)

### Positive
- [ ] Upload CSV with new teacher data → Users created, emails sent (check console or email).
- [ ] Teacher can reset password after first login, CSV hash updated.

### Negative
- [ ] Upload CSV with missing fields → Those rows skipped, others processed.
- [ ] Upload CSV with duplicate username/email → Existing user not overwritten, warning shown.

#### CSV Testing Instructions

- For development, set in `settings.py`:
    ```
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    ```
  Use any dummy email address for testing. No real emails will be sent.
- For real email testing, update SMTP settings and use a real email/app password.

---

## 6. Security

- [ ] All sensitive actions require login.
- [ ] Only staff can upload teacher CSV.
- [ ] Passwords never shown in plain text.
- [ ] CSRF tokens present in all forms and AJAX requests.

---

## 7. UI/UX

- [ ] Modals open and close as expected.
- [ ] All error/success messages are clear.
- [ ] Responsive design works on desktop and mobile.

---

## 8. Additional Use Cases (Implemented)

- [ ] Student names are case-insensitively unique per subject.
- [ ] Student name format enforced: "Firstname I I" or "Firstname I" (initials, spaces, no dots).
- [ ] Marks can be any integer (positive, zero, or negative).
- [ ] Login warns if username not found.
- [ ] Subject dropdown with "Add new subject..." option.

---

# End of Test Flow
