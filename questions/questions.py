import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """ 
    files_dict = {}
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), encoding="utf-8") as file:
            data = file.read()
            files_dict[filename] = data

    return files_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = []
    words = nltk.word_tokenize(document.lower())
    for word in words:
        if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english"):
            tokens.append(word)
    
    return tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs_dict = {}
    for file in documents:
        for word in documents[file]:
            if word not in idfs_dict:
                idfs_dict[word] = 0

    for word in idfs_dict:
        for file in documents:
            if word in documents[file]:
                idfs_dict[word] += 1

    total_docs = len(documents)
    for word in idfs_dict:
        idfs_dict[word] = math.log(total_docs / idfs_dict[word])
    
    return idfs_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_tf_idf = {}
    for file in files:
        total_tf_idfs = []
        for word in query:
            word_num = files[file].count(word)
            if word_num != 0:
                tf_idf = word_num * idfs[word]
                total_tf_idfs.append(tf_idf)
        file_tf_idf[file] = sum(total_tf_idfs)

    return [item[0] for item in sorted(file_tf_idf.items(), key=lambda x:-x[1])[:n]]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    m_w_m = {}
    for sentence in sentences:
        for word in query:
            if word in sentences[sentence]:
                if sentence in m_w_m:
                    m_w_m[sentence]["idf"] += idfs[word]
                    m_w_m[sentence]["qtd"] += sentences[sentence].count(word) / len(sentences[sentence])
                else:
                    m_w_m[sentence] = {"idf": idfs[word], "qtd": sentences[sentence].count(word) / len(sentences[sentence])}
    
    return [item[0] for item in sorted(m_w_m.items(), key=lambda x:(-x[1]["idf"], -x[1]["qtd"]))[:n]]


if __name__ == "__main__":
    main()
