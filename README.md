# mustream

__Status:__ core functions are working

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
## high priority
- update permissions
- extend User
- returning more metadata in TrackDetail
- limit size of image and audio uploads (different limits for user and staff)

## med priority
- pagementation
- caching
- Web client
- watch folder and automatically update database on file change
- switch primary key from id to UUID (https://tech.serhatteker.com/post/2020-01/uuid-primary-key/)
- download file https://stackoverflow.com/questions/2681338/django-serving-a-download-in-a-generic-view
- multiple artist, album, genre per track (no promises for this)
- limit for space each user can use

## low priority
- cli client (?)
- add youtube playlists and server will autodl
