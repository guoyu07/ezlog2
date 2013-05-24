# -*- coding: utf-8 *-*
from _pic_pil import PicPIL
from _pic_operator import OssOperator
from _pic_model import NullModel
from util import generate_url

class Picture(object):

    def __init__(self, file, operator=OssOperator, model=NullModel):
        self.url        = None
        self.picpil     = PicPIL(file)
        self.operator   = operator()
        self.model      = model()


    def save(self):
        self.picpil.thumbnail((400,10**4))
        self.picpil.recreate_file()
        self.operator.save(self.picpil.file)
        self.model.save(self.operator.filename)
        self.url = generate_url(self.operator.filename)

    def delete(self):
        pass

    def get_url(self):
        return self.url

    @property
    def size(self):
        return self.picpil.size
