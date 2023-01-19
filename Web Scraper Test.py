import requests
import time
import wget
from urllib.error import HTTPError

# Base of the URL that we use to request from AO3
BaseURL = "https://archiveofourown.org/downloads/"

# To iterate this number, it has to be an integer, but needs to be converted into a string to put into the URL
# Keeping both versions separate to make checking easier, then should convert it into one variable once I know wtf I'm doing
UniqueID = 1
UniqueIDStr = str(UniqueID)

URLEnd = "/Download.html"

# Possible responses from server listed below:
# Expecting to see 200 for successes, 404 for when the fic is deleted, and 429 when the server is sick of my shit
# The range below is just for testing, adjust as needed. There are 44,349,139 possible URL combinations as of January 17th 2023. Have fun lmao
for UniqueID in range(51927,44349139):
    try:
        #Make the URL, send to server
        URL = BaseURL+UniqueIDStr+URLEnd
        response = requests.get(URL)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'For link {UniqueID} HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'For link {UniqueID} other error occurred: {err}') 
        
        # Specific handling of when the server times you out. Optimal timer, in seconds, appears to be in between 80 and 200.
        # AO3 has no API for this so it's just trial and error
        # If the timing is incorrect, this script downloads a 1Kb file that contains no useful data. Review these to see where the timer is failing
        if response.status_code == 429:
            
            # Timeout pod for bold kiddies and web scrapers
            time.sleep(200)
            
            response = requests.get(URL)
            print(response.status_code)

            # Write the downloaded file to current directory
            open(UniqueIDStr+".html", "wb").write(response.content)
        else: 
            exit
    else:
        # Write the downloaded file to current directory. Yes I nested the same code twice
        print(response.status_code)
        open(UniqueIDStr+".html", "wb").write(response.content)
    finally:
        # Iterate
        UniqueID+= 1
        UniqueIDStr = str(UniqueID)






