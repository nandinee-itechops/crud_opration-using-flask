function populateEditForm(employeeId) {
    fetch(`/edit/${employeeId}`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => {
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error('Received non-JSON response from server');
        }
        return response.json();
    })
    .then(result => {
        if (result.status === 'error') {
            throw new Error(result.message);
        }
        
        const employee = result.data;
        document.getElementById('editId').value = employee.id;
        document.getElementById('editName').value = employee.name;
        document.getElementById('editEmail').value = employee.email;
        document.getElementById('editPhone').value = employee.phone;
        document.getElementById('editAddress').value = employee.address;
        document.getElementById('editDob').value = employee.dob;
        document.getElementById('editPosition').value = employee.position;
        
        new bootstrap.Modal(document.getElementById('editModal')).show();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error fetching employee data: ' + error.message);
    });
}

document.getElementById('editEmployeeForm').addEventListener('submit', function(event) {
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
    const id = document.getElementById('editId').value;
    
    fetch(`/edit/${id}`, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.message || 'Update failed');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            const modal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
            modal.hide();
            document.body.classList.remove('modal-open');
            const modalBackdrops = document.querySelectorAll('.modal-backdrop');
            modalBackdrops.forEach(backdrop => backdrop.remove());
            
            showAlert('Employee Updated Successfully!');
            setTimeout(() => location.reload(), 1000);
        } else {
            throw new Error(data.message || 'Error updating employee');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error updating employee: ' + error.message, 'danger');
    });
});

document.getElementById('editName').addEventListener('input', function() {
    if (!validateName(this.value)) {
        this.setCustomValidity('Name should contain only letters and spaces');
        this.reportValidity();
    } else {
        this.setCustomValidity('');
    }
});

document.getElementById('editPhone').addEventListener('input', function() {
    if (!validatePhone(this.value)) {
        this.setCustomValidity('Phone number should be exactly 10 digits');
        this.reportValidity();
    } else {
        this.setCustomValidity('');
    }
});
