document.addEventListener('DOMContentLoaded', function() {
    const editPostForm = document.getElementById('editPostForm');

    if (editPostForm) {
        editPostForm.addEventListener('submit', function(e) {
            e.preventDefault(); 

            const postIdElement = document.getElementById('postId');  

            // Ensure postId is set correctly
            if (!postIdElement || !postIdElement.value) {
                console.error('Post ID not found or invalid');
                return;
            }

            const postId = postIdElement.value;  

            // Capture the values from the form
            const titleElement = document.getElementById('id_title');
            const contentElement = document.getElementById('id_content');

            if (!titleElement || !contentElement) {
                console.error('One of the form fields was not found in the DOM');
                return;
            }

            // Get the form data
            const title = titleElement.value;
            const content = contentElement.value;  

            // Send the PUT request to update the post
            fetch(`/api/posts/${postId}/`, {
                method: 'PUT',  
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,  
                },
                body: JSON.stringify({
                    title: title,
                    content: content,
                }),
            })
            .then(response => {
                if (response.ok) {
                   
                    window.location.href = '/profile/';  
                } else {
                    return response.json().then(err => { throw err; });
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});
