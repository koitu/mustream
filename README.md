# mustream

__Status:__ not working

## Quickstart
cd into the folder with manage.py 
```
python manage.py generate_secret_key --replace
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
- enable streaming
- update permissions
- extend User
- api root
- returning more metadata in TrackDetail
- response when put or post in TrackList
- deal with duplicate file names 
- limit size of image and audio uploads (different limits for user and staff)

## med priority
- pagementation
- caching
- Web client
- watch folder and automatically update database on file change
- switch primary key from id to UUID (https://tech.serhatteker.com/post/2020-01/uuid-primary-key/)
- multiple artist, album, genre per track (no promises for this)
- limit for space each user can use

## low priority
- cli client (?)
- add youtube playlists and server will autodl
