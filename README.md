# Django Blog Site

This project is a blog site where users can add posts after registration and login.

## Features

- **Registration**: Users can create new accounts.
- **Login**: Users can log into the system.
- **Adding Posts**: After logging in, users can create new posts.
- **Editing and Deleting Posts**: Users can edit and delete only their own posts.
- **Viewing Posts**: All users can view posts.

## Technical Details

The project uses Django to implement all features. SQLite is used for data storage during development.

## Steps to Run the Project

1. **Clone the Project from GitHub**
   - Create any folder.
   - Navigate to it and run:
     ```bash
     git clone https://github.com/denyshub/Blog_Django.git
     ```

2. **Set Up the Virtual Environment and Run the Site**
   - Navigate to the project folder:
     ```bash
     cd Blog_Django
     ```
   - Activate the virtual environment:
     ```bash
     .\djvenv\Scripts\activate
     ```
   - Go to the root directory:
     ```bash
     cd petblog
     ```
   - Start the server:
     ```bash
     python manage.py runserver
     ```

3. **Open the Browser**
   - Go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
