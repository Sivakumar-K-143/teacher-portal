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
- [ ] Add new student with valid name, subject, marks (0-100) → Student appears in list.
- [ ] Add student with existing name and subject → Marks are incremented.
- [ ] Add student with existing name but new subject → New row is created.
- [ ] Edit student inline (change name, subject, marks) → Updates in list.
- [ ] Delete student → Row is removed.

### Negative
- [ ] Add student with marks < 0 or > 100 → Error shown.
- [ ] Add student with empty fields → Error shown.
- [ ] Edit student with invalid marks → Error shown.
- [ ] Delete non-existent student (simulate) → Handled gracefully.

---

## 3. Subject Dropdown

- [ ] All standard subjects visible in dropdown.
- [ ] Add a new subject via popup → Subject appears in dropdown next time.

---

## 4. Forgot Password Flow

### Positive
- [ ] Click "Forgot password?", enter valid email → OTP sent (check console).
- [ ] Enter correct OTP and new password (twice) → Password updated, can log in with new password.

### Negative
- [ ] Enter unknown email → Error shown.
- [ ] Enter incorrect OTP → Error shown.
- [ ] Enter mismatched passwords → Error shown.

---

## 5. Teacher CSV Upload (Principal)

### Positive
- [ ] Upload CSV with new teacher data → Users created, emails sent (check console).
- [ ] Teacher can reset password after first login, CSV hash updated.

### Negative
- [ ] Upload CSV with missing fields → Those rows skipped, others processed.
- [ ] Upload CSV with duplicate username → Existing user not overwritten.

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

# End of Test Flow
