import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

def downloadVideo(link, id):
    cookies = {
        '_ga': 'GA1.1.215585002.1718159802',
        'arp_scroll_position': '0',
        '__gads': 'ID=77aab3245bfcb6ee:T=1718159802:RT=1719747903:S=ALNI_MZ3ASMe7SgQp5jlETp_QC0LGljEug',
        '__gpi': 'UID=00000e58286c3517:T=1718159802:RT=1719747903:S=ALNI_MZXbC5jyoBAV0FVSzXjaKRBEhLw_A',
        '__eoi': 'ID=4aa2bfa5d4131212:T=1718159802:RT=1719747904:S=AA-AfjZed3VeCKjdFLDoXNgIKZOf',
        'FCNEC': '%5B%5B%22AKsRol8pT18u2qqHgiSviJFjNFh2ovp6ul0MboApSKCVYXcY_RC51BvO1y3gIj7yj2in_FYnE-GxMP0H7JmjDz7FhFuGknilBX4XMlBtuVXiijGD195ko_ChMsXvR1ZNJJvFexMe0WVgCUimrckAI1CuGQPAm5B2eg%3D%3D%22%5D%5D',
        '_ga_ZSF3D6YSLC': 'GS1.1.1719747560.4.1.1719747914.0.0.0',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'hx-current-url': 'https://ssstik.io/how-to-download-tiktok-video-1',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'priority': 'u=1, i',
        'referer': 'https://ssstik.io/how-to-download-tiktok-video-1',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'cFdMZkw3',
    }

    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")

    try:
        downloadLink = downloadSoup.a["href"]
        videoTitle = downloadSoup.p.getText().strip()
    except Exception as e:
        print(f"Error extracting download link: {e}")
        return

    # Ensure the directory exists
    os.makedirs('videos', exist_ok=True)

    print("STEP 5: Saving the video :)")
    try:
        mp4File = urlopen(downloadLink)
        with open(f"videos/{id}-{videoTitle}.mp4", "wb") as output:
            while True:
                data = mp4File.read(4096)
                if data:
                    output.write(data)
                else:
                    break
    except Exception as e:
        print(f"Error downloading video: {e}")

print("STEP 1: Open Chrome browser")
options = Options()
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=options)
#Enter Tiktok ID url here
driver.get("url")

print("Please solve the reCAPTCHA manually, then press Enter to continue...")
input()  # Wait for user to solve reCAPTCHA

scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")
i = 1

print("STEP 2: Scrolling page")
while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    if (screen_height) * i > scroll_height:
        break 
#KIN class name Add the Class Code of Titkot ID. The first part of ID
className = "css-at0k0c-DivWrapper"
script  = "let l = [];"
script += "Array.from(document.getElementsByClassName(\""
script += className
script += "\")).forEach(item => { l.push(item.querySelector('a').href)});"
script += "return l;"

urlsToDownload = driver.execute_script(script)

print(f"STEP 3: Time to download {len(urlsToDownload)} videos")
for index, url in enumerate(urlsToDownload):
    print(f"Downloading video: {index}")
    downloadVideo(url, index)
    time.sleep(10)

driver.quit()
