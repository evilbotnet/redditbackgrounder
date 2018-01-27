from PIL import Image, ImageDraw, ImageFont
import requests
import random
import textwrap
import urllib.request
import csv
import os

showerThoughts = "https://www.reddit.com/r/Showerthoughts/top/.json?=week&limit=25"
motivationalQuotes = "https://www.reddit.com/r/quotes/top/.json?=month&limit=100"
widescreenwallpaper = "https://www.reddit.com/r/WidescreenWallpaper/top/.json?t=week&limit=100"
wqhd_wallpaper = "https://www.reddit.com/r/WQHD_Wallpaper/top/.json?t=month&limit=100"
wallpapers = "https://www.reddit.com/r/wallpapers/top/.json?t=week&limit=100"
earthporn = "https://www.reddit.com/r/earthporn/top/.json?t=week&limit=100"

urlList = [widescreenwallpaper, wqhd_wallpaper, wallpapers, earthporn]
print(urlList)
try: 
    os.removedirs('pics3')
    os.mkdir('pics3')
    outputfolder = 'pics3/'
except FileNotFoundError:
    os.mkdir('pics3')
    outputfolder = 'pics3/'

def errnos():
    inputfile = 'errno.csv'
    error_nums = []
    error_titles = []
    f = open(inputfile)
    csv_file = csv.reader(f, delimiter=',')
    for row in csv_file:
        error_nums.append(row[0])
        error_titles.append(row[2])
    dictionary = dict(zip(error_nums, error_titles))
    return dictionary

dictionary = errnos()
#message_key = random.choice(list(dictionary))
#message = "Errno %s: %s" % (message_key, dictionary[message_key])

def imageList(url):
    r = requests.get(url, headers={'User-agent': 'Image Downloader'})
    data = r.json()
    return data

def quoteScraper():
    s = requests.get(motivationalQuotes, headers={'User-Agent': 'your bot 0.1'})
    shower = s.json()
    thoughts = []

    for thought in shower['data']['children']:
        title = thought['data']['title']
        thoughts.append(title)
    return thoughts

#quoteScraper()


def drawText(filename, suffix):
    im = Image.open(filename + suffix)
    draw = ImageDraw.Draw(im)

    W, H = im.size
    font_height = H / 15
    font = ImageFont.truetype("ariblk.ttf", int(font_height))
    #message = random.choice(quoteScraper())
    message_key = random.choice(list(dictionary))
    message = "Errno %s: %s" % (message_key, dictionary[message_key])
    msg = textwrap.wrap(message, width=50)
    H = H * 0.6
    pad = 0

    for line in msg:
        w, h = font.getsize(line)
        try:
            draw.text(((W - w) / 2, (H - h + pad) / 2), line, (255, 255, 255), font=font)
            pad += h * 2
        except TypeError as e:
            print(e)
    im.save(filename + '_modified_' + suffix)

def imageDownloader(data):
    for child in data['data']['children']:
        #print(child)
        title = child['data']['title']
        #filesize = re.findall(r"\[([0-9xX× ]+)\]", title)
        image_url = child['data']['url']
        score = int(child['data']['score'])
        try:
            width = child['data']['preview']['images'][0]['source']['width']
            height = child['data']['preview']['images'][0]['source']['height']
            ratio = float(width) / height
            if ratio > float(1.59) and height >= 1080 and width >= 1920:
                #imgur = child['data']['media']['type']
                domain = child['data']['domain']
                suffix = image_url[-4:]
                print(suffix)
                if score > 10 and suffix == '.jpg' or '.png' and 'imgur' not in image_url:
                    print(title)
                    print(image_url)
                    print(score)
                    filename = outputfolder + child['data']['id']
                    try:
                        urllib.request.urlretrieve(image_url, filename=filename + suffix)
                        drawText(filename, suffix)
                    except urllib.error.HTTPError:
                        print("Failed to download " + title + " at " + image_url)


                if "imgur" in image_url and score > 10:
                    suffix = '.jpg'
                    try:
                        imgur = child['data']['media']
                        imgur_url = imgur['oembed']['thumbnail_url']
                        imgur_image = imgur_url[:-3]
                        print("IMGUR " + title)
                        print(imgur_image)
                        print(score)
                        filename = outputfolder + child['data']['id']
                        urllib.request.urlretrieve(imgur_image, filename=filename + suffix)
                        drawText(filename, suffix)
                    except TypeError:
                        pass
                elif score < 10:
                    #print("Score too LOW!")
                    break
            else:
                pass
                #print("Not a widescreen image")
        except KeyError:
            #print("WTF Reddit... Not an image.")
            pass



for i in urlList:
    imageDownloader(imageList(i))