import json
import pytest
import numpy as np
import pandas as pd
import requests


@pytest.mark.persistence
def test_map_id_creation():
    testcases = [
        # {"params": {"q": "air quality management", "from": "1665-01-01", "to": "2017-09-08", "sorting": "most-relevant", "document_types": [121]},
        #  "param_types": ["from", "to", "document_types", "sorting"],
        #  "expected result": "2074f8b9eee26f53936abd16f6187ed8"},
        # {"params": {"q": "trump", "from": "1665-01-01", "to": "2017-10-27", "sorting": "most-relevant", "document_types": [121]},
        #  "param_types": ["from", "to", "document_types", "sorting"],
        #  "expected result": "d9c930deef17b3f22e3030a9bd020f9f"},
        # {"params": {"q": "solar eclipse", "from": "1665-01-01", "to": "2017-09-08", "sorting": "most-relevant", "document_types": [121]},
        #  "param_types": ["from", "to", "document_types", "sorting"],
        #  "expected result": "f9f0d52aaf3a91d0040c2acdacf00620"},
        # {"params": {"q": "pop music", "from": "1665-01-01", "to": "2017-09-08", "sorting": "most-relevant", "document_types": [121]},
        #  "param_types": ["from", "to", "document_types", "sorting"],
        #  "expected result": "32df883cd04d85a710b6c4057f01dfd8"},
        # {"params": {"q": "fear-of-missing-out", "from": "1665-01-01", "to": "2017-09-08", "sorting": "most-relevant", "document_types": [121]},
        #  "param_types": ["from", "to", "document_types", "sorting"],
        #  "expected result": "81baaafd6f0ddba4a7ce4e7237210fe7"},
        {"params": {"q": "sustainable development goals", 'from': '1809-01-01',
                     'to': '2017-09-08',
                     'sorting': 'most-relevant',
                     'article_types': ['adaptive clinical trial',
                      'address',
                      'autobiography',
                      'bibliography',
                      'biography',
                      'book illustrations',
                      'case reports',
                      'classical article',
                      'clinical conference',
                      'clinical study',
                      'clinical trial',
                      'clinical trial protocol',
                      'clinical trial, phase i',
                      'clinical trial, phase ii',
                      'clinical trial, phase iii',
                      'clinical trial, phase iv',
                      'clinical trial, veterinary',
                      'collected work',
                      'collected works',
                      'comment',
                      'comparative study',
                      'congress',
                      'consensus development conference',
                      'consensus development conference, nih',
                      'controlled clinical trial',
                      'corrected and republished article',
                      'dataset',
                      'dictionary',
                      'directory',
                      'duplicate publication',
                      'editorial',
                      'electronic supplementary materials',
                      'english abstract',
                      'ephemera',
                      'equivalence trial',
                      'evaluation studies',
                      'evaluation study',
                      'expression of concern',
                      'festschrift',
                      'government publication',
                      'guideline',
                      'historical article',
                      'interactive tutorial',
                      'interview',
                      'introductory journal article',
                      'journal article',
                      'lecture',
                      'legal case',
                      'legislation',
                      'letter',
                      'manuscript',
                      'meta analysis',
                      'multicenter study',
                      'news',
                      'newspaper article',
                      'observational study',
                      'observational study, veterinary',
                      'overall',
                      'patient education handout',
                      'periodical index',
                      'personal narrative',
                      'pictorial work',
                      'popular work',
                      'portrait',
                      'practice guideline',
                      'pragmatic clinical trial',
                      'preprint',
                      'publication components',
                      'publication formats',
                      'publication type category',
                      'published erratum',
                      'randomized controlled trial',
                      'randomized controlled trial, veterinary',
                      'research support, american recovery and reinvestment act',
                      'research support, n i h, extramural',
                      'research support, n i h, intramural',
                      "research support, non u s gov't",
                      "research support, u s gov't, non p h s",
                      "research support, u s gov't, p h s",
                      'research support, u s government',
                      'retraction of publication',
                      'review',
                      'scientific integrity review',
                      'study characteristics',
                      'support of research',
                      'systematic review',
                      'technical report',
                      'twin study',
                      'validation study',
                      'video audio media',
                      'webcasts']},
         "param_types": ["from", "to", "sorting", "article_types"],
         "expected result": "60d2dd3caeade4c0eed6ed486d737fd3"},
         {"params": {"q": "athens",
                    'from': '1809-01-01',
                     'to': '2017-09-08',
                     'sorting': 'most-relevant',
                     'article_types': ['adaptive clinical trial',
                      'address',
                      'autobiography',
                      'bibliography',
                      'biography',
                      'book illustrations',
                      'case reports',
                      'classical article',
                      'clinical conference',
                      'clinical study',
                      'clinical trial',
                      'clinical trial protocol',
                      'clinical trial, phase i',
                      'clinical trial, phase ii',
                      'clinical trial, phase iii',
                      'clinical trial, phase iv',
                      'clinical trial, veterinary',
                      'collected work',
                      'collected works',
                      'comment',
                      'comparative study',
                      'congress',
                      'consensus development conference',
                      'consensus development conference, nih',
                      'controlled clinical trial',
                      'corrected and republished article',
                      'dataset',
                      'dictionary',
                      'directory',
                      'duplicate publication',
                      'editorial',
                      'electronic supplementary materials',
                      'english abstract',
                      'ephemera',
                      'equivalence trial',
                      'evaluation studies',
                      'evaluation study',
                      'expression of concern',
                      'festschrift',
                      'government publication',
                      'guideline',
                      'historical article',
                      'interactive tutorial',
                      'interview',
                      'introductory journal article',
                      'journal article',
                      'lecture',
                      'legal case',
                      'legislation',
                      'letter',
                      'manuscript',
                      'meta analysis',
                      'multicenter study',
                      'news',
                      'newspaper article',
                      'observational study',
                      'observational study, veterinary',
                      'overall',
                      'patient education handout',
                      'periodical index',
                      'personal narrative',
                      'pictorial work',
                      'popular work',
                      'portrait',
                      'practice guideline',
                      'pragmatic clinical trial',
                      'preprint',
                      'publication components',
                      'publication formats',
                      'publication type category',
                      'published erratum',
                      'randomized controlled trial',
                      'randomized controlled trial, veterinary',
                      'research support, american recovery and reinvestment act',
                      'research support, n i h, extramural',
                      'research support, n i h, intramural',
                      "research support, non u s gov't",
                      "research support, u s gov't, non p h s",
                      "research support, u s gov't, p h s",
                      'research support, u s government',
                      'retraction of publication',
                      'review',
                      'scientific integrity review',
                      'study characteristics',
                      'support of research',
                      'systematic review',
                      'technical report',
                      'twin study',
                      'validation study',
                      'video audio media',
                      'webcasts']},
          "param_types": ["from", "to", "sorting", "article_types"],
          "expected result": "fc3240ce14abf183f7a089ad8757f6a1"},
          {"params": {"q": "hannover",
                     'from': '1809-01-01',
                     'to': '2018-02-16',
                     'sorting': 'most-relevant',
                     'article_types': ['adaptive clinical trial',
                      'address',
                      'autobiography',
                      'bibliography',
                      'biography',
                      'book illustrations',
                      'case reports',
                      'classical article',
                      'clinical conference',
                      'clinical study',
                      'clinical trial',
                      'clinical trial protocol',
                      'clinical trial, phase i',
                      'clinical trial, phase ii',
                      'clinical trial, phase iii',
                      'clinical trial, phase iv',
                      'clinical trial, veterinary',
                      'collected work',
                      'collected works',
                      'comment',
                      'comparative study',
                      'congress',
                      'consensus development conference',
                      'consensus development conference, nih',
                      'controlled clinical trial',
                      'corrected and republished article',
                      'dataset',
                      'dictionary',
                      'directory',
                      'duplicate publication',
                      'editorial',
                      'electronic supplementary materials',
                      'english abstract',
                      'ephemera',
                      'equivalence trial',
                      'evaluation studies',
                      'evaluation study',
                      'expression of concern',
                      'festschrift',
                      'government publication',
                      'guideline',
                      'historical article',
                      'interactive tutorial',
                      'interview',
                      'introductory journal article',
                      'journal article',
                      'lecture',
                      'legal case',
                      'legislation',
                      'letter',
                      'manuscript',
                      'meta analysis',
                      'multicenter study',
                      'news',
                      'newspaper article',
                      'observational study',
                      'observational study, veterinary',
                      'overall',
                      'patient education handout',
                      'periodical index',
                      'personal narrative',
                      'pictorial work',
                      'popular work',
                      'portrait',
                      'practice guideline',
                      'pragmatic clinical trial',
                      'preprint',
                      'publication components',
                      'publication formats',
                      'publication type category',
                      'published erratum',
                      'randomized controlled trial',
                      'randomized controlled trial, veterinary',
                      'research support, american recovery and reinvestment act',
                      'research support, n i h, extramural',
                      'research support, n i h, intramural',
                      "research support, non u s gov't",
                      "research support, u s gov't, non p h s",
                      "research support, u s gov't, p h s",
                      'research support, u s government',
                      'retraction of publication',
                      'review',
                      'scientific integrity review',
                      'study characteristics',
                      'support of research',
                      'systematic review',
                      'technical report',
                      'twin study',
                      'validation study',
                      'video audio media',
                      'webcasts']},
           "param_types": ["from", "to", "sorting", "article_types"],
           "expected result": "3b39a6afad01a572d02122d15d3bf9bb"},
           {"params": {"q": "hangover",
                    'from': '1809-01-01',
                     'to': '2018-02-16',
                     'sorting': 'most-relevant',
                     'article_types': ['adaptive clinical trial',
                      'address',
                      'autobiography',
                      'bibliography',
                      'biography',
                      'book illustrations',
                      'case reports',
                      'classical article',
                      'clinical conference',
                      'clinical study',
                      'clinical trial',
                      'clinical trial protocol',
                      'clinical trial, phase i',
                      'clinical trial, phase ii',
                      'clinical trial, phase iii',
                      'clinical trial, phase iv',
                      'clinical trial, veterinary',
                      'collected work',
                      'collected works',
                      'comment',
                      'comparative study',
                      'congress',
                      'consensus development conference',
                      'consensus development conference, nih',
                      'controlled clinical trial',
                      'corrected and republished article',
                      'dataset',
                      'dictionary',
                      'directory',
                      'duplicate publication',
                      'editorial',
                      'electronic supplementary materials',
                      'english abstract',
                      'ephemera',
                      'equivalence trial',
                      'evaluation studies',
                      'evaluation study',
                      'expression of concern',
                      'festschrift',
                      'government publication',
                      'guideline',
                      'historical article',
                      'interactive tutorial',
                      'interview',
                      'introductory journal article',
                      'journal article',
                      'lecture',
                      'legal case',
                      'legislation',
                      'letter',
                      'manuscript',
                      'meta analysis',
                      'multicenter study',
                      'news',
                      'newspaper article',
                      'observational study',
                      'observational study, veterinary',
                      'overall',
                      'patient education handout',
                      'periodical index',
                      'personal narrative',
                      'pictorial work',
                      'popular work',
                      'portrait',
                      'practice guideline',
                      'pragmatic clinical trial',
                      'preprint',
                      'publication components',
                      'publication formats',
                      'publication type category',
                      'published erratum',
                      'randomized controlled trial',
                      'randomized controlled trial, veterinary',
                      'research support, american recovery and reinvestment act',
                      'research support, n i h, extramural',
                      'research support, n i h, intramural',
                      "research support, non u s gov't",
                      "research support, u s gov't, non p h s",
                      "research support, u s gov't, p h s",
                      'research support, u s government',
                      'retraction of publication',
                      'review',
                      'scientific integrity review',
                      'study characteristics',
                      'support of research',
                      'systematic review',
                      'technical report',
                      'twin study',
                      'validation study',
                      'video audio media',
                      'webcasts']},
            "param_types": ["from", "to", "sorting", "article_types"],
            "expected result": "3d7c033bf1dac0ca0895f9004d18db01"},
    ]
    for tc in testcases:
        res = requests.post("http://localhost/api/persistence/createID", json=tc)
        result = res.json()
        assert result["unique_id"] == tc["expected result"]


@pytest.mark.persistence
def test_add_map_to_database():
    pass


@pytest.mark.persistence
def test_add_revision_to_database():
    pass
