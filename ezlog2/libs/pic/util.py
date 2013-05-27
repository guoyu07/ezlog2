# -*- coding: utf-8 *-*
import StringIO
import md5

from PIL import Image
from PIL import ImageOps

def generate_url(name):
    if name is None:
        return ""
    from oss.oss_config import *
    return "http://" + END_POINT + "/" + BUCKET + "/" + name

# it is StringIO, not a file. but the API is same. I regard it as file-like object
def convert_image_to_file(image):
    image_buffer = StringIO.StringIO()
    image.save(image_buffer, "JPEG")
    image_buffer.seek(0) #make sure image_buffer.read(0) works
    return image_buffer

def convert_file_to_image(file):
    file.seek(0)
    #change file mode??
    data = file.read()
    buf = buffer(data, 0, len(data))
    image = Image.open(StringIO.StringIO(buf)).convert('RGB')
    return image

def sumfile(fobj):
    '''Returns an md5 hash for an object with read() method.
       & hold file object'''
    fobj.seek(0)
    m = md5.new()
    while True:
        d = fobj.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()

def get_image_file(url):
    import requests
    from StringIO import StringIO
    r = requests.get(url)
    return StringIO(r.content)
