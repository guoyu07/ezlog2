# -*- coding: utf-8 *-*
try:
    #this import only used when oss operator used
    from oss.oss_api import OssAPI
    from oss.oss_config import *
except ImportError, e:
    pass

try:
    #this import only used when oss operator used
    from mongoengine import Document,StringField,FileField
except ImportError, e:
    pass
from PIL import Image
from util import sumfile,convert_image_to_file

class PicBaseOperator():
    '''mainly do with save(), delete(),get_url() something either oss or mongoengine'''
    def __init__(self):
        raise NotImplementedError()

    def save(self, pic):
        raise NotImplementedError()

    def delete(self, pic):
        raise NotImplementedError()

    def get_url(self):
        raise NotImplementedError()

class OssOperator(PicBaseOperator):
    def __init__(self):
        self.url        = None
        self.filename   = None
        self.oss        = OssAPI(END_POINT, ACCESS_ID, ACCESS_KEY)

    def save(self, file):
        self.filename = sumfile(file)
        self.url      = self.oss.put_object_from_fp(BUCKET,
                                                    self.filename,
                                                    file)

    def delete(self, filename):
        self.oss.delete_object(BUCKET, filename)

    def get_url(self):
        return self.url

class MongoStorage(Document):
    picture         = FileField()

class MongOperator(PicBaseOperator):
    def __init__(self, mongo_storage = MongoStorage()):
        self.mongo_storage = mongo_storage  #Document Type, need picture attribute
        self.filename      = None
        self.url           = None
        
    @classmethod
    def get_pictue_by_id(cls,id):
        f = MongoStorage.objects(id=id).first()
        if f is None:
            return None
        im = Image.open(f.picture)
        return convert_image_to_file(im)

    def save(self, file):
        self.mongo_storage.picture.put(file, content_type = 'image/jpeg')
        self.mongo_storage.save()
        self.url = "/picture/"+str(self.mongo_storage.id)

    def delete(self, filename):
        self.mongo_storage.picture.delete()

    def get_url(self):
        return self.url



class DiskOperator(PicBaseOperator):
    pass










