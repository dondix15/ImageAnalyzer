import os
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import render
from .forms import UploadFileForm

# views.py handles the file upload
def home(request):
    return HttpResponse("Welcome to ImageAnalyzer!")

def upload_file(request):
    # Delete previous images before uploading a new one
    delete_previous_images()

    file_url = None

    if request.method == 'POST':
        print("file url is ", file_url)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
            filename = fs.save(file.name, file)
            file_url = fs.url(filename)  # Get the URL of the uploaded file
        else:
            print("Form is not valid")
    else:
        form = UploadFileForm()

    print(f"file url: {file_url}")
    return render(request, 'analyzer_app/upload.html', {'form': form, 'file_url': file_url})

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
