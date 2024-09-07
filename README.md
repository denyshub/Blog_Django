# Django Blog Site

This project is a blog site where users can add posts after registration and login.

## Features

- **Registration**: Users can create new accounts.
- **Login**: Users can log into the system.
- **Adding Posts**: After logging in, users can create new posts.
- **Editing and Deleting Posts**: Users can edit and delete only their own posts.
- **Viewing Posts**: All users can view posts.

## Technical Details

The project uses Django to implement all features. SQLite was used for data storage during development but has been switched to PostgreSQL.

## Steps to Run the Project

1. **Clone the Project from GitHub**
   - Create any folder.
   - Navigate to it and run:
     ```bash
     git clone https://github.com/denyshub/Blog_Django.git
     ```

2. **Set Up the Virtual Environment and Install Dependencies**
   - Navigate to the project folder:
     ```bash
     cd Blog_Django
     ```
   - Create and activate a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # For Windows: venv\Scripts\activate
     ```
   - Install the required dependencies:
     ```bash
     pip install -r petblog/requirements.txt
     ```

3. **Apply Migrations and Start the Server**
   - Navigate to the root directory of your Django project:
     ```bash
     cd petblog
     ```
   - Apply migrations to set up the database:
     ```bash
     python manage.py migrate
     ```
   - Start the server:
     ```bash
     python manage.py runserver
     ```

4. **Open the Browser**
   - Go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)


