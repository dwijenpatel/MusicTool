Tool to organize really big music collections and break them up into genre folders
----

4 step process:


1)Load as much metadata as possible for every mp3 

 -Use MusicBrainz mostly

 -Try using other id3 tag filler services for unidentified mp3s


2)Move mp3s to artist subfolders based on id3 tag "artistsortname".

 -Avoid having lots of artist folders that start with "The", e.g. "Doors, The" instead of "The Doors"

 -Avoid lower/uppercase annoyances

 -Avoid dealing with "feat." issues.  The "artistsortname" will not include the "featuring [OtherArtist]" that "artistname" has


3)scan "genre" id3 tags for each song in an artist folder to determine the artists' musical genre.

 -Get all the genre tags that are applied to each song in the current artistfolder's directory.

 -Make a determination on the artist's musical genre based on the frequency of the various unique genre tags.

4)move artist folders to genre folders based on user specified genre tag groups

 -e.g. the genre folder I am creating for "Dance" will include artists that are tagged unders the genres: acid, beat, club, techno, techno, trance, etc.



Typical Use Case for a big messy music collection:
----

PART 1:

-run musicbrainz picard

-add all of your unsorted music ("add folder")

-run "scan" to identify mp3s

-Options -> File naming

-check the "move files to this directory when saving" and choose the "global root directory" of your music collection

-under the "Name files like this" field, paste this:
%albumartistsort%/%artist% - %album% - $num(%tracknumber%,2) - %title%

e.g. "Beatles, The/The Beatles - Revolver - 01 - Taxman.mp3"

-select all identified songs and click "save".


PART 2:

-Decide on your major genre folders and the associated tags with those genres. Create a json file to reflect this. See GenreSetup.json

-Run: "python musicfolders.py [musicsourcedir] [genre-info.json] > [artistMoves.json]".

-Run: "python MoveToGenreDirs.py [artistMoves.json]".




