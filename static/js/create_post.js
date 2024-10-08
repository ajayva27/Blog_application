document.getElementById('createPostForm').addEventListener('submit', function (event) {
    event.preventDefault(); 

    const postTitle = document.querySelector('[name="title"]').value;  
    const postContent = document.querySelector('#postContent').value;  

    const postData = {
        title: postTitle,
        content: postContent,
    };

    // Fetch API to create post using session-based authentication
    fetch('/api/posts/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), 
        },
        body: JSON.stringify(postData),
        credentials: 'include',  
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(`Error ${response.status}: ${err.detail || err}`);
            });
        }
        return response.json();
    })
    .then(data => {
        
        window.location.href = 'http://127.0.0.1:8000/';
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
});

// Function to retrieve CSRF token
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return decodeURIComponent(value);
        }
    }
    return '';
}
