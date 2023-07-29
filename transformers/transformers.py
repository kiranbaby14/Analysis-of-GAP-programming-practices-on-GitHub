import re
from nltk.corpus import stopwords
from sklearn.base import BaseEstimator, TransformerMixin
import chardet  # an ML model, It uses machine learning to detect the encoding of a file
import requests


# Custom transformer for case-folding
class CaseFoldingTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [x.lower() for x in X]


# Custom transformer for stop words removal
class StopWordsRemovalTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        stop_words_list = stopwords.words('english')
        return [' '.join([word for word in x.split() if word not in stop_words_list]) for x in X]

    # Custom transformer to remove numbers from text


class NumberRemovalTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Remove numbers using regular expression
        return [re.sub(r'\d+', '', text) for text in X]


def remove_non_ascii(text):
    """
    Remove non-ASCII characters from the given text using a regular expression.
    """
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)
    return cleaned_text


class UrlToContentTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        transformed_X = []
        for url in X:
            while True:
                try:
                    response = requests.get(url)
                    content = response.content
                    encoding = chardet.detect(content)

                    if encoding['encoding'] == "ISO-8859-1":
                        decoded_content = content.decode("iso-8859-1")
                    elif encoding['encoding'] == "GB2312":
                        decoded_content = content.decode("GB2312")
                    else:
                        decoded_content = content.decode("utf-8")

                    # Remove non-ASCII characters from the decoded content
                    cleaned_content = remove_non_ascii(decoded_content)

                    transformed_X.append(cleaned_content)
                    break
                except Exception as e:
                    print(url)
                    decoded_content = content.decode("utf-8")
                    cleaned_content = remove_non_ascii(decoded_content)
                    transformed_X.append(cleaned_content)
                    break
        return transformed_X
