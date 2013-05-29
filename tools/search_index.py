# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ezlog2.model.search import SearchIndex

if __name__ == "__main__":
    SearchIndex.build_index()










