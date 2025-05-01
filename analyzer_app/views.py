
import os
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import render
from .forms import UploadFileForm
#views.py handles the file upload
def home(request):
    return HttpResponse("Welcome to ImageAnalyzer!")

def upload_file(request):
    file_url = None
    delete_previous_images()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
            filename = fs.save(file.name, file)
            file_url = fs.url(filename)
        #return 3 urls of the files. pass that to render 
    else:
        print("else statement")
        form = UploadFileForm()
        request.session.pop('file_url', None)
        
    print(f"file url: {file_url}")
    return render(request, 'analyzer_app/upload.html', {'form': form, 'file_url': file_url})
 
def delete_previous_images():
     directory_path = os.getcwd()
     for filename in os.listdir(directory_path + "/uploads"):
            file_path = os.path.join(directory_path, filename)
            # Check if it is a file (not a subdirectory)
            if os.path.isfile(file_path):
                #os.remove(file_path)  # Delete the file
                print(f"Deleted: {file_path}")
