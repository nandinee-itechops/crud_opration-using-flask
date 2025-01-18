document.getElementById('addEmployeeForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const name = this.elements['name'].value;
    const email = this.elements['email'].value;
    const phone = this.elements['phone'].value;

    if (!validateName(name)) {
        showAlert('Name should contain only letters and spaces', 'danger');
        return;
    }

    if (!validateEmail(email)) {
        showAlert('Please enter a valid email address', 'danger');
        return;
    }

    if (!validatePhone(phone)) {
        showAlert('Phone number should be exactly 10 digits', 'danger');
        return;
    }

    const formData = new FormData(this);
    fetch('/add', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const modal = bootstrap.Modal.getInstance(document.getElementById('addModal'));
            modal.hide();
            document.body.classList.remove('modal-open');
            const modalBackdrops = document.querySelectorAll('.modal-backdrop');
            modalBackdrops.forEach(backdrop => backdrop.remove());
            
            showAlert('Employee Added Successfully!');
            setTimeout(() => location.reload(), 1000);
        } else {
            showAlert(data.message, 'danger');
        }
    });
});

document.getElementById('addName').addEventListener('input', function() {
    if (!validateName(this.value)) {
        this.setCustomValidity('Name should contain only letters and spaces');
        this.reportValidity();
    } else {
        this.setCustomValidity('');
    }
});

document.getElementById('addPhone').addEventListener('input', function() {
    if (!validatePhone(this.value)) {
        this.setCustomValidity('Phone number should be exactly 10 digits');
        this.reportValidity();
    } else {
        this.setCustomValidity('');
    }
});
