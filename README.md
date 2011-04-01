This is a set of python scripts that transcode media files between some common formats. 

## Notes
* Scripts detect the number of CPU cores and will transcode multiple files in parallel.
* Scripts are called without arguments and will transcode all files in the current directory that have a given extension (e. g. flactomp3.py will transcode \*.flac to \*.mp3).
* Scripts depend on binary tools in your path (e.g. MP3 support requires LAME).

## To Do
* Factor out baseline transcoder functionality.
