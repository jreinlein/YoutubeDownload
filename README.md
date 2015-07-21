# YoutubePlaylistDownload
## Description
A small script which automates the downloading of videos off YouTube as MP3 files.  
Works for single songs, mixes, and playlists.  
Organizes the files into an appropriately-named folder when downloading mixes and playlists.
## Instructions
1. Ensure you have Python 3.x installed (script written in 3.4.3.)  
2. Download the _selenium_ package using __pip install selenium__ in the console  
3. Copy the YouTube URL into a file named __url.txt__ in the same directory as the script
4. Run the .py script and allow the downloads to complete before closing browser
5. Enjoy!  

## Dependencies
* Python 3
* Selenium
* Firefox  

## Future Plans
* Test functionality on Linux/Mac
* Test funtionality on non-English YT
* Improve UX (error messages)
* Add support for:
  - :white_check_mark: Mixes (different from playlists)
  - URL of the playlist itself (rather than video in playlist)
  - :white_check_mark: Single songs
  - Multiple URLs in file
