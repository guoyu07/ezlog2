# -*- coding: utf-8 *-*

class PicBaseModel(object):

    def save(self, filename):
        raise NotImplementedError()

    @classmethod
    def get_pic_by_id(cls, id):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()


class MongoEngineMixin(PicBaseModel):
    #url         = StringField(required=True)

    @classmethod
    def get_pic_by_id(cls, id):
        return cls.objects(id=id).first()


class NullModel(PicBaseModel):
    '''this is the default model for picture lib,
       this works if client does not require store
       extra pictue information'''

    def save(self,filename):
        pass

    @classmethod
    def get_pic_by_id(cls, id):
        pass

    def delete(self):
        pass
