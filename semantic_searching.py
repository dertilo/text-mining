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
from util import util_methods

from pubtator_dump_parsing import doc_generator, pubtator_parser


def calc_similarities(corpus: List[str], embedder, query: str):
    corpus_embeddings = embedder.encode(corpus)
    query_embeddings = embedder.encode([query])
    distances = scipy.spatial.distance.cdist(
        query_embeddings, corpus_embeddings, "cosine"
    )[0]
    similarities = [1 - dist for dist in distances]
    return [(s, sim) for s, sim in zip(corpus, similarities)]


if __name__ == "__main__":

    import spacy

    nlp = spacy.load("en_core_web_sm")
    file_path = (
        os.environ["HOME"]
        + "/code/NLP/IE/pubtator/download/bioconcepts2pubtatorcentral.offset.sample"
    )
    g = (pubtator_parser(content) for content in doc_generator(file_path))
    texts_g = (sent.text for d in g for sent in nlp(d["text"]).sents)

    embedder = SentenceTransformer("bert-base-nli-mean-tokens")
    query = "A substantial fraction of both mutants reached the surface even at low expression levels."
    g = util_methods.process_batchwise(
        partial(calc_similarities, embedder=embedder, query=query),
        texts_g,
        batch_size=32,
    )
    print(list(sorted(((s,sim) for s,sim in tqdm(g) if sim>0.5), key=lambda x: -x[1])))
