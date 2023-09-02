# import external libraries.
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
import os
from datetime import datetime, timedelta

# set xvfb display since there is no GUI in docker container.
# large size to have complete screenshots
display = Display(visible=0, size=(1920, 4*1080))
display.start()

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')



path = "/userdata/pages/"
server = os.environ['WIKI_SERVER']
user = os.environ['WIKI_USERNAME']
password = os.environ['WIKI_PASSWORD']
print(server)

while(True):

    logged_in = False

    try:

        print('start session')
        driver = webdriver.Chrome(options=chrome_options)

        # accept cookies and login
        driver.get(server)
        print("accept cookies")
        screenshot = driver.save_screenshot('/userdata/test1.png')
        banner = driver.find_elements(By.NAME,'disablecookiewarning')
        if len(banner) > 0: banner[0].click()
        screenshot = driver.save_screenshot('/userdata/test2.png') 
        print("login")
        driver.get(server + '/w/index.php?title=Special:UserLogin')
        #sleep(3)
        driver.find_elements(By.ID, 'wpName1')[0].send_keys(user)
        driver.find_elements(By.ID, 'wpPassword1')[0].send_keys(password)
        driver.find_elements(By.ID, 'wpRemember')[0].click() 
        screenshot = driver.save_screenshot('/userdata/test3.png') 
        driver.find_elements(By.ID, 'wpLoginAttempt')[0].click() 
        screenshot = driver.save_screenshot('/userdata/test4.png') 
            
        logged_in = True

    except:
        logged_in = False
        print("Login error") 

    first_run = True
    retry = 0

    while(logged_in and retry < 3):
        pages = [
            #"Category:OSW44deaa5b806d41a2a88594f562b110e9",
            #"Category:OSWd9aa0bca9b0040d8af6f5c091bf9eec7"
        ]

        try:

            if first_run:
            # Main, Talk, File, Category, Item
                nss = ["0", "1", "6", "14", "7000"]
                for ns in nss:
                    print("Query namespace  " + ns)
                    _continue = True
                    continue_param = ""
                    while _continue:
                        driver.get(server + '/w/api.php?action=query&format=json&prop=revisions&generator=allpages&formatversion=2&rvprop=timestamp&gaplimit=10&gapnamespace=' + ns + continue_param)
                        content = driver.find_element(By.TAG_NAME, 'pre').text
                        parsed_json = json.loads(content)
                        if 'query' in parsed_json:
                            for page in parsed_json['query']['pages']:
                                title = page['title']
                                pages.append(title)
                        if 'continue' in parsed_json:
                            print("Continue with page " + parsed_json['continue']['gapcontinue'])
                            continue_param = "&continue=" + parsed_json['continue']['continue'] + "&gapcontinue=" + parsed_json['continue']['gapcontinue']
                        else: _continue = False

            else:
                print("Query recent changes")
                timestamp = (datetime.today() - timedelta(hours=0, minutes=10)).replace(microsecond=0).isoformat()
                driver.get(server + '/w/api.php?action=query&list=recentchanges&rcprop=title|ids|sizes|flags|user&rclimit=100&rcend=' + timestamp)
                content = driver.find_element(By.TAG_NAME, 'pre').text
                parsed_json = json.loads(content)
                if 'query' in parsed_json:
                    for page in parsed_json['query']['recentchanges']:
                        title = page['title']
                        pages.append(title)

            for page in pages:
                page_name = page.replace(":", "_")
                print("Download " + page)
                driver.get(server + '/w/index.php?title=' + page)
                html = driver.find_elements(By.ID, 'mw-content-text')[0].get_attribute('innerHTML')
                with open(path + page_name + '.html',"w") as f: f.write(html)
                #screenshot = driver.save_screenshot(path + page_name + '.png') 

            #search_query = driver.find_element(By.NAME, 'q')
            #search_query.send_keys("Test" + ' wikipedia')
            #search_query.send_keys(Keys.RETURN)
            #screenshot = driver.save_screenshot('/userdata/test.png')
            #wiki_url = driver.find_element(By.CLASS_NAME, 'iUh30').text.replace(' › ','/')
            #driver.get(wiki_url)#

            sleep(60)
            first_run = False

        except:
            retry += 1

    sleep(10)

#finally:
# close chromedriver and display
# driver.quit()
# display.stop()