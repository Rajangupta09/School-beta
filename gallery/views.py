from django.shortcuts import render, HttpResponse

from .models import Album, Photo, Video
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required
def add_album(request):
	if request.method == "POST":
		album = request.FILES.getlist("album")
		album_name = request.POST.get("album_name")
		for a in album:
			Album.objects.create(album_name=album_name, file=a)
		messages.success(request, 'Album Uploaded Successfully.')
	return render(request, 'gallery/album.html')

@login_required
def add_video(request):
	if request.method == "POST":
		video = request.FILES.get("video")
		video_name = request.POST.get("video_name")
		Video.objects.create(video_name=video_name, file=video)
	return render(request, 'gallery/video.html')
	
@login_required
def add_photo(request):
	if request.method == "POST":
		photo = request.FILES.get("photo")
		photo_name = request.POST.get("photo_name")
		Photo.objects.create(photo_name=photo_name, file=photo)
	return render(request, 'gallery/photo.html')

def gallery(request):
	album = Album.objects.all()
	if request.method == "GET":
		if 'name' in request.GET:
			name = request.GET.get('name')
			temp = Album.objects.filter(album_name=name)
			content = ''
			for i in temp:
				content += '<a href="' + i.file.url + '" data-toggle="lightbox" data-gallery="gallery" class="col-md-3 col-sm-5"><img src="' + i.file.url + '" class="img-fluid rounded "></a>'	
			return HttpResponse(content)
	return render(request, 'gallery/gallery.html', {'photos': Photo.objects.all(), 'albums': album, 'videos' : Video.objects.all()})