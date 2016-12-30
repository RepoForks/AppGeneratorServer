#! /usr/bin/env python
import os
import json
import validators
import re
import sys
import urllib2
import urllib
from firebase import firebase
import requests
from tempfile import mkstemp
import subprocess
from tempfile import mkstemp
import zipfile
import shutil
from shutil import move, copyfile
from os import remove, close
from PIL import Image
reload(sys)
sys.setdefaultencoding('utf8')

def replace(file_path, pattern, subst):
    # Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    # Remove original file
    remove(file_path)
    # Move new file
    move(abs_path, file_path)

arg = sys.argv[1]
# Path to be created
path = "/var/www/files/" + str(arg)
print(path)
if not os.path.exists(path):
    os.makedirs(path)

firebase = firebase.FirebaseApplication(
    'https://app-generator.firebaseio.com', None)
result = firebase.get('/users', str(arg))

email = json.dumps(result['Email'])
email = email.replace('"', '')
api = json.dumps(result['Api_Link'])
api = api.replace('"', '')
mode = json.dumps(result['datasource'])
mode = mode.replace('"', '')
print(mode)
print(email)
directory = path + "/" + email
print(directory)
if mode == "jsonupload" :
    result['Api_Link'] = "https://www.test.com" #Set API link to null in case a zip was uploaded

jsonData = json.dumps(result)
with open('/var/www/config.json') as json_data:
    config = json.load(json_data)

conApi = config["api"]
conSender = config["sender"]
conTitle = config["title"]
conBody = config["body"]


if not os.path.exists(directory):
    os.makedirs(directory)
print(conApi)
subprocess.call(['/var/www/scripts/clone.sh', directory])
# subprocess.call(['/var/www/html/setPerm.sh', directory])

#subprocess.call(["/var/www/scripts/deleteAssets.sh", directory])

with open(directory + "/open-event-android/android/app/src/main/assets/config.json", "wb") as fo:
    fo.write(jsonData)

extractPath = directory + "/zip"
if not os.path.exists(extractPath):
    os.makedirs(extractPath)
print("/var/www/html/uploads/" + str(arg) + "/json.zip")
if os.path.exists("/var/www/html/uploads/" + str(arg) + "/json.zip"):
    #zip = zipfile.ZipFile(str("/var/www/html/uploads/" + str(arg) + "/json.zip"))
    # zip.extractall(str(extractPath))
    subprocess.call(['/var/www/scripts/extractZip.sh',
                     "/var/www/html/uploads/" + str(arg) + "/json.zip", extractPath])

eventUrl = str(api) + "/event"

if mode == "eventapi":
    print(mode)
    request = urllib2.Request(eventUrl)
    event = urllib2.urlopen(request).read()
    eventJson = json.loads(event)
else:
    with open(directory + "/zip/event") as json_data:
        event = json.load(json_data)
    eventJson = event

app_name_orig = str(eventJson['name'])
app_name = re.sub('\W+','', app_name_orig )
print app_name
#app_name.encode('ascii', 'ignore')
#filter(app_name.isalnum,app_name)
back_image = str(object=eventJson['background_image'])
logo_path = eventJson['logo']
if back_image.startswith("/"):
   background = directory + "/zip" + back_image
   back = Image.open(background)
   back.load()
   backNew = Image.new("RGB",back.size)
   backNew.paste(back)
   backNew.resize(back.size,Image.ANTIALIAS)
     # Open the image to be converted
   backNew.save(directory+"/zip/background.png",quality=95,optimize=True) # Save it
   copyfile(directory+"/zip/background.png", directory +
            "/open-event-android/android/app/src/main/res/drawable/background.png")
elif back_image != "":
   urllib.urlretrieve(back_image, directory + "/background.png")
   back = Image.open(directory + "/background.png")
   back.load()
   backNew = Image.new("RGB",(back.size))
   backNew.paste(back)
   backNew.resize(back.size,Image.ANTIALIAS)
     # Open the image to be converted
   backNew.save(directory+"/background.png",quality=95,optimize=True) # Save it
   copyfile(directory + "/background.png", directory +
            "/open-event-android/android/app/src/main/res/drawable/background.png")
if logo_path == "":
    print("No logo specified")
    copyfile("/var/www/ic_launcher.png", directory +
             "/open-event-android/android/app/src/main/res/mipmap-hdpi/ic_launcher.png")
    copyfile("/var/www/ic_launcher.png", directory +
             "/open-event-android/android/app/src/main/res/mipmap-mdpi/ic_launcher.png")
    copyfile("/var/www/ic_launcher.png", directory +
             "/open-event-android/android/app/src/main/res/mipmap-xhdpi/ic_launcher.png")
    copyfile("/var/www/ic_launcher.png", directory +
             "/open-event-android/android/app/src/main/res/mipmap-xxhdpi/ic_launcher.png")
    copyfile("/var/www/ic_launcher.png", directory +
             "/open-event-android/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png")
