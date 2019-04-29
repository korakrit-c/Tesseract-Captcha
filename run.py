from PIL import Image
import urllib, urllib2, cookielib, os, re, time, sys, httplib


url_captcha='https://xdg.com/api/captcha'
url_submit='https://xdg.com/api/ro/gift_code'
url_home='https://www.ragnaroketernallove.com/jana'
captcha='captcha.png'

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

resp = opener.open(url_home)
content = resp.read()

for i in range(1):
    while True:
        #Opening captcha and copy image
        f = opener.open(url_captcha)
        data = f.read()
        f.close()
        with open(captcha, "wb") as d:
            d.write(data)
        if os.path.getsize(captcha) > 0:
            break
        else:
            print 'reset!! empty file'
            break
    
    picture = Image.open(captcha)
    picture = picture.convert('RGB')
    black = (0,0,0)
    white = (255,255,255)
    width, height = picture.size

    for x in range(0,width):
        for y in range(0,height):
            #print picture.getpixel( (x, y) )
            r,g,b= picture.getpixel( (x, y) )
            if r <= 50  and g <= 50 and b <= 50: # blue
                picture.putpixel( (x,y), black)
            else:
                picture.putpixel( (x,y), white)
                #print 'no'
    resize = 5
    picture = picture.resize((int(width*resize), int(height*resize)), Image.ANTIALIAS) # BICUBIC is awesome
    picture.save('result.png')
    os.system('tesseract result.png result -l eng')
    #os.system('tesseract result.png result -l eng --psm 10 --dpi 480')
    f = open ("result.txt","r")
    val = f.read().replace("\n", "").replace("","").replace(" ","")
    val = ''.join(re.findall("[a-zA-Z0-9]+", val))
    print 'submit: ',val
    f = open ("result.txt","w+")
    f.write(val)
    f.close()