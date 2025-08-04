# AI4S Online Test Platform


<!-- Replace the placeholder URL above with a real screenshot of your application's homepage -->

A robust, full-stack web application designed for creating, managing, and taking online assessments, with a primary focus on SAP modules. This platform provides a seamless, role-based experience for students and administrators, featuring a modern UI, a secure backend, and a professional-grade feature set.

---

## ✨ Core Features

This platform is divided into two primary experiences: a feature-rich portal for students and a powerful content management system for administrators.

### 🎓 For Students & Users
*   **Secure Authentication:** User registration and login with support for both username and email. Includes a secure "Forgot Password" flow.
*   **Interactive Test Catalog:** A fully responsive gallery of all published tests with live searching and filtering by category and difficulty.
*   **Detailed Test Previews:** A dedicated "enrollment" page for each test, providing a full description, topics covered, duration, and number of questions before the user begins.
*   **Timed Exam Interface:** A clean, focused, and timed environment for taking tests, complete with a real-time progress bar.
*   **Instant Results & History:** Users see their score and pass/fail status immediately after submission. A personal dashboard tracks their entire test history.

### ⚙️ For Administrators (Staff)
*   **Role-Based Access Control:** A clear distinction between regular users and staff. Administrative pages and controls are completely inaccessible to students.
*   **Front-End Content Management:** Admins can create, manage, and delete tests and questions entirely through the website's UI—no need to use the backend Django Admin for content.
*   **Flexible Question Posting:**
    *   **Manual Entry:** An intuitive form for adding questions and answers one by one.
    *   **Bulk Upload via JSON:** A powerful feature to upload hundreds of questions at once from a structured JSON file.
*   **Admin Dashboard:** A central hub showing platform statistics (total users, tests, attempts) and a live feed of recent user activity.
*   **Manual Publishing Control:** Admins have a toggle switch on each test's management page to manually publish or unpublish it, giving them full control over test visibility.

---

## 🛠️ Technical Stack & Architecture

This project is built on a modern, scalable technology stack designed for performance and maintainability.

| Category      | Technology / Library                                       | Purpose                                            |
|---------------|------------------------------------------------------------|----------------------------------------------------|
| **Backend**   | Django, Python                                             | Core web framework and language                    |
|               | Gunicorn                                                   | Production WSGI server                             |
|               | PostgreSQL                                                 | Production-grade relational database               |
|               | `django-decouple`, `dj-database-url`                         | Secure management of environment variables         |
|               | `Pillow`, `django-imagekit`                                  | Automatic image resizing and processing            |
| **Frontend**  | HTML5, CSS3, JavaScript (ES6)                              | Core web technologies                              |
|               | Font Awesome                                               | Iconography                                        |
|               | Google Fonts (`Lexend`, `Inter`)                             | Professional typography                            |
| **DevOps**    | Docker                                                     | Containerization for consistent environments       |
|               | Google Cloud Platform (GCP)                                | Cloud hosting                                      |
|               | ↳ **Cloud Run**                                            | Serverless container hosting                       |
|               | ↳ **Cloud SQL**                                            | Managed PostgreSQL database                        |
|               | ↳ **Cloud Storage**                                        | Static and media file storage                      |
|               | ↳ **Artifact Registry**                                    | Private Docker image storage                       |
|               | Nginx                                                      | Web server and reverse proxy                       |
|               | Git & GitHub                                               | Version control                                    |

---

## 🚀 Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

*   Python (3.10+ recommended)
*   Git

### Local Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/YourUsername/YourRepo.git]
    cd YourRepo
    ```

2.  **Create and activate a Python virtual environment:**
    ```sh
    # For Mac/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up your local environment variables:**
    *   Create a file named `.env` in the project root.
    *   Copy the contents of `.env.example` (if provided) or add the following, adjusting as needed:
    ```env
    SECRET_KEY="a-strong-local-secret-key"
    DEBUG=True
    ALLOWED_HOSTS="127.0.0.1,localhost"
    # For local development, you can use SQLite by leaving DATABASE_URL blank
    DATABASE_URL=""
    ```

5.  **Apply the database migrations:**
    ```sh
    python manage.py migrate
    ```

6.  **Create a superuser to access the admin panel:**
    ```sh
    python manage.py createsuperuser
    ```
    (Follow the prompts to create your admin account).

7.  **Run the development server:**
    ```sh
    python manage.py runserver
    ```

8.  Open your browser and navigate to `http://127.0.0.1:8000`.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page]([https://github.com/YourUsername/YourRepo/issues]).

## 📜 License

This project is licensed under the [MIT License](LICENSE.txt).
<!-- You would need to create a LICENSE.txt file for this link to work -->
