"""
This is a simple application for sentence embeddings: semantic search

We have a corpus with various sentences. Then, for a given query sentence,
we want to find the most similar sentence in this corpus.

This script outputs for various queries the top 5 most similar sentences in the corpus.
"""
from functools import partial
from tqdm import tqdm

from typing import List

import os

from sentence_transformers import SentenceTransformer
import scipy.spatial
from util import util_methods, data_io

from pubtator_dump_parsing import doc_generator, pubtator_parser


def calc_similarities(corpus: List[str], embedder, query: str):
    corpus_embeddings = embedder.encode(corpus, batch_size=8)
    query_embeddings = embedder.encode([query])
    distances = scipy.spatial.distance.cdist(
        query_embeddings, corpus_embeddings, "cosine"
    )[0]
    similarities = [1 - dist for dist in distances]
    return [(s, float(sim)) for s, sim in zip(corpus, similarities)]


if __name__ == "__main__":

    import spacy

    # nlp = spacy.load("en_core_web_sm")
    nlp = spacy.blank("en")
    nlp.add_pipe(nlp.create_pipe("sentencizer"))

    file_path = (
        os.environ["HOME"] + "/pubtator/download/bioconcepts2pubtatorcentral.offset.gz"
    )
    g = (pubtator_parser(content) for content in doc_generator(file_path, limit=100_000))
    texts_g = (sent.text for d in g for sent in nlp(d["text"]).sents)

    embedder = SentenceTransformer("bert-base-nli-mean-tokens")
    query = "Clinical characteristics of novel coronavirus disease 2019 (COVID-19) in newborns, infants and children"
    g = util_methods.process_batchwise(
        partial(calc_similarities, embedder=embedder, query=query),
        texts_g,
        batch_size=1024,
    )
    data_io.write_lines(
        "results.csv", ("\t".join([s, str(sim)]) for s, sim in tqdm(g) if sim > 0.9),
    )
