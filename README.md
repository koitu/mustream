# mustream
Music streaming and uploading service that exposes a RESTful API

### Dependencies
Create virtualenv and install dependencies
```sh
python3 -m venv mustream-venv
. mustream-venv/bin/activate
pip install -r requirements.txt
```

### Quickstart
cd into the folder with manage.py 
```sh
python manage.py generate_secret_key --replace
python manage.py makemigrations catalog
python manage.py migrate
python manage.py createsuperuser --username admin
python manage.py runserver
```
Then vist http://127.0.0.1:8000/

### To Do
- Web client
#### high priority
- update TrackSerializer based on new Track Model
- finish SimpleTrackSerializer
- Finish UserSerializer and add view to urls
	- limit for space each user can use
- update urls
- test playlists
- allow users to bookmark other users playlists
	- will need to create another field in userprofile

#### med priority
- limit size of image and audio uploads (different limits for user and staff)
- pagementation
- techinial metadata (streaminfo ex. format, sample rate, channels, bitrate ...)
- custom login and logout (https://github.com/encode/django-rest-framework/blob/master/rest_framework/urls.py)
- add static files to database
	- might need to rewrite models with (https://www.geeksforgeeks.org/filepathfield-django-models/)
	- would also need to serve file (possible need to write second app)
- switch primary key from id to UUID (https://tech.serhatteker.com/post/2020-01/uuid-primary-key/)
- download file https://stackoverflow.com/questions/2681338/django-serving-a-download-in-a-generic-view
- add support for track to belong to multiple genres (and maybe artists) (but not albums)

#### low priority 
- cli client
- add youtube playlists and server will autodl
- auto updating user playlist with all tracks (readonly)
- allow user to add every track in a artist/album/genre to a playlist
