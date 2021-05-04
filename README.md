# mustream

__Status:__ not working

## requirements
- django
- djangorestframework
- django-cleanup
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
- limit size of uploads

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
