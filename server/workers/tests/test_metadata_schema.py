import os
import json
import pandas as pd
import numpy as np
from pandas_schema import Column, Schema
from pandas_schema.validation import (InListValidation,
                                      DateFormatValidation,
                                      IsDtypeValidation,
                                      CustomElementValidation)


core_schema = Schema([
    Column('id', [CustomElementValidation(
                    lambda x: isinstance(x, str), "Not a string.")]),
    Column('authors', [CustomElementValidation(
                    lambda x: isinstance(x, str), "Not a string.")]),
    Column('title', [CustomElementValidation(
                    lambda x: isinstance(x, str), "Not a string.")]),
    Column('paper_abstract', [CustomElementValidation(
                    lambda x: isinstance(x, str), "Not a string.")]),
    Column('year', [CustomElementValidation(
                    lambda x: isinstance(x, str), "Not a string.")]),
    Column('subject_orig', [CustomElementValidation(
                    lambda x: isinstance(x, str), "Not a string.")]),
])


base_schema = Schema([
    Column('link', [CustomElementValidation(
                    lambda x: isinstance(x, str), "Not a string.")]),
    Column('oa_state', [CustomElementValidation(
                    lambda x: isinstance(x, str), "Not a string.")]),
    Column('published_in', [CustomElementValidation(
                    lambda x: isinstance(x, str), "Not a string.")]),
    Column('subject', [CustomElementValidation(
                    lambda x: isinstance(x, str), "Not a string.")]),
    Column('url', [CustomElementValidation(
                    lambda x: isinstance(x, str), "Not a string.")]),
    Column('relation', [CustomElementValidation(
                    lambda x: isinstance(x, str), "Not a string.")]),
    Column('relevance', [CustomElementValidation(
                    lambda x: isinstance(x, int), "Not an integer.")])
])


pubmed_schema = Schema([
    Column('subject', [CustomElementValidation(
                    lambda x: isinstance(x, str), "Not a string.")]),
    Column('url', [CustomElementValidation(
                    lambda x: isinstance(x, str), "Not a string.")]),
    Column('doi', [CustomElementValidation(
                    lambda x: isinstance(x, str), "Not a string.")]),
    Column('pmid', [CustomElementValidation(
                    lambda x: isinstance(x, str), "Not a string.")]),
])


def test_metadata_schema():
    for casefile in os.listdir("tests/testdata"):
        with open(os.path.join("tests/testdata", casefile)) as infile:
            casedata = json.load(infile)
        service = casedata["params"]["service"]
        metadata = pd.DataFrame.from_records(json.loads(casedata["input_data"]["metadata"]))
        core_errors = core_schema.validate(metadata, columns=core_schema.get_column_names())
        if service == "base":
            service_errors = base_schema.validate(metadata, columns = base_schema.get_column_names())
        if service == "pubmed":
            service_errors = pubmed_schema.validate(metadata, columns = pubmed_schema.get_column_names())
        assert len(core_errors) == 0
        assert len(service_errors) == 0
