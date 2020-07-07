import requests as req
from bs4 import BeautifulSoup as bs
import datetime
#import html2text as ht
from tomd import Tomd
from app import db
from app.models import User,Post,Category
from dateutil.parser import parse
import time

img_folder = "static/img/"

site = "https://www.yogaone.es/blog/"

head = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
}

u = User.query.get(1)



def get_single_page(inputurl,en):
    page = req.get(inputurl, headers=head).text
    bs_ = bs(page,"lxml")

    img_url = bs_.find(class_="entry-thumbnail")

    if img_url.img:

        img_url = img_url.img['src']

        for i in range(5):
            try:
                img = req.get(img_url,headers=head).content
                break
            except:
                print('Get Image Time Out')
                time.sleep(10)

        img_path = img_folder+img_url.split('/')[-1]
        
        with open('app/'+img_path,"wb") as f:
            f.write(img)
    else:
        img_path = ""
    
    title = bs_.find(class_="entry-title").string

    date = parse(bs_.find(class_="entry-date")['datetime'])

    body = str(bs_.find(class_="entry-content"))

    md = Tomd(body).markdown

    category = bs_.find(class_="entry-categories").a.string
    print(category)
    if not Category.query.filter_by(name=category).first():
        c = Category(name=category)
        db.session.add(c)
        db.session.commit()
        c = Category.query.filter_by(name=category).first()
        print(c)
    else:
        c = Category.query.filter_by(name=category).first()

    u = User.query.get(1)

    print(f'is_en value is: {en}')

    if Post.query.filter_by(title=title).first():
        p = Post.query.filter_by(title=title).first()
        p.title=title
        p.body=md
        p.timestamp=date
        p.cover=img_path
        p.category= c
        p.is_en=en
    else:
        p = Post(title=title,body=md,timestamp=date,author=u,cover=img_path,category=c,is_en=en)
    

    db.session.add(p)

    db.session.commit()

    return bs_

def get_post_urls(inputurl,post_urls):

    page = req.get(inputurl,headers=head).text

    bs_ = bs(page,'lxml')

    if bs_.find(id="post-0"):
        print("PAGE NOT EXISTS!!")
        return False

    articles = bs_.find(id="content").find_all('article')

    for a in articles:

        post_url = a.div.header.div.a['href']

        #print(post_url)        

        post_urls.append(post_url)

    return True


def mainsite():
    site = "https://www.yogaone.es/blog/"
    en = False

    post_urls = []

    page_count = 1

    while True:
        url = "{}page/{}/".format(site,page_count)

        isExist = get_post_urls(url,post_urls)

        if isExist:
            page_count += 1
        else:
            break
    print(post_urls)

    for p in post_urls:
        print("INTO POST "+p)
        print(en)
        get_single_page(p,en)
    
    print("ALL ES SITES FINISHED")




    site = "https://www.yogaone.es/blog/en/"
    en = True

    post_urls = []

    page_count = 1

    while True:
        url = "{}page/{}/".format(site,page_count)

        isExist = get_post_urls(url,post_urls)

        if isExist:
            page_count += 1
        else:
            break
    print(post_urls)

    for p in post_urls:
        print("INTO POST "+p)
        print(en)
        get_single_page(p,en)
    
    print("ALL EN SITES FINISHED")
#mainsite()
mainsite()

    #single_page(site+"introduccion-al-yoga-todo-lo-que-necesitas-saber/")