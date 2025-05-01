
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
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
        filename = fs.save( file.name, file)
        file_url = fs.url(filename)
        return render(request, 'analyzer_app/showimage.html', {'file_url': file_url})
    else:
        form = UploadFileForm()
        #return render(request, 'upload_success.html', {'file_path': full_path})
    return render(request, 'analyzer_app/upload.html', {'form': form})

