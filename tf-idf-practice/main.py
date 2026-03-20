import multiprocessing
import pathlib
import json
import math
from time import perf_counter, sleep
from nltk.tokenize import wordpunct_tokenize
from nltk.stem.snowball import SnowballStemmer


from os import listdir
from os.path import isfile, join

from multiprocessing import Pool

from typing import NamedTuple, cast
import psutil
import os


class Index(NamedTuple):
    tf_meta: dict[str, dict[str, int]]
    idf_meta: dict[str, int]

    def __str__(self) -> str:
        return f"Index(tf_meta=...{len(self.tf_meta)} items, idf_meta=...{len(self.idf_meta)} items )"


def resolve_path(path: pathlib.Path):
    return str(path.resolve())


def read_file_with_path(path: str):
    return (path, read_file(path))


def read_file(path: str):

    try:
        with open(path, "r") as f:
            return f.read()

    except Exception:
        return None


def get_term_occurrences(path: pathlib.Path):
    #

    _path = str(path)
    try:
        with open(_path, "r") as f:
            file_read = (_path, f.read())

    except Exception as e:
        raise e

    # get term occurrences

    f = file_read

    name = f[0]
    content = f[1]

    print(
        f"\033[?25l\033[2K\rindexing {name}",
        end="",
    )

    stemmer = SnowballStemmer("english")
    tokens: list[str] = [
        stemmer.stem(word) for word in wordpunct_tokenize(content.lower())
    ]

    tokens: list[str] = wordpunct_tokenize(content.lower())

    # getting term occurrencces for each token in the document and collecting them into a dict
    term_occurrences: dict[str, int] = {}

    for token in tokens:
        term_occurrence = 0

        for to_be_compared_token in tokens:
            token = token

            if token == to_be_compared_token:
                term_occurrence += 1

        term_occurrences[token] = term_occurrence

    return {name: term_occurrences}


def create_index_(dir: str):

    # get the file paths

    # paths = filter(
    #     lambda doc: doc.suffix in (".html"),
    #     pathlib.Path("documents/coryn.club/coryn.club").rglob("*"),
    # )

    # TODO (jma): TURN THIS TO SINGLE FUNCTION PROCESS NOW, THIS WILL BURN YOUR CPU
    # with Pool(1) as p:
    #     # count for occurrences
    #     term_occurrences_per_document: dict[str, dict[str, int]] = {}
    #     term_occurrences_in_all_documents: dict[str, int] = {}

    #     # save this as the result of multiprocessing
    #     term_occurrences_per_document_results = p.map(
    #         get_term_occurrences, paths, chunksize=1
    #     )

    #     for data in term_occurrences_per_document_results:
    #         term_occurrences_per_document.update(data)

    #         for path, occurrences in data.items():
    #             for term, _ in occurrences.items():
    #                 existing_occurrence = term_occurrences_in_all_documents.get(term)

    #                 # if existing_occurrence:
    #                 #     term_occurrences_in_all_documents[term] = occurrence + existing_occurrence1

    #                 # else:
    #                 #     term_occurrences_in_all_documents[term] = occurrence

    #                 if existing_occurrence:
    #                     term_occurrences_in_all_documents[term] = (
    #                         existing_occurrence + 1
    #                     )

    # return Index(
    #     tf_meta=term_occurrences_per_document,
    #     idf_meta=term_occurrences_in_all_documents,
    # )

    paths = filter(
        lambda doc: doc.suffix in (".html") and doc.is_file(),
        pathlib.Path("documents/coryn.club/coryn.club").rglob("*"),
    )

    term_occurrences_per_document: dict[str, dict[str, int]] = {}
    term_occurrences_in_all_documents: dict[str, int] = {}

    for path in paths:
        term_occurrences = get_term_occurrences(path)
        term_occurrences_per_document.update(term_occurrences)

        print(term_occurrences)

    for path, occurrences in term_occurrences_per_document.items():
        for term, _ in occurrences.items():
            existing_occurrence = term_occurrences_in_all_documents.get(term)

            if existing_occurrence:
                term_occurrences_in_all_documents[term] = existing_occurrence + 1

    return Index(
        tf_meta=term_occurrences_per_document,
        idf_meta=term_occurrences_in_all_documents,
    )


def get_term_occurrences_from_processed_file(
    f: tuple[str, str],
) -> dict[str, dict[str, int]]:

    name = f[0]
    content = f[1]

    print(
        f"\033[?25l\033[2K\rindexing {name}",
        end="",
    )

    stemmer = SnowballStemmer("english")
    tokens: list[str] = [
        stemmer.stem(word) for word in wordpunct_tokenize(content.lower())
    ]

    tokens: list[str] = wordpunct_tokenize(content.lower())

    # getting term occurrencces for each token in the document and collecting them into a dict
    term_occurrences: dict[str, int] = {}

    for token in tokens:
        term_occurrence = 0

        for to_be_compared_token in tokens:
            token = token

            if token == to_be_compared_token:
                term_occurrence += 1

        term_occurrences[token] = term_occurrence

    return {name: term_occurrences}


def get_term_occurrences_per_doc(file: str) -> dict[str, dict[str, float]]:

    print(
        f"\033[?25l\033[2K\rindexing {file}",
        end="",
    )

    with open(file, "r") as text:
        tokens: list[str] = wordpunct_tokenize(text.read())

        # getting term occurrencces for each token in the document and collecting them into a dict
        term_occurrences: dict[str, float] = {}

        for token in tokens:
            term_occurrence = 1

            for to_be_compared_token in tokens:
                token = token.lower()
                to_be_compared_token.lower()

                if token == to_be_compared_token:
                    term_occurrence += 1

            term_occurrences[token] = term_occurrence

        return {file: term_occurrences}


def tf(term: str, dto: dict[str, int]):

    terms = dto.keys()

    times_found = dto.get(term)
    return (times_found if times_found else 0) / len(terms)


def idf(term: str, index: Index):

    documents = index.tf_meta.items()

    total_n_docs = len(documents)

    total_n_docs_containing_term = index.idf_meta.get(term)

    return math.log(
        total_n_docs
        / (total_n_docs_containing_term if total_n_docs_containing_term else 1)
    )


def tf_idf(term: str, dto: dict[str, int], index: Index):

    return tf(term, dto) * idf(term, index)


def search(query: str, index: Index):
    stemmer = SnowballStemmer("english")
    query_terms: list[str] = [
        stemmer.stem(word) for word in wordpunct_tokenize(query.lower())
    ]

    # query_terms: list[str] = wordpunct_tokenize(query.lower())

    # get tf-idf of query

    results: list[tuple[str, float]] = []

    for path, doc_dto in index.tf_meta.items():
        score = 0
        for query_term in query_terms:
            score += tf_idf(query_term, doc_dto, index)

        results.append((path, score))

    return sorted(results, reverse=True, key=lambda e: e[1])[0:10]


def main():

    start = perf_counter()
    with open("model.json", "w") as i:
        index_asdict = create_index_("documents/coryn.club/coryn.club")._asdict()
        i.write(json.dumps(index_asdict))

    with open("model.json", "rb") as i:
        index: Index = Index(**json.load(i))

        query = "Dual bringer"
        print("\n", index)
        print(search(query, index))

    end = perf_counter()

    print(f"\nsearching finished ({(end - start):.2f}s)")


if __name__ == "__main__":
    main()

    # TODO (jma): make this a .exe file
