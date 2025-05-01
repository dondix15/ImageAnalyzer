
import os
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.shortcuts import render
from .forms import UploadFileForm
#views.py handles the file upload
def home(request):
    return HttpResponse("Welcome to ImageAnalyzer!")

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        return HttpResponse(f"name of uploaded file is {str(file)}")
    else:
        form = UploadFileForm()
        #return render(request, 'upload_success.html', {'file_path': full_path})
    return render(request, 'analyzer_app/upload.html', {'form': form})

