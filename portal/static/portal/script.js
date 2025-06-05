// Modal logic
let editing = false;
let editingId = null;

// Name validation: "Arun S S" or "Arun S", initials single uppercase, no dots, space-separated
function validateStudentName(name) {
    const parts = name.trim().split(/\s+/);
    if (parts.length < 2) return false;
    if (!/^[A-Z][a-z]+$/.test(parts[0])) return false; // First name
    for (let i = 1; i < parts.length; i++) {
        if (!/^[A-Z]$/.test(parts[i])) return false; // Initials
    }
    return true;
}

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
            // If there are no subjects, show only "Add new subject..."
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

            // Always attach the event handler after options are set
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

function closeModal() {
    document.getElementById('studentModal').style.display = 'none';
}

document.getElementById('addStudentBtn').onclick = () => openModal(false);

// Attach edit/delete handlers after DOM is loaded
window.onload = function() {
    document.querySelectorAll('.editBtn').forEach(btn => {
        btn.onclick = function() {
            let tr = btn.closest('tr');
            openModal(true, {
                id: tr.dataset.id,
                name: tr.querySelector('.name').innerText,
                subject: tr.querySelector('.subject').innerText,
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
};

// Handle form submit with name validation and warning
document.getElementById('studentForm').onsubmit = function(e) {
    e.preventDefault();
    let name = document.getElementById('name').value.trim();
    let subject = document.getElementById('subject').value;
    if (subject === '__new__') {
        subject = document.getElementById('newSubject').value.trim();
    }
    let marks = document.getElementById('marks').value;

    // Name validation
    if (!validateStudentName(name)) {
        document.getElementById('modalError').innerText =
            'Name should be like "Arun S S" or "Arun S". Initials must be single uppercase letters with spaces, no dots.';
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
            document.getElementById('modalError').innerText = data.message || 'Error!';
        }
    })
    .catch(() => {
        document.getElementById('modalError').innerText = 'Server error. Please try again.';
    });
};