elif logo_path.startswith("/"):
    logo = directory + "/zip" + logo_path
    img = Image.open(logo)
    img.load()
    til = Image.new("RGB",img.size)
    til.paste(img)
    til.resize((192,192),Image.ANTIALIAS)
      # Open the image to be converted
    til.save(directory+"/zip/ic_launcher.png",quality=95,optimize=True) # Save it
    copyfile(directory+"/zip/ic_launcher.png", directory +
             "/open-event-android/android/app/src/main/res/mipmap-hdpi/ic_launcher.png")
    copyfile(directory+"/zip/ic_launcher.png", directory +
             "/open-event-android/android/app/src/main/res/mipmap-mdpi/ic_launcher.png")
    copyfile(directory+"/zip/ic_launcher.png", directory +
             "/open-event-android/android/app/src/main/res/mipmap-xhdpi/ic_launcher.png")
    copyfile(directory+"/zip/ic_launcher.png", directory +
             "/open-event-android/android/app/src/main/res/mipmap-xxhdpi/ic_launcher.png")
    copyfile(directory+"/zip/ic_launcher.png", directory +
             "/open-event-android/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png")
elif validators.url(logo_path):
    print(logo_path)
    urllib.urlretrieve(logo_path, directory + "/ic_launcher.png")
    img = Image.open(directory + "/ic_launcher.png")
    img.save('ic-launcher','png')
    img = Image.open(directory + "/ic_launcher.png")
    img.load()
    til = Image.new("RGB",img.size)
    til.paste(img)
    til.resize((192,192),Image.ANTIALIAS)
    til.save(directory+"/ic_launcher.png",quality=95,optimize=True)
    copyfile(directory + "/ic_launcher.png", directory +
             "/open-event-android/android/app/src/main/res/mipmap-hdpi/ic_launcher.png")
    copyfile(directory + "/ic_launcher.png", directory +
             "/open-event-android/android/app/src/main/res/mipmap-mdpi/ic_launcher.png")
    copyfile(directory + "/ic_launcher.png", directory +
             "/open-event-android/android/app/src/main/res/mipmap-xhdpi/ic_launcher.png")
    copyfile(directory + "/ic_launcher.png", directory +
             "/open-event-android/android/app/src/main/res/mipmap-xxhdpi/ic_launcher.png")
    copyfile(directory + "/ic_launcher.png", directory +
             "/open-event-android/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png")
# if mode == "eventapi":
#     logo_url = api + logo_path
#     print logo_url
#     f = urllib2.urlopen(logo_url)
#     with open("ic_launcher.png", "wb") as code:
#         code.write(f.read())
# else :
#     logo_location = directory + "/zip/" + logo_path
#     copyfile(logo_location,directory+"/open-event-android/android/app/src/main/assets/ic_launcher.png")
#

absDirectory = directory + "/open-event-android/android/"
# subprocess.call(['./setPerm.sh', directory])
replace(directory + "/open-event-android/android/app/src/main/res/values/strings.xml",
        'OpenEvent', app_name)
replace(directory + "/open-event-android/android/app/src/main/res/layout/nav_header.xml",
       'twitter', "background")
replace(directory + "/open-event-android/android/app/build.gradle",
        '"org.fossasia.openevent"', '"org.fossasia.openevent.' + app_name.replace(" ", "") + '"')
for f in os.listdir(directory + "/zip"):
    #       print "no" + f
    if os.path.isfile(os.path.join(directory + "/zip", f)):
        copyfile(directory + "/zip/" + f, directory +
                 "/open-event-android/android/app/src/main/assets/" + f)
        # print f
    # elif f.endswith('.png'):
    #       copyfile(f, directory + "open-event-android/android/app/src/main/res/drawable"+f)
    # replace(directory+"/open-event-android/android/app/src/main/res/values/strings.xml", 'mipmap/ic_launcher', 'drawable/' + f)

subprocess.call(['/var/www/scripts/buildApk.sh', directory])
subprocess.call(['/var/www/scripts/copyApk.sh', absDirectory, arg])
subprocess.call(['/var/www/scripts/passapi.sh', arg, email])
subprocess.call(['python', '/var/www/scripts/sendNotif.py', email, arg])
print("Script End")

