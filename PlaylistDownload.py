# Author: James Reinlein (2015)
import os
import time
import urllib
# import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = ""

def main():
    # get URL from file
    global url
    f = open('url.txt', 'r')
    url = f.readline()
    validateUrl(url)
    '''
    # get URL from clipboard then run
    global url
    r = tk.Tk()
    url = r.selection_get(selection="CLIPBOARD")
    r.destroy()
    '''
    download(webdriver.Firefox())
    
    
def profileSetup(playlistName):
    # Download Preference setup
    profile = webdriver.FirefoxProfile()
    
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'audio/mpeg')
    if playlistName is None: # single song (same directory)
        profile.set_preference('browser.download.dir', os.getcwd())
    else:
        profile.set_preference('browser.download.dir', os.getcwd() + '\\' + playlistName)

    return profile


     
def download(driver):
    print('Getting video URL(s)...', end=" ")
    downloadLink = 'http://www.youtube-mp3.org/'
    yt = 'https://www.youtube.com/watch?v='

    driver.get(url)
    
    category = getCategory(driver) # single, mix, or playlist

    title = getFolderTitle(driver, category)

    # create folder to hold songs (mixes and playlists only)
    if category != "single":
        title = cleanString(title)
        if not os.path.exists(os.getcwd() + '\\' + title): os.makedirs(title)

    urls = getUrls(driver, category)

    # close driver and open up new one
    print(len(urls), "video(s) found!")
    driver.close()
    print('Starting download(s)...', end=" ")

    # set proper download settings
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
        # break # used for testing purposes
    print("Done!")
    print("Please allow download(s) to finish before closing browser.")


def validateUrl(url):
    s = urllib.parse.urlparse(url)
    if "youtube" not in s.netloc:
        raise ValueError('You failed to provide a YouTube link.')

    if s.path not in ["/watch", "/playlist"]:
        raise ValueError('The YouTube link you have provided is invalid.')
    
def cleanString(string):
    for ch in ['/', '\\', '?', '%', '*', ':', '|', '"', '<', '>', '.']:
        if ch in string:
            string = string.replace(ch, '-')
    return string


def getCategory(driver):
    if "playlist?" in driver.current_url:
        return "playlist-page"
    elif len(driver.find_elements(By.CLASS_NAME, "playlist-info")) < 1:
        return "single"
    else:
        title = driver.find_element_by_class_name("author-attribution").text
        if title.strip().lower() == "by YouTube".lower():
            return "mix"
        else:
            return "playlist"


def getFolderTitle(driver, category):
    if category == "single":
        return None
    elif category == "playlist" or category == "mix":
        return driver.find_element_by_class_name("playlist-title").text
    else: # playlist-page
        return driver.find_element_by_class_name("pl-header-title").text

    


def getUrls(driver, category):
    urls = []
    
    if category == "single":
        url = driver.current_url
        url = url[(url.find("v=") + 2):]
        urls.append(url)
        
    elif category == "mix":
        playlist = driver.find_element_by_id("playlist-autoscroll-list")

        items = playlist.find_elements(By.TAG_NAME, value='li')
        for item in items:
            urls.append(item.get_attribute('data-video-id'))

    else: # playlists and playlist pages
        # navigate to page for playlist
        if category == "playlist":
            driver.find_element_by_class_name("playlist-title").click()
        
        while True:
            try:
                button = WebDriverWait(driver, 3).until(
                      EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Load more')]")))
            except:
                break # nothing left to load

            button.click() # load more
            time.sleep(1) # needed, or else it clicks too quickly and messes up

        # get all URLs
        playlist = driver.find_element_by_id("pl-video-table")
        items = playlist.find_elements(By.TAG_NAME, value='tr')
    
        for item in items:
            urls.append(item.get_attribute("data-video-id"))

    return urls


main()
