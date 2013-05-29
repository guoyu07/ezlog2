from collections import Counter,defaultdict

import jieba

from ezlog2.libs.db import db
from ezlog2.model.tweet import Tweet

class DocItem(db.EmbeddedDocument):
    doc_id = db.ObjectIdField(required=True)
    score = db.FloatField(required=True)
    meta = {
        'index_types': False,
    }

class SearchIndex(db.Document):
    keyword = db.StringField(primary_key=True, required=True)
    doc_list = db.ListField(db.EmbeddedDocumentField(DocItem))

    meta = {
        'allow_inheritance': False,
        'index_types': False,
    }

    @staticmethod
    def build_index():
        def _keyword_count(string):
            counter         = Counter()
            if not string:
                return counter
            keyword_list    = jieba.cut_for_search(string)
            for key in keyword_list:
                counter[key] +=1
            return counter

        tweets  = Tweet.objects().only("content","id")
        final_d = defaultdict(list)
        for t in tweets:
            counter     = _keyword_count(t.content)
            for key in counter:
                final_d[key].append((t.id,counter[key]))

        SearchIndex.drop_collection()
        for key in final_d:
            si      = SearchIndex(keyword=key)
            si.doc_list.extend([DocItem(doc_id=doc_id, score=score) for doc_id,score in final_d[key]])
            si.save()