def scrape():
    # In[7]:


    from splinter import Browser
    from bs4 import BeautifulSoup


    # In[8]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # # NASA Mars News

    # In[9]:


    url1 = 'https://mars.nasa.gov/news/'
    browser.visit(url1)
    html1 = browser.html
    soup1 = BeautifulSoup(html1, 'html.parser')


    # In[10]:


    news_title = soup1.find('div', class_="content_title").text
    news_p = soup1.find('div', class_="article_teaser_body").text


    # # JPL Mars Space Images - Featured Image

    # In[11]:


    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    html2 = browser.html
    soup2 = BeautifulSoup(html2, "html.parser")


    # In[12]:


    featured_image_url = 'https://www.jpl.nasa.gov' + soup2.find('a', class_="fancybox").get("data-fancybox-href")


    # # Mars Weather

    # In[13]:


    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    html3 = browser.html
    soup3 = BeautifulSoup(html3, "html.parser")


    # In[18]:


    mars_weather = soup3.find('p', class_='tweet-text').text


    # # Mars Facts

    # In[48]:


    import pandas as pd
    url4 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url4)
    mars_facts = tables[0].values


    # # Mars Hemispheres

    # In[31]:


    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    html5 = browser.html
    soup5 = BeautifulSoup(html5, "html.parser")


    # In[ ]:


    hemis_list = []
    hem_titles = soup5.find_all('h3')

    for i in range(4):
        hem_title = hem_titles[i].text

        browser.click_link_by_partial_text(hem_title)
        img_html = browser.html
        img_soup = BeautifulSoup(img_html, "html.parser")
        img_url = "https://astrogeology.usgs.gov" + img_soup.find("img", class_="wide-image").get("src")

        hemis_list.append({"title":hem_title,"img_url":img_url})

        browser.click_link_by_partial_text("Back")

    return {
    "news_title":news_title,
    "news_p":news_p,
    "featured_image_url":featured_image_url,
    "mars_facts":mars_facts,
    "hemis_list":hemis_list
    }
