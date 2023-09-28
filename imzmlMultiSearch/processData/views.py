from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm, ModelFormWithFileField
from .models import ModelFormWithFileField

#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

'''def handle_uploaded_file(f):
    with open("name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)'''

def index(request):
    if request.method == "POST":
        form = ModelFormWithFileField(request.POST, request.FILES)
        if form.is_valid():
            instance = ModelWithFileField(file_field=request.FILES["file"])
            instance.save()
            return HttpResponseRedirect("/success/url/")
    else:
        form = ModelFormWithFileField()
    return render(request, "processData/upload.html", {"form": form})
            
'''def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            return HttpResponseRedirect("/success/url/")
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})'''
