# MuStream

design ideas
- add multiple dir that are scanned when updatedb 
- allow file uploads (have no idea when someone will use this lol)
- allow deletion of tracks/albums/genres/artist/user (confirm + retype password)
- editing of database will change the orgianal file?


- each user
	- has a list of dirs to scan
	- has a list of albums + artists + tracks + genres + playlists (able to view and play from each)
		- play from album/artist/all tracks/genre/playlist (shuffle on/off)
	- keep history in session at least
	- ? keep history in db ?
	- keep shuffle on/off in db
	- 
	


apps
- catalog
	- list + details + editing for user/playlist/album/artist/track/genre


requirements
- audio-metadata
- django
- djangorestframework
- pillow
- django-cleanup

something to manage images
something to play audio?
...

## Things to do 

## high prio
how to deal with same file begin uploaded twice (what about songs with same title) 
pagementation
caching
limit size of uploads

## med prio
Web client
Add app to watch files and automatically update database (when detect file change)
switch public from id to UUID (https://tech.serhatteker.com/post/2020-01/uuid-primary-key/)
multiple artist, album, genre per track
limit for space that user can use

## low prio
Could try to make a cli client?
add youtube playlists and server will autodl them for you
