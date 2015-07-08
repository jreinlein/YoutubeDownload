# Author: James Reinlein (2015)
import os
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = ""
folder = "Downloaded Playlist"

def main():
    # get URL from clipboard then run
    global url
    r = tk.Tk()
    url = r.selection_get(selection="CLIPBOARD")
    r.destroy()
    download(webdriver.Firefox())
    
    
def profileSetup(playlistName):
    # Download Preference setup
    profile = webdriver.FirefoxProfile()
    
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'audio/mpeg')
    profile.set_preference('browser.download.dir', os.getcwd() + '\\' + playlistName)

    return profile
        
     
def download(driver):
    print('Getting video URLs...', end=" ")
    downloadLink = 'http://www.youtube-mp3.org/'
    yt = 'https://www.youtube.com/watch?v='

    driver.get(url)
		
    # get all URLs
    playlist = driver.find_element_by_id("playlist-autoscroll-list")

    items = playlist.find_elements(By.TAG_NAME, value='li')
    urls = []
    for item in items:
            urls.append(item.get_attribute('data-video-id'))

    # get playlist title and set DL path
    title = driver.find_element_by_class_name("playlist-title").text
    if not os.path.exists(os.getcwd() + '\\' + title): os.makedirs(title)

    # close driver and open up new one with proper download settings
    print("Done!")
    driver.close()
    print('Starting downloads...', end="")
    
    profile = profileSetup(title)
    driver = webdriver.Firefox(profile)

    driver.get(downloadLink)

    for link in urls:
        elem = driver.find_element_by_id('youtube-url')
        elem.clear()
        elem.send_keys(yt + link)
        elem.send_keys(Keys.RETURN)

        downloads = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'success')))

        dlLink = driver.find_element_by_link_text('Download')
        dlLink.click()
        #break # USED FOR TESTING PURPOSES
    print("Done! Please allow downloads to finish.")

'''
def checkURL(url):
    if 'youtube.com' or '&list=' not in url[:]:
        print('Failure')
'''

main()
# check functionality on BIG playlists (50+ songs)
