import os
from django.conf import settings
from django.shortcuts import render
from .forms import UploadFileForm
import pandas as pd

def handle_uploaded_file(f):
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'report_generator')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    file_path = os.path.join(upload_dir, f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path

def process_file(file_path):
    try:
        # Determine file extension and read the file accordingly
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Print the columns for debugging
        print("Columns in the uploaded file:", df.columns.tolist())
        
        # Rename columns if needed
        if 'Cust State' in df.columns:
            df = df.rename(columns={'Cust State': 'State'})
        
        # Check if the expected columns are present
        if 'State' not in df.columns or 'DPD' not in df.columns:
            raise ValueError("The uploaded file does not contain the required columns 'State' and 'DPD'.")

        # Remove any leading/trailing whitespace in the data
        df['State'] = df['State'].str.strip()
        df['DPD'] = df['DPD'].astype(str).str.strip()

        # Handle missing or null values
        df.dropna(subset=['State', 'DPD'], inplace=True)

        # Convert DPD to numeric, coercing errors
        df['DPD'] = pd.to_numeric(df['DPD'], errors='coerce')
        
        # Drop rows with invalid DPD values
        df.dropna(subset=['DPD'], inplace=True)
        df['DPD'] = df['DPD'].astype(int)

        # Group by 'State' and 'DPD', and count occurrences
        summary = df.groupby(['State', 'DPD']).size().reset_index(name='Count')
        
        # Sort the summary DataFrame by 'State' and then by 'DPD' within each state group
        summary = summary.sort_values(by=['State', 'DPD'])
        


        # Convert the summary to a list of dictionaries
        summary_dict = summary.to_dict(orient='records')
        
        return summary_dict
    except Exception as e:
        print(f"Error processing file: {e}")
        return []

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = handle_uploaded_file(request.FILES['file'])
            summary = process_file(file_path)
            return render(request, 'report_app/summary.html', {'summary': summary})
    else:
        form = UploadFileForm()
    return render(request, 'report_app/file_upload.html', {'form': form})
