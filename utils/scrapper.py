# IMPORT NECCESSARY LIB
import os
import time
from utils.date import now
from utils.formatter import format_description_text
from utils.tweet import tweet

path = os.getcwd()
default_media = path + '/blizzard.png'

def blizzard_forum_scrapper(driver, WebDriverWait, By, EC):
    driver.get('https://us.forums.blizzard.com/en/hearthstone/g/blizzard-tracker/activity/topics')
    wait = WebDriverWait(driver, 60)
    driver.implicitly_wait(10)

    url = None 

    all_bliss_articles = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "a.tracked-post.group-community-manager")))
    top_ten_articles = all_bliss_articles[:10] 

    for new_url in top_ten_articles:
        tweeted = False
        with open(path +"/data/tweeted_articles.txt") as f:
            for line in f:
                if line.strip() == new_url.get_attribute('href'):
                    tweeted = True
                    break
        if tweeted:
            continue  
        else: 
            with open(path +"/data/tweeted_articles.txt", 'a') as f:
                f.write(new_url.get_attribute('href') + '\n')
                url = new_url.get_attribute('href')
            break

    if url == None:
        print('No new articles available at the moment', now())        
    else:
        scrape_articles(driver, WebDriverWait, By, EC, url)
        print('done..............', now())    
        driver.quit()


def scrape_articles(driver, WebDriverWait, By, EC, url):
    driver.get(url)
    time.sleep(10)
    title = driver.find_element(By.CSS_SELECTOR, "a.fancy-title").text

    intro = '📢 Forum article spotted 📢'
    url = driver.current_url
   
    text = f"{intro}\n\n📺 {title}\n\n🌐 {url}"

    # UPLOAD TO TWITTER
    tweet(text, media = default_media)
    
    time.sleep(5)
    driver.quit()
    
    
