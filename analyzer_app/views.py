import os
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import redirect, render

from imageAnalyzer.settings import BASE_DIR
from .forms import UploadFileForm
from analyzer_app.process_image import FilterImage

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/media/'
# views.py handles the file upload
def home(request):
    return render(request, "analyzer_app/homepage.html")

def upload_file(request):
    delete_previous_images()
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES["file"]

        if form.is_valid():
            image_processing = FilterImage(MEDIA_ROOT, file, 55, 30, 20, "veg")
            image_processing.run()

            file.seek(0)

            image_processing = FilterImage(MEDIA_ROOT, file, 30, 100, 150, "urban")
            image_processing.run()

            file.seek(0)

            image_processing = FilterImage(MEDIA_ROOT, file, 70, 40, 20, "soil")
            image_processing.run()
            # Use FileSystemStorage to save files to the /uploads directory

            
            # After uploading, return the homepage
            return redirect('show_images')
    else:
        form = UploadFileForm()
    
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

import os
from django.conf import settings
from django.shortcuts import render

def show_images(request):
    directory_path = settings.MEDIA_ROOT
    filtered_images = []

    # Categorize images based on suffix
    soil_images = []
    urban_images = []
    veg_images = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".png"):
            file_path = os.path.join(directory_path, filename)

            if "soil" in filename.lower():
                soil_images.append(filename)
            elif "urban" in filename.lower():
                urban_images.append(filename)
            elif "veg" in filename.lower():
                veg_images.append(filename)

    # Combine them in the desired order
    filtered_images = soil_images + urban_images + veg_images

    return render(request, "analyzer_app/show_images.html", {
        "filtered_images": filtered_images
    })

    return render(request, 'analyzer_app/show_images.html', {'filtered_images': filtered_images})