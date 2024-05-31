# report_generator

# Django File Upload and Processing Application

This Django application allows users to upload Excel or CSV files, processes the uploaded files, and generates a summary report grouped by state and DPD (Days Past Due).

## Features

- Upload CSV or Excel files.
- Validate and clean the uploaded data.
- Generate a summary report grouped by state and DPD.
- Display the summary report in a user-friendly format.

## Prerequisites

- Python 3.x
- Django 3.x or later
- pandas

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ajeet1083/report_generator.git
   cd django-file-upload

2. ** Create a virtual environment: **
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`

3. ** Install the required packages: **
    pip install -r requirements.txt

4. ** Set up the Django project: **

5. ** Set up the Django project: **
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver


#  Configuration

Ensure your settings.py has the following configuration for media files:
    # settings.py

    import os

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

Add the following to your project's urls.py to handle media files during development:

    # urls.py

    from django.conf import settings
    from django.conf.urls.static import static
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', include('uploader.urls')),
    ]

    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Usage
Run the Django development server:
    python manage.py runserver
    
Access the upload page:
    Open your web browser and navigate to http://127.0.0.1:8000/upload/.

Upload a file:
    Choose a CSV or Excel file containing the columns Cust State and DPD.
    Click the Upload button.
View the summary report:

The application will process the file and display a summary report grouped by state and DPD.
