// ===============================
// Modal and Student Management JS
// ===============================

// Utility: Name validation (at least one word, if more than one word, each will be capitalized)
function validateStudentName(name) {
    const parts = name.trim().split(/\s+/);
    if (parts.length < 1) return false; // At least one word
    for (let part of parts) {
        if (!/^[A-Z][a-z]*$/.test(part)) return false;
    }
    return true;
}

// Modal state
let editing = false;
let editingId = null;

// Open Add/Edit Student Modal
function openModal(edit = false, student = null) {
    document.getElementById('studentModal').style.display = 'flex';
    document.getElementById('modalTitle').innerText = edit ? 'Edit Student' : 'Add Student';
    document.getElementById('modalError').innerText = '';
    document.getElementById('studentForm').reset();
    document.getElementById('newSubject').style.display = 'none';
    editing = edit;
    editingId = edit && student ? student.id : null;

    // Populate subject dropdown
    fetch('/get_subjects/')
        .then(res => res.json())
        .then(data => {
            let select = document.getElementById('subject');
            select.innerHTML = '';
            if (data.subjects.length === 0) {
                let opt = document.createElement('option');
                opt.value = '__new__';
                opt.text = 'Add new subject...';
                select.appendChild(opt);
                document.getElementById('newSubject').style.display = 'block';
            } else {
                data.subjects.forEach(subj => {
                    let opt = document.createElement('option');
                    opt.value = subj;
                    opt.text = subj;
                    select.appendChild(opt);
                });
                let opt = document.createElement('option');
                opt.value = '__new__';
                opt.text = 'Add new subject...';
                select.appendChild(opt);
                document.getElementById('newSubject').style.display = 'none';
            }

            if (edit && student) {
                document.getElementById('name').value = student.name;
                select.value = student.subject;
                document.getElementById('marks').value = student.marks;
            }

            select.onchange = function() {
                if (this.value === '__new__') {
                    document.getElementById('newSubject').style.display = 'block';
                } else {
                    document.getElementById('newSubject').style.display = 'none';
                }
            };

            // If only "Add new subject..." is present, show the input immediately
            if (select.options.length === 1 && select.options[0].value === '__new__') {
                select.selectedIndex = 0;
                document.getElementById('newSubject').style.display = 'block';
            }
        })
        .catch(() => {
            document.getElementById('modalError').innerText = 'Failed to load subjects. Please try again.';
        });
}

// Close Modal
function closeModal() {
    document.getElementById('studentModal').style.display = 'none';
}

// Attach Edit/Delete handlers to table buttons
function attachTableButtonListeners() {
    document.querySelectorAll('.editBtn').forEach(btn => {
        btn.onclick = function() {
            let tr = btn.closest('tr');
            openModal(true, {
                id: tr.dataset.id,
                name: tr.querySelector('.student-name').innerText,
                subject: tr.querySelector('.subject-cell').innerText,
                marks: tr.querySelector('.marks').innerText
            });
        };
    });
    document.querySelectorAll('.deleteBtn').forEach(btn => {
        btn.onclick = function() {
            let tr = btn.closest('tr');
            let id = tr.dataset.id;
            if (confirm('Are you sure you want to delete this student?')) {
                fetch(`/delete_student/${id}/`, {
                    method: 'POST',
                    headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'deleted') {
                        location.reload();
                    } else {
                        alert('Failed to delete student.');
                    }
                })
                .catch(() => {
                    alert('Server error. Please try again.');
                });
            }
        };
    });
}

// Form submit handler
function studentFormSubmitHandler(e) {
    e.preventDefault();
    let name = document.getElementById('name').value.trim();
    let subject = document.getElementById('subject').value;
    if (subject === '__new__') {
        subject = document.getElementById('newSubject').value.trim();
    }
    let marks = document.getElementById('marks').value;
    let errorDiv = document.getElementById('modalError');
    errorDiv.innerText = '';
    errorDiv.className = 'warning';

    // Name validation
    if (!validateStudentName(name)) {
        errorDiv.innerText =
            'Name should have at least one word, each word starting with a capital letter (e.g., "Arun", "Arun Kumar","Arunkumar S").';
        return;
    }

    // Marks validation: must be a number (no upper/lower bound)
    if (marks === '' || isNaN(Number(marks))) {
        errorDiv.innerText = 'Marks must be a number.';
        return;
    }

    let url = editing ? `/edit_student/${editingId}/` : '/add_student/';
    let method = 'POST';
    let payload = JSON.stringify({name, subject, marks});
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: payload
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'created' || data.status === 'updated' || data.status === 'success') {
            location.reload();
        } else {
            errorDiv.innerText = data.message || 'Error!';
        }
    })
    .catch(() => {
        errorDiv.innerText = 'Server error. Please try again.';
    });
}

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    // Add Student button
    document.getElementById('addStudentBtn').onclick = () => openModal(false);

    // Attach listeners to Edit/Delete buttons
    attachTableButtonListeners();

    // Modal form submit
    document.getElementById('studentForm').onsubmit = studentFormSubmitHandler;
});
