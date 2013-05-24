# -*- coding: utf-8 *-*
from io import BytesIO
import StringIO
import md5

import Image
import ImageOps

from .util import convert_image_to_file, convert_file_to_image, sumfile
'''
# import StringIO
# im = Image.open(StringIO.StringIO(buffer))
a image object can construct from string buffer

http://stackoverflow.com/a/8242265/847357

data = file.read(SIZE)
buf = buffer(data, 0, len(data))

'''
class PicPIL(object):
    '''mainly do something with PIL '''

    def __init__(self, file):
        self.file = file
        self.image = convert_file_to_image(file)


    def recreate_file(self):
        self.file = convert_image_to_file(self.image)

    @property
    def size(self):
        return self.image.size
        
        
    #this method will keep width, height ratio
    def thumbnail(self, size):
        self.image.thumbnail(size, Image.ANTIALIAS)

    #this method will resize the image
    def resize(self, size):
        self.image = self.image.resize(size)

    def crop(self, box):
        '''Returns a rectangular region from the current image. The box is a 4-tuple defining the left, upper, right, and lower pixel coordinate.

        This is a lazy operation. Changes to the source image may or may not be reflected in the cropped image. To get a separate copy, call the load method on the cropped copy.

        this method probably only used by avatar model
        '''
        self.image = self.image.crop(box)









































