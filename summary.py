from re import L
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter, defaultdict


def initialize():
    nltk.download('punkt')
    nltk.download('stopwords')


def summarize(text: str) -> str:
    stopWords = set(stopwords.words('english'))
    words = word_tokenize(text)

    counter = Counter(words)

    for word in stopWords:
        if word in counter:
            del counter[word]

    sentences = sent_tokenize(text)
    sentVal = defaultdict(int)

    for sentence in sentences:
        for word in sentence.lower():
            sentVal[sentence] += counter[word] if word in counter else 0


    sum_values = sum(sentVal.values())
    avg = sum_values // len(sentVal)

    summary = ''
    for sentence in sentences:
        if (sentence in sentVal) and (sentVal[sentence] > (1.2 * avg)):
            summary += " " + sentence

    return summary