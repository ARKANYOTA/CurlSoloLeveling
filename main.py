import re
from io import BytesIO

import urllib.request
from PIL import Image 

import subprocess
import requests


def main1():
    file = "list_ep.md"
    links = []
    with open(file, "r") as f:
        for line in f.readlines():
            linesplit = (line.split("\t"))
            if len(linesplit) >= 2:
                link,name = tuple(linesplit)
                links.append((link,name))
    return links

def main2(link, numero_image, name_image):
    # out = subprocess.Popen(['curl', link], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # stdout,stderr = out.communicate()
    # stdout = stdout.decode("utf-8")
    stdout = requests.post(link).text
    urls = []
    for line in stdout.split("\n"):
        if re.search("decoding=\"async\" src", line):
            print("\033[34m",line,"\033[0m")
            urls.append(re.search("src=\"([^\"]*)\"",line).group(1))
            print("\t",re.search("src=\"([^\"]*)\"",line).group(1))

    if len(urls) == 0:
        for line in stdout.split("\n"):
            if (re.search("Page", line) or re.search("Scan", line)) and re.search("img", line):
                urls.append(re.search("src=\"([^\"]*)\"",line).group(1).replace("&amp;", "&"))
                print("\t",re.search("src=\"([^\"]*)\"",line).group(1))

    if len(urls) == 0:
        for line in stdout.split("\n"):
            if re.search("_2_tDEnGMLxpM6uOa2kaDB3", line) and re.search("img", line):
                urls.append(re.search("src=\"([^\"]*)\"",line).group(1).replace("&amp;", "&"))
                print("\t",re.search("src=\"([^\"]*)\"",line).group(1))


    # Ep 186
    if len(urls) == 0:
        for line in stdout.split("\n"):
            if re.search("toonix.xyz", line) and re.search("img", line):
                urls.append(re.search("src=\"([^\"]*)\"",line).group(1).replace("&amp;", "&"))
                print("\t",re.search("src=\"([^\"]*)\"",line).group(1))

    if len(urls) == 0:
        for line in stdout.split("\n"):
            if re.search("class=\"wp-manga-chapter-img\"", line) and re.search("img", line):
                urls.append(re.search("src=\"([^\"]*)\"",line).group(1).replace("&amp;", "&"))
                print("\t",re.search("src=\"([^\"]*)\"",line).group(1))

    if len(urls) == 0:
        for line in stdout.split("\n"):
            if re.search("decoding=\"async\" class=\"aligncenter\" src=", line) and re.search("img", line):
                urls.append(re.search("src=\"([^\"]*)\"",line).group(1).replace("&amp;", "&"))
                print("\t",re.search("src=\"([^\"]*)\"",line).group(1))

    if len(urls) == 0:
        for line in stdout.split("\n"):
            print(line)
        print("\033[34m--------------------------\033[0m")
        for line in stdout.split("\n"):
            if re.search("img", line):
                print(line)
        exit(0)
    print(urls)
    getimage(urls).save(f"output/{numero_image}_{name_image.strip().replace(' ', '_')}.png")



def getimage(urls):
    images = []
    for url in urls:
        # url = 'https://1.bp.blogspot.com/-tIYYMDh-1To/YQ_LZK49mBI/AAAAAAAAAOE/ektpxzYzjGY3ITQLyoe4ZDrGqTT1e8p2gCLcBGAsYHQ/s0/002.jpg'
        # image = Image.open(urllib.request.urlopen(url)) 
        try:
            image = Image.open(urllib.request.urlopen(url)) 
            images.append(image)
        except:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            images.append(image)

    h = 0
    w = 0
    for img in images:
        h+= img.height
        w = max(w, img.width)

    print("len(image),h,w: ",len(images),h,w)

    dst = Image.new('RGB', (w,h))
    pos_h = 0
    for img in images:
        dst.paste(img, (0, pos_h))
        pos_h += img.height
    return dst



if __name__ == "__main__":
    s = 189
    links = main1()[::-1][s:]
    print(links)
    for i,linked in enumerate(links):
        i+=s
        link, name = linked
        main2(link, i, name)
        print(f"\033[33m{name} Done\033[0m")

            
