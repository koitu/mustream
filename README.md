# mustream

__Status:__ Might be broken

## Quickstart
cd into the folder with manage.py 
```
python manage.py generate_secret_key --replace
python manage.py makemigrations catalog
python manage.py migrate
python manage.py createsuperuser --username admin
python manage.py runserver
```
Then vist http://127.0.0.1:8000/

## Requirements
- django
- djangorestframework
- django-cleanup
- django-generate-secret-key
- pillow
- audio-metadata

# To Do
- Web client
## high priority
- update TrackSerializer based on new Track Model
- finish SimpleTrackSerializer
- Finish UserSerializer and add view to access
	- limit for space each user can use
- update urls
- test playlists
- allow users to bookmark other users playlists
	- will need to create another field in userprofile

## med priority
- limit size of image and audio uploads (different limits for user and staff)
- pagementation
- techinial metadata (streaminfo ex. format, sample rate, channels, bitrate ...)
- custom login and logout (https://github.com/encode/django-rest-framework/blob/master/rest_framework/urls.py)
- add static files to database
	- might need to rewrite models with (https://www.geeksforgeeks.org/filepathfield-django-models/)
	- another way could be to change the upload to locations instead
	- would also need to serve file (how to design url?)
	- how to secure this? (write a second app to serve files?)
- switch primary key from id to UUID (https://tech.serhatteker.com/post/2020-01/uuid-primary-key/)
- download file https://stackoverflow.com/questions/2681338/django-serving-a-download-in-a-generic-view
- add support for track to belong to multiple genres (and maybe artists) (but not albums)

## low priority 
- cli client
- add youtube playlists and server will autodl
- auto updating playlist with all your tracks (readonly)
- play random track from album/genre/artist/all tracks
- allow user to add every track in a artist/album/genre to a playlist
