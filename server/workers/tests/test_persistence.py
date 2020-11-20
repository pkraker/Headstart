import json
import pytest
import numpy as np
import pandas as pd
import requests

from .test_helpers import KNOWNCASES, CASENAMES, CASEDATA, RESULTS, get_dataprocessing_result


@pytest.mark.persistence
def test_vis_id_creation_base():
    testcases = [
        {"params": {"q": "air quality management", "from": "1665-01-01", "to": "2017-09-08", "sorting": "most-relevant", "document_types": [121], "min_descsize": 300},
         "param_types": ["from", "to", "document_types", "sorting", "min_descsize"],
         "expected_result": "9810f6b4aefa7d0b8151e030c07c9514"},
        {"params": {"q": "solar eclipse", "from": "1665-01-01", "to": "2017-09-08", "sorting": "most-relevant", "document_types": [121], "min_descsize": 300},
         "param_types": ["from", "to", "document_types", "sorting", "min_descsize"],
         "expected_result": "d76de62667fe956bd65862ebbf3c5448"},
        {"params": {"q": "lisbon treaty", "from": "1665-01-01", "to": "2018-10-04", "sorting": "most-relevant", "document_types": [121], "min_descsize": 300},
         "param_types": ["from", "to", "document_types", "sorting", "min_descsize"],
         "expected_result": "a2005cba90de92b6b8f13cdcb890dbfa"},
        {"params": {"q": "fear-of-missing-out", "from": "1665-01-01", "to": "2017-09-08", "sorting": "most-relevant", "document_types": [121], "min_descsize": 300},
         "param_types": ["from", "to", "document_types", "sorting", "min_descsize"],
         "expected_result": "f82bf0235217431d56a5afac8ef2c1d4"},
        {"params": {"q": "air quality management", "from": "1665-01-01", "to": "2017-09-08", "sorting": "most-relevant", "document_types": ["121"], "min_descsize": "300"},
         "param_types": ["from", "to", "document_types", "sorting", "min_descsize"],
         "expected_result": "9810f6b4aefa7d0b8151e030c07c9514"},
        {"params": {"q": "solar eclipse", "from": "1665-01-01", "to": "2017-09-08", "sorting": "most-relevant", "document_types": ["121"], "min_descsize": "300"},
         "param_types": ["from", "to", "document_types", "sorting", "min_descsize"],
         "expected_result": "d76de62667fe956bd65862ebbf3c5448"},
        {"params": {"q": "lisbon treaty", "from": "1665-01-01", "to": "2018-10-04", "sorting": "most-relevant", "document_types": ["121"], "min_descsize": "300"},
         "param_types": ["from", "to", "document_types", "sorting", "min_descsize"],
         "expected_result": "a2005cba90de92b6b8f13cdcb890dbfa"},
        {"params": {"q": "fear-of-missing-out", "from": "1665-01-01", "to": "2017-09-08", "sorting": "most-relevant", "document_types": ["121"], "min_descsize": "300"},
         "param_types": ["from", "to", "document_types", "sorting", "min_descsize"],
         "expected_result": "f82bf0235217431d56a5afac8ef2c1d4"},
        {"params": {"q": '"machine learning"', "from":"1665-01-01","to":"2020-11-10","document_types":[121],"sorting":"most-relevant","min_descsize":300},
         "param_types": ["from", "to", "document_types", "sorting", "min_descsize"],
         "expected_result": "d605fe2d66d651830f19ab0e980ad321"},
        {"params": {"q": '"machine learning"', "from":"1665-01-01","to":"2020-11-10","document_types":["121"],"sorting":"most-relevant","min_descsize":"300"},
         "param_types": ["from", "to", "document_types", "sorting", "min_descsize"],
         "expected_result": "d605fe2d66d651830f19ab0e980ad321"},
    ]
    for tc in testcases:
        res = requests.post("http://localhost/api/persistence/createID", json=tc)
        result = res.json()
        assert result["unique_id"] == tc["expected_result"]


