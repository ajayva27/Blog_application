document.addEventListener('DOMContentLoaded', function () {
    let postIdToDelete;

    const deleteButtons = document.querySelectorAll('.deletePost');
    const deleteModal = document.getElementById('deleteModal');
    const confirmDeleteButton = document.getElementById('confirmDelete');
    const cancelDeleteButton = document.getElementById('cancelDelete');

    // Show the modal when the delete button is clicked
    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            postIdToDelete = button.getAttribute('data-post-id');
            deleteModal.classList.remove('hidden');  
        });
    });

    // Hide the modal when cancel is clicked
    cancelDeleteButton.addEventListener('click', function () {
        deleteModal.classList.add('hidden');  
    });

    // Handle delete confirmation
    confirmDeleteButton.addEventListener('click', function () {
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        fetch(`/api/posts/${postIdToDelete}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                deleteModal.classList.add('hidden');  
                location.reload();  
            } else {
                return response.text().then(errorText => {
                    console.error('Delete error:', errorText);  
                    alert('Failed to delete post. Please try again.');
                });
            }
        })
        .catch(error => {
            console.error('Network error:', error);  
            alert('An error occurred. Please try again.');
        });
    });
});
