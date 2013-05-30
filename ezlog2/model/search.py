# -*- coding: utf-8 *-*
from collections import Counter,defaultdict
import itertools

import jieba

from ezlog2.libs.db import db
from ezlog2.model.tweet import Tweet

class DocItem(db.EmbeddedDocument):
    doc     = db.ReferenceField(Tweet, required=True)
    score   = db.FloatField(required=True)

    meta    = {
        'index_types': False,
    }
    
    def __hash__(self):
        if self.doc is None:
            # For new object
            return super(BaseDocument, self).__hash__()
        else:
            return hash(self.doc)

class SearchIndex(db.Document):
    keyword = db.StringField(primary_key=True, required=True)
    doc_list = db.ListField(db.EmbeddedDocumentField(DocItem))

    meta = {
        'allow_inheritance': False,
        'index_types': False,
        'indexes': [
            {'fields': ['keyword'], 'unique': True},
        ]
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

        tweets  = Tweet.objects(retweetid="").only("content","id")
        final_d = defaultdict(list)
        for t in tweets:
            counter     = _keyword_count(t.content)
            for key in counter:
                final_d[key].append((t,counter[key]))

        SearchIndex.drop_collection()
        for key in final_d:
            si      = SearchIndex(keyword=key)
            si.doc_list.extend([DocItem(doc=doc, score=score) for doc,score in final_d[key]])
            si.save()

    @classmethod
    def get_tweets_by_keywords(cls,keywords,limit=10,offset=0):
        start     = offset*limit
        end       = offset*limit + limit
        doc_lists = (x.doc_list for x in SearchIndex.objects(keyword__in=keywords).only("doc_list"))
        # print d
        docs      = itertools.chain.from_iterable(doc_lists)
        counter   = Counter()
        for d in docs:
            counter[d] +=d.score

        sorted_d = sorted(counter.iteritems(),key=lambda x:-x[1])[start:end]

        return [x[0].doc for x in sorted_d]







