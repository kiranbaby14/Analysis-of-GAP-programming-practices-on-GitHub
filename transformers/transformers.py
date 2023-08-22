import re
from sklearn.base import BaseEstimator, TransformerMixin
import chardet  # an ML model, It uses machine learning to detect the encoding of a file
import requests


# Custom transformer to remove numbers from text
class NumberRemovalTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Remove numbers using regular expression
        return [re.sub(r'\d+', '', text) for text in X]


# Custom transformer to remove non-ASCII characters from the given text using a regular expression.
class NonASCIIRemovalTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # remove non-ASCII characters from the given text using a regular expression.
        return [re.sub(r'[^\x00-\x7F]+', '', text) for text in X]


# Custom transformer to remove multiple spaces from the content
class MultipleSpacesRemovalTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        #  remove multiple spaces from the content
        return [" ".join(text.split()) for text in X]


class UrlToContentTransformer(BaseEstimator, TransformerMixin):
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

                    transformed_X.append(decoded_content)
                    break
                except Exception as e:
                    decoded_content = content.decode("utf-8")
                    transformed_X.append(decoded_content)
                    break
        return transformed_X