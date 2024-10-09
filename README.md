# Blog Application

The Blog Application offers a range of features designed to enhance the user experience, including user signup and login with JWT-based authentication for secure access. Users can create, edit, and delete their blog posts with rich text formatting provided by CKEditor. Additionally, the application allows users to view all published posts, edit their profile information, and search for specific posts using keywords. An admin panel is available for administrators to manage users and posts effectively. Overall, this application provides a seamless platform for content creation and sharing.

## Project Overview

- **Framework**: Django
- **Database**: MySQL
- **Authentication**: JWT (JSON Web Token) with `rest_framework_simplejwt`
- **Text Editor**: CKEditor for rich text editing
- **Deployment**: Microsoft Azure
- **Containerization**: Docker for encapsulating the app

## Setup and Installation Steps

### Prerequisites

- Python 3.11
- Docker and Docker Compose
- MySQL (if running locally without Docker)
- Azure CLI (if deploying to Azure)
  
### Local Setup (Without Docker)

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/blog_application.git
    cd blog_application
    ```

2. Set up a virtual environment:
    ```bash
    python -m venv blog_env
    source blog_env/bin/activate   # On Windows: blog_env\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables in a `.env` file:
    ```plaintext
    SECRET_KEY=your-secret-key
    DEBUG=True
    DATABASE_NAME=blog_db
    DATABASE_USER=root
    DATABASE_PASSWORD=yourpassword
    DATABASE_HOST=localhost
    DATABASE_PORT=3306
    ```

5. Run database migrations:
    ```bash
    python manage.py migrate
    ```

6. Create a superuser for accessing the admin panel:
    ```bash
    python manage.py createsuperuser
    ```

7. Run the development server:
    ```bash
    python manage.py runserver
    ```

Access the app at `http://localhost:8000`.

### Setup with Docker

1. Build the Docker image:
    ```bash
    docker build -t blog_app .
    ```

2. Run the Docker container:
    ```bash
    docker-compose up
    ```

3. Migrate the database:
    ```bash
    docker-compose exec web python manage.py migrate
    ```

4. Create a superuser:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

Access the app at `http://localhost:8000`.

## API Documentation

### REST API Endpoints (JWT-based authentication)

- **Authentication:**
    - `POST /api/token/` - Obtain JWT tokens.
    - `POST /api/token/refresh/` - Refresh the access token.

- **Blog Endpoints:**
    - `GET /api/posts/` - Retrieve a list of all blog posts.
    - `POST /api/posts/` - Create a new blog post (authenticated users only).
    - `GET /api/posts/<id>/` - Retrieve a single blog post by ID.
    - `PUT /api/posts/<id>/` - Update a blog post (authenticated users only).
    - `DELETE /api/posts/<id>/` - Delete a blog post (authenticated users only).

- **User Endpoints:**
    - `GET /api/users/` - List all users.
    - `POST /api/register/` - Register a new user.

## Deployment Steps (Microsoft Azure)

### Prerequisites

- An Azure account
- Azure CLI installed and logged in

### Deployment Process

1. **Create an Azure Container Registry**:
    ```bash
    az acr create --resource-group myResourceGroup --name blogapp18 --sku Basic
    ```

2. **Log in to the registry**:
    ```bash
    az acr login --name blogapp18
    ```

3. **Tag and push the Docker image to ACR**:
    ```bash
    docker tag blog_app blogapp18.azurecr.io/blog_app:v1
    docker push blogapp18.azurecr.io/blog_app:v1
    ```

4. **Create a Web App on Azure**:
    ```bash
    az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name blogAppWeb --deployment-container-image-name blogapp18.azurecr.io/blog_app:v1
    ```

5. **Enable logging and monitoring (Application Insights)**:
    ```bash
    az webapp log config --name blogAppWeb --resource-group myResourceGroup --application-logging true
    ```

6. **Apply necessary environment variables on Azure**:
    - In the Azure portal, go to your Web App's "Configuration" and add your environment variables (e.g., `SECRET_KEY`, `DATABASE_URL`, etc.).

7. **Access the deployed app**:
    - The app will be available at `https://myblogapp.azurewebsites.net`.


