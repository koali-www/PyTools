from PIL import Image
import pathlib

basedir="xxxxx"
files = pathlib.Path(basedir).glob('**/*.jpg')

width = 1487
height = 2105

for img in files:
    try:
      pic = Image.open(img)
      newpic = pic.resize((width, height), Image.LANCZOS)
      # print (newpic)
      newpic.save(basedir+"\\"+img.name+".pdf")
      # newpic.save()
      print(f"[*]Create success: {img.name}")
    except:
       print(f"[x]Create failed: {img.name}")