# vectorizer.py
from threading import Lock

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import torch
import scipy.spatial.distance as ds
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity


class TextVectorizer:
    lemmatizer_lock = Lock()
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased-sentence")
        self.model = AutoModel.from_pretrained("DeepPavlov/rubert-base-cased-sentence")

    @staticmethod
    def preprocess_text(text: str):
        # Приведение к нижнему регистру
        text = text.lower()

        # Удаление пунктуации и других нежелательных символов
        text = re.sub(r'[^\w\s]', '', text)

        # Токенизация
        tokens = word_tokenize(text)

        # Удаление стоп-слов
        stop_words = set(stopwords.words('russian'))  # Используйте 'russian' для русского языка
        tokens = [token for token in tokens if token not in stop_words]

        with TextVectorizer.lemmatizer_lock:
            # Лемматизация
            lemmatizer = WordNetLemmatizer()
            tokens = [lemmatizer.lemmatize(token) for token in tokens]

        # Собираем обратно в строку
        return ' '.join(tokens)

    def vectorize(self, text: str):
        text = self.preprocess_text(text)
        t = self.tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(**{k: v.to(self.model.device) for k, v in t.items()})
        embeddings = model_output.last_hidden_state[:, 0, :]
        embeddings = torch.nn.functional.normalize(embeddings)
        return embeddings[0].cpu().numpy()

    def find_simular(self, origin: str, texts: list[str], top_n: int = 5, threshold: float = 0.9):
        vector_origin = self.vectorize(origin)
        vector_texts = []
        for text in texts:
            # print(text)
            vector_texts.append(self.vectorize(text))
        dis = ds.cdist([vector_origin], vector_texts)
        combined = list(zip(texts, dis[0]))
        sorted_combined = sorted(combined, key=lambda x: x[1])

        # Теперь мы можем выбрать первые n текстов
        lowest_coeff_texts = [text for text, coeff in sorted_combined[:10]]

        # for text in lowest_coeff_texts:
        #     print(self.preprocess_text(text), "\n ---------------------------------------------------------------")

        cos_sim = cosine_similarity([vector_origin], vector_texts)
        combined = list(zip(texts, cos_sim[0]))
        sorted_combined = sorted(combined, key=lambda x: -x[1])  # Сортируем по убыванию сходства
        lowest_coeff_texts = [text for text, coeff in sorted_combined[:10]]
        return lowest_coeff_texts