@pytest.mark.persistence
def test_vis_id_creation_pubmed():
    testcases = [
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
            "expected_result": "60d2dd3caeade4c0eed6ed486d737fd3"},
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
         "expected_result": "fc3240ce14abf183f7a089ad8757f6a1"},
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
          "expected_result": "3b39a6afad01a572d02122d15d3bf9bb"},
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
           "expected_result": "3d7c033bf1dac0ca0895f9004d18db01"},
        {"params": {"q": '"machine learning"', "from":"1809-01-01","to":"2020-11-10","sorting":"most-relevant",
                    "article_types":["adaptive clinical trial","address","autobiography","bibliography",
                    "biography","book illustrations","case reports","classical article","clinical conference",
                    "clinical study","clinical trial","clinical trial protocol","clinical trial, phase i",
                    "clinical trial, phase ii","clinical trial, phase iii","clinical trial, phase iv","clinical trial, veterinary",
                    "collected work","collected works","comment","comparative study","congress","consensus development conference",
                    "consensus development conference, nih","controlled clinical trial","corrected and republished article","dataset",
                    "dictionary","directory","duplicate publication","editorial","electronic supplementary materials",
                    "english abstract","ephemera","equivalence trial","evaluation studies","evaluation study","expression of concern",
                    "festschrift","government publication","guideline","historical article","interactive tutorial","interview",
                    "introductory journal article","journal article","lecture","legal case","legislation","letter","manuscript",
                    "meta analysis","multicenter study","news","newspaper article","observational study","observational study, veterinary",
                    "overall","patient education handout","periodical index","personal narrative","pictorial work","popular work","portrait",
                    "practice guideline","pragmatic clinical trial","preprint","publication components","publication formats",
                    "publication type category","published erratum","randomized controlled trial","randomized controlled trial, veterinary",
                    "research support, american recovery and reinvestment act","research support, n i h, extramural","research support, n i h, intramural",
                    "research support, non u s gov't","research support, u s gov't, non p h s","research support, u s gov't, p h s",
                    "research support, u s government","retraction of publication","review","scientific integrity review","study characteristics",
                    "support of research","systematic review","technical report","twin study","validation study","video audio media","webcasts"]},
           "param_types": ["from", "to", "sorting", "article_types"],
           "expected_result": "6a0503da37397cd535807f420f2ad7e2"}
    ]
    for tc in testcases:
        res = requests.post("http://localhost/api/persistence/createID", json=tc)
        result = res.json()
        assert result["unique_id"] == tc["expected_result"]


@pytest.mark.persistence
def test_vis_id_creation_triple():
    testcases = [
        {"params": {"q": '"social responsibility"', "from":"1809","to":"2020","sorting":"most-recent","vis_type":"timeline","language":"en","limit":"1000","sg_method":"count"},
         "param_types": ["from", "to", "sorting", "vis_type", "language", "limit", "sg_method"],
         "expected_result": "d6339f547d3973d1b6bff934931cce6e"},
        {"params": {"q": '"Black Power movement"', "from":"1809","to":"2020","sorting":"most-relevant","vis_type":"overview","language":"en","limit":"100","sg_method":"tfidf"},
         "param_types": ["from", "to", "sorting", "vis_type", "language", "limit", "sg_method"],
         "expected_result": "54aeae843934ea1c0a6d2eca817a45b5"},
        {"params": {"q": 'spain', "from":"1809","to":"2020","sorting":"most-relevant","vis_type":"timeline","language":"all","limit":"100"},
         "param_types": ["from", "to", "sorting", "vis_type", "language", "limit"],
         "expected_result": "dce1831710b80c54160fd3477b7ec2dc"},
        {"params": {"q": 'antique egypt', "from":"1809","to":"2020","sorting":"most-relevant","vis_type":"overview"},
         "param_types": ["from", "to", "sorting", "vis_type"],
         "expected_result": "1ed301e7afc3f820b7ef83abf0a004de"}
    ]
    for tc in testcases:
        res = requests.post("http://localhost/api/persistence/createID", json=tc)
        result = res.json()
        assert result["unique_id"] == tc["expected_result"]


@pytest.mark.persistence
def test_get_last_version():
    # vis_id, details, context
    pass


@pytest.mark.persistence
@pytest.mark.parametrize("testcase", KNOWNCASES)
def test_create_visualization(testcase):
    caseid = testcase["caseid"]
    payload = {}
    payload["vis_id"] = caseid
    payload["vis_title"] = caseid
    payload["data"] = RESULTS[caseid].to_json(orient='records')
    payload["vis_clean_query"] = caseid
    payload["vis_query"] = caseid
    payload["vis_params"] = json.dumps(testcase["casedata"]["params"])
    res = requests.post("http://localhost/api/persistence/createVisualization",
                        json=payload)
    assert res.status_code == 200, res.json().get('reason')


@pytest.mark.persistence
@pytest.mark.parametrize("testcase", KNOWNCASES)
def test_write_revision(testcase):
    caseid = testcase["caseid"]
    payload = {}
    payload["vis_id"] = caseid
    payload["data"] = RESULTS[caseid].to_json(orient='records')
    res = requests.post("http://localhost/api/persistence/writeRevision",
                        json=payload)
    assert res.status_code == 200, res.json().get('reason')


@pytest.mark.persistence
@pytest.mark.parametrize("testcase", KNOWNCASES)
def test_map_exists(testcase):
    caseid = testcase["caseid"]
    payload = {}
    payload["vis_id"] = caseid
    res = requests.post("http://localhost/api/persistence/existsVisualization",
                        json=payload)
    result = res.json()
    assert result["exists"] is True


@pytest.mark.persistence
@pytest.mark.parametrize("testcase", KNOWNCASES)
def test_map_exists_not(testcase):
    caseid = testcase["caseid"]
    invalid_id = caseid[2:]
    payload = {}
    payload["vis_id"] = invalid_id
    res = requests.post("http://localhost/api/persistence/existsVisualization",
                        json=payload)
    result = res.json()
    assert result["exists"] is False
