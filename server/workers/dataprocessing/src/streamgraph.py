import pandas as pd
import logging
import sys
import os

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')


logger = logging.getLogger(__name__)
logger.setLevel(os.environ["HEADSTART_LOGLEVEL"])
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
handler.setLevel(os.environ["HEADSTART_LOGLEVEL"])
logger.addHandler(handler)


def get_streamgraph_data(metadata, n=12, method="tfidf"):
    df = pd.DataFrame.from_records(metadata)
    df.year = pd.to_datetime(df.year)
    df.year = df.year.map(lambda x: x.year)
    df.year = df.year.map(lambda x: pd.to_datetime(x, format="%Y"))
    df = df[df.subject.map(lambda x: x is not None)]
    df.subject = df.subject.map(lambda x: [s for s in x.split("; ") if s])
    df = df[df.subject.map(lambda x: x != [])]
    df["boundary_label"] = df.year
    df = df.explode('subject')
    df = df[df.subject != ""]
    counts = get_counts(df)
    boundaries = get_boundaries(df)
    daterange = get_daterange(boundaries)
    data = pd.merge(counts, boundaries, on='year')
    top_n = get_top_n(metadata, data, n, method)
    data = data[data.subject.map(lambda x: x in top_n)].sort_values("year").reset_index(drop=True)
    x = get_x_axis(daterange)
    sg_data = {}
    sg_data["x"] = x
    sg_data["subject"] = postprocess(daterange, data)
    return sg_data


def get_x_axis(daterange):
    return [str(x.year) for x in daterange]


def get_daterange(boundaries):
    daterange = pd.date_range(start=min(boundaries.year).to_datetime64(),
                              end=max(boundaries.year).to_datetime64(),
                              freq='AS')
    if len(daterange) > 0:
        return sorted(daterange)
    else:
        return sorted(pd.unique(boundaries.year))


def get_stream_range(df):
    stream_range = {
        "min": min(df.year),
        "max": max(df.year),
        "range": max(df.year) - min(df.year)
    }
    return stream_range


def get_counts(df):
    counts = (df.groupby(["year", "subject"])
                .agg({'subject': 'count', 'id': lambda x: ", ".join(x)}))
    counts.rename({"subject": "counts"}, axis=1, inplace=True)
    counts.reset_index(inplace=True)
    return counts


def get_boundaries(df):
    boundaries = df[["boundary_label", "year"]].drop_duplicates()
    return boundaries


def get_top_n(metadata, data, n, method):
    df = pd.DataFrame.from_records(metadata)
    df["subject"] = df["subject"].map(lambda x: x.replace("; ;", "; "))
    df = df[df.subject.map(lambda x: len(x) > 2)]
    corpus = df.subject.tolist()
    if method == "count":
        # set stopwords , stop_words='english'
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, tokenizer=lambda x: x.split("; "), lowercase=False)
        tf = tf_vectorizer.fit_transform(corpus)
        counts = pd.DataFrame(tf.toarray(), columns=tf_vectorizer.get_feature_names())
        candidates = counts.sum().sort_values(ascending=False).index.tolist()
        candidates = [c for c in candidates if len(c) > 0]
        top_n = candidates[:n]
    if method == "tfidf":
        tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, tokenizer=lambda x: x.split("; "), lowercase=False)
        tfidf = tfidf_vectorizer.fit_transform(corpus)
        weights = pd.DataFrame(tfidf.toarray(), columns=tfidf_vectorizer.get_feature_names())
        candidates = weights.sum().sort_values(ascending=False).index.tolist()
        candidates = [c for c in candidates if len(c) > 0]
        top_n = candidates[:n]
    if method == "lda":
        tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, tokenizer=lambda x: x.split("; "), lowercase=False)
        tfidf = tfidf_vectorizer.fit_transform(corpus)
        nmf = NMF(n_components=n, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)
        candidates = weights.sum().sort_values(ascending=False).index.tolist()
        candidates = [c for c in candidates if len(c) > 0]
        top_n = candidates[:n]
    if method == "mmf":
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, tokenizer=lambda x: x.split("; "), lowercase=False)
        tf = tf_vectorizer.fit_transform(corpus)
        lda = LatentDirichletAllocation(n_components=n, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
        candidates = weights.sum().sort_values(ascending=False).index.tolist()
        candidates = [c for c in candidates if len(c) > 0]
        top_n = candidates[:n]
    return top_n


def get_top_words(topic, feature_names, n):
    return [feature_names[i] for i in topic.argsort()[:-n - 1:-1]]


def postprocess(daterange, data):
    x = pd.DataFrame(daterange, columns=["year"])
    temp = []
    for item in pd.unique(data.subject):
        tmp = (pd.merge(data[data.subject == item], x,
                        left_on="year", right_on="year",
                        how="right")
                 .fillna({"counts": 0, "subject": item, "id": "NA"})
                 .sort_values("year"))
        y = tmp.counts.astype(int).to_list()
        ids_overall = pd.unique(tmp[tmp.id != "NA"].id.map(lambda x: x.split(", ")).explode()).tolist()
        ids_timestep = tmp.id.map(lambda x: x.split(", ")).tolist()
        temp.append({"name": item, "y": y, "ids_overall": ids_overall, "ids_timestep": ids_timestep})
    df = pd.DataFrame.from_records(temp)
    return df.to_dict(orient="records")
