import pytest
import json

from tmclass_exercises.indexing import TextIndex
from tmclass_exercises.language_detector import get_language_detector
from tmclass_exercises import POETRY_FOLDER_PATH

with open(POETRY_FOLDER_PATH / 'metadata.json') as f:
    POETRY_METADATA = json.load(f)


@pytest.mark.xfail(reason="TODO: remove this xfail marker and fix the code")
def test_preprocess_text():
    index = TextIndex()

    # The index object can preprocess French text to put everything in lower
    # case and remove the accentuated characters.
    preprocessed = index.preprocess("C'est l'été !", language='fr')
    assert preprocessed == "c'est l'ete !"

    # English text is transformed to lower case: there is no accentuated
    # characters to "normalize".
    preprocessed = index.preprocess("Winter is coming!", language='en')
    assert preprocessed == "winter is coming!"

    # Persian and Japanese texts are unaffected by our proprocessing.
    preprocessed = index.preprocess("ای باغبان", language="fa")
    assert preprocessed == "ای باغبان"

    preprocessed = index.preprocess("古池や蛙飛び込む水の音", language="ja")
    assert preprocessed == "古池や蛙飛び込む水の音"


@pytest.mark.xfail(reason="TODO: remove this xfail marker and fix the code")
def test_tokenize_text():
    index = TextIndex()
    tokens = index.tokenize("winter is coming!", language="en")
    assert tokens == ["winter", "is", "coming"]

    tokens = index.tokenize("ای باغبان", language="fa")
    assert tokens == ["ای", "باغبان"]


@pytest.mark.xfail(reason="TODO: remove this xfail marker and fix the code")
def test_index_text():
    index = TextIndex()
    index.index_text("doc1", "winter is coming!", language="en")
    assert len(index) == 1

    index.index_text("doc2", "ای باغبان", language="fa")
    assert len(index) == 2

    assert index.lookup_token("winter") == ["doc1"]
    assert index.lookup_token("باغبان") == ["doc2"]


@pytest.mark.xfail(reason="TODO: remove this xfail marker and fix the code")
def test_index_french_text_files():
    index = TextIndex()
    index.index_text_file(POETRY_FOLDER_PATH / 'baudelaire.txt',
                          language="fr", encoding="iso-8859-15")
    index.index_text_file(POETRY_FOLDER_PATH / 'verlaine.txt',
                          language="fr", encoding="utf-8")
    assert len(index) == 2

    # Note that the following does not retrieve the occurence of the word
    # "automnes" from baudelaire.txt because we did not implement any
    # normalization strategy for plural forms. This minimal full-text index
    # could be improved in that respect.
    assert index.lookup_token("automne") == ["verlaine.txt"]

    # Common words can return many results in many documents.
    assert index.lookup_token("mon") == ["baudelaire.txt", "verlaine.txt"]

    # Token with accents are "normalized" to make it easy to query for
    # documents without having to type the accents.
    assert index.lookup_token("feeriques") == ["baudelaire.txt"]

    # Words not present in the indexed documents cannot be found as indexed
    # tokens:
    assert index.lookup_token("inexistant") == []


@pytest.mark.xfail(reason="TODO: remove this xfail marker and fix the code")
def test_index_english_text_files():
    index = TextIndex()
    index.index_text_file(POETRY_FOLDER_PATH / 'shakespeare.txt',
                          language="en", encoding="utf-8")

    assert index.lookup_token("thy") == ["shakespeare.txt"]
    assert index.lookup_token("holly") == ["shakespeare.txt"]


@pytest.mark.xfail(reason="TODO: remove this xfail marker and fix the code")
def test_index_persian_text_files():
    index = TextIndex()
    index.index_text_file(POETRY_FOLDER_PATH / 'rumi.txt',
                          language="fa", encoding="utf-8")
    assert index.lookup_token("خزان") == ["rumi.txt"]


@pytest.mark.xfail(reason="TODO: remove this xfail marker and fix the code")
def test_index_japanese_text_files():
    pytest.importorskip("janome")  # skip this test if janome is not installed

    index = TextIndex()
    index.index_text_file(POETRY_FOLDER_PATH / 'basho.txt',
                          language="ja", encoding="shift-jis")
    assert index.lookup_token("蛙") == ["basho.txt"]


@pytest.mark.skipif(get_language_detector() is None,
                    reason="Test requires the pre-trained language detector.")
@pytest.mark.xfail(reason="TODO: remove this xfail marker and fix the code")
def test_complex_queries_with_language_detection():
    index = TextIndex()
    index.index_text_file(POETRY_FOLDER_PATH / 'baudelaire.txt',
                          encoding="iso-8859-15")
    index.index_text_file(POETRY_FOLDER_PATH / 'rumi.txt',
                          encoding="utf-8")
    index.index_text_file(POETRY_FOLDER_PATH / 'shakespeare.txt',
                          encoding="utf-8")
    index.index_text_file(POETRY_FOLDER_PATH / 'verlaine.txt',
                          encoding="utf-8")

    assert index.query("feeriques palais") == ["baudelaire.txt"]
    assert index.query("Féeriques palais") == ["baudelaire.txt"]

    assert index.query("Winter Bite!") == ["shakespeare.txt"]
    assert index.query("سبزپوشان خزان") == ["rumi.txt"]

    assert index.query("unexistingtoken") == []


@pytest.mark.skipif(get_language_detector() is None,
                    reason="Test requires the pre-trained language detector.")
@pytest.mark.xfail(reason="TODO: remove this xfail marker and fix the code")
def test_complex_queries_with_language_detection_japanese():
    pytest.importorskip("janome")  # skip this test if janome is not installed

    index = TextIndex()
    index.index_text_file(POETRY_FOLDER_PATH / 'basho.txt',
                          encoding="shift-jis")
    index.index_text_file(POETRY_FOLDER_PATH / 'baudelaire.txt',
                          encoding="iso-8859-15")
    index.index_text_file(POETRY_FOLDER_PATH / 'rumi.txt',
                          encoding="utf-8")
    index.index_text_file(POETRY_FOLDER_PATH / 'shakespeare.txt',
                          encoding="utf-8")
    index.index_text_file(POETRY_FOLDER_PATH / 'verlaine.txt',
                          encoding="utf-8")

    assert index.query("蛙") == ["basho.txt"]
