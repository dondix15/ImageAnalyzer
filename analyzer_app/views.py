import os
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import render

from imageAnalyzer.settings import BASE_DIR
from .forms import UploadFileForm


MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/media/'
# views.py handles the file upload
def home(request):
    return render(request, "analyzer_app/homepage.html")
from django.shortcuts import render
from .forms import UploadFileForm

def upload_file(request):
    delete_previous_images()
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist("file_field")
        
        if form.is_valid():
            # Use FileSystemStorage to save files to the /uploads directory
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            
            for f in files:
                # Save the uploaded file to the /uploads directory
                filename = fs.save(f.name, f)
                uploaded_file_url = fs.url(filename)  # URL of the uploaded file
                
                print(f"File uploaded: {filename}")
            
            # After uploading, return the homepage
            return render(request, "analyzer_app/homepage.html")
    else:
        form = UploadFileForm()
    
    return render(request, "analyzer_app/upload.html", {"form": form})
    
    return render(request, "analyzer_app/upload.html", {"form": form})
def delete_previous_images():
    # Use MEDIA_ROOT to get the correct directory for uploaded files
    directory_path = settings.MEDIA_ROOT
    # Loop through all the files in the directory and delete them
    
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        # Check if it is a file (not a subdirectory)
        if os.path.isfile(file_path):
            os.remove(file_path)  # Delete the file
            print(f"Deleted: {file_path}")

def show_images(request):
    # Get the full path to the uploads directory

    directory_path = settings.MEDIA_ROOT
    # Loop through all the files in the directory and delete them
    filtered_images = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        print(f"filename is {file_path}")
     # List all files in the uploads directory
        
    #     # Check if the file ends with '_filtered.png'
         # if filename.endswith('_filtered.png'):
        filtered_images.append(file_path)  # Add to list if it matches
        
    #     # Optionally, print the filenames for debugging
    #     print(f"filename: {filename}")

    # # Pass the list of filtered images to the template
    return render(request, 'analyzer_app/show_images.html', {'filtered_images': filtered_images})