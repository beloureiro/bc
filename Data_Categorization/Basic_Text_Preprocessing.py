# Nesta versão foram implementadas as seguintes melhorias:
# Summary of Improvements:
# 1. **Critical Expression Capture**: Refined text preprocessing to preserve critical expressions as single tokens, enhancing sentiment detection accuracy.
# 2. **Enhanced Negative Sentiment Weighting**: Adjusted sentiment weighting for critical phrases to better reflect negative feedback intensity.
# 3. **Multidimensional Sentiment Analysis**: Introduced sentence-level analysis for more granular and accurate sentiment assessment across long texts.
# 4. **Dynamic Sentiment Adjustment**: Implemented mechanism to modify sentiment scores when critical phrases are present but not adequately reflected in initial analysis.
# 5. **Optimized Negation Handling**: Enhanced negation handling by combining negation words with subsequent tokens, improving context preservation and analysis accuracy.
# 6. **Custom Stopwords Optimization**: Refined stopwords list to retain essential descriptive words and phrases critical for sentiment interpretation.
# 7. **Sentiment Validation and Correction**: Added validation step to cross-check preprocessing efficacy and sentiment consistency.
# 8. **Performance Optimization**: Leveraged multiprocessing for efficient parallel processing of large datasets.
# 9. **Code Enhancement**: Refined code structure, incorporated best practices, and removed redundant functionalities.
# 10. **Negative Words Validation**: Implemented logic to validate sentiment scores using a negative words dictionary, changing classification to negative if positive texts contain words from the dictionary.
# 11. **Sentiment Score Adjustment**: Added functionality to adjust sentiment scores based on the presence of negative words, preserving sentiment intensity while inverting polarity when necessary.

import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import os
import re
import logging
from functools import lru_cache
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import multiprocessing
from multiprocessing import Pool
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import csv

# Baixar dados necessários do NLTK (tokenizadores, stopwords e wordnet para lematização)
for resource in ['punkt', 'stopwords', 'wordnet']:
    try:
        nltk.download(resource, quiet=True)
    except Exception as e:
        logging.error(f"Failed to download {resource}: {str(e)}")

# Especificar o diretório para armazenamento dos dados do NLTK
nltk_data_dir = os.path.join(os.path.expanduser('~'), 'nltk_data')
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)
nltk.data.path.append(nltk_data_dir)

# Configuração de palavras a serem mantidas e limiar de mudança significativa no sentimento
WORDS_TO_KEEP = {'not', 'no', 'never', 'doctor', 'nurse', 'patient', 'hospital',
                 'clinic', 'treatment', 'medicine', 'correct', 'necessary',
                 'low', 'empathy', 'important', 'significant'}
SENTIMENT_THRESHOLD = 0.2

# Inicializar o lematizador e a lista de stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english')) - WORDS_TO_KEEP

# Inicializar o analisador de sentimento VADER
analyzer = SentimentIntensityAnalyzer()

# Dicionário de frases críticas negativas que devem ajustar o sentimento
critical_negative_phrases_weights = {
    'do_not_recommend': -0.9,  # Aumentado o peso negativo
    'not_recommend': -0.8,
    'poor_service': -0.5,
    'bad_experience': -0.5,
    'terrible': -0.7,
    'horrible': -0.7,
    'awful': -0.7,
    'worst': -0.9,
    'never again': -0.8,
    'disappointed': -0.6
}

@lru_cache(maxsize=10000)
def preprocess_text(text):
    """
    Função para pré-processar o texto: limpeza, tokenização e lematização.
    Usa cache para acelerar chamadas repetidas com o mesmo texto.
    """
    if not isinstance(text, str):
        return ''
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\b\d+\b', '', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    # Manter "do not recommend" e outras frases críticas juntas
    text = re.sub(r'\b(i\sdo\snot|don\'t)\s(recommend)\b', r'do_not_recommend', text)
    text = re.sub(r'\b(not|no|never)\b\s+\b(\w+)\b', r'\1_\2', text)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) if word not in WORDS_TO_KEEP else word for word in tokens]
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [word for word in tokens if len(word) > 1]
    return ' '.join(tokens)

@lru_cache(maxsize=10000)
def get_sentiment(text):
    """
    Função para calcular a polaridade do sentimento do texto usando VADER,
    com ajustes para frases críticas.
    """
    score = analyzer.polarity_scores(text)['compound']
    for phrase, weight in critical_negative_phrases_weights.items():
        if phrase in text:
            score += weight
    return max(min(score, 1.0), -1.0)

def process_chunk(chunk):
    """
    Função para processar um pedaço do DataFrame: limpar o texto, calcular o sentimento e medir a mudança de sentimento.
    """
    try:
        chunk['cleaned_content'] = chunk['content_en'].apply(preprocess_text)
        chunk['original_sentiment'] = chunk['content_en'].apply(get_sentiment)
        chunk['cleaned_sentiment'] = chunk['cleaned_content'].apply(analyze_multidimensional_sentiment)
        chunk['sentiment_difference'] = abs(chunk['original_sentiment'] - chunk['cleaned_sentiment'])
        chunk = chunk.apply(validate_and_adjust_sentiment, axis=1)
        return chunk
    except Exception as e:
        logging.error(f"Error processing chunk: {str(e)}")
        return None

def validate_and_adjust_sentiment(row):
    """
    Função para validar e ajustar o sentimento se houver discrepância significativa.
    """
    if row['sentiment_difference'] < SENTIMENT_THRESHOLD and 'do_not_recommend' in row['cleaned_content']:
        row['cleaned_sentiment'] -= 0.5  # Ajustar dinamicamente o sentimento se houver uma discrepância
    return row

def analyze_multidimensional_sentiment(text):
    """
    Função para analisar o sentimento multidimensional de um texto, avaliando várias sentenças separadamente.
    """
    sentences = nltk.sent_tokenize(text)
    if len(sentences) == 0:  # Verifica se há sentenças para evitar divisão por zero
        return 0  # Retorna um valor neutro ou outro valor apropriado
    sentiment_scores = [get_sentiment(sentence) for sentence in sentences]
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    return avg_sentiment

def validate_preprocessing(row):
    """
    Função para validar a eficácia do pré-processamento de texto e verificar a consistência do sentimento.
    """
    original = set(row['content_en'].lower().split())
    cleaned = set(row['cleaned_content'].split())
    removed = original - cleaned
    sentiment_changed = row['sentiment_difference'] > SENTIMENT_THRESHOLD
    return len(removed) > 0 and len(cleaned) > 0 and not sentiment_changed

def load_negative_words(file_path):
    """
    Carrega as palavras negativas do arquivo CSV.
    """
    negative_words = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Pula o cabeçalho
        for row in reader:
            if row:  # Verifica se a linha não está vazia
                word = row[0].split(',')[0].strip().lower()
                negative_words.add(word)
    return negative_words

def validate_sentiment(text, sentiment_score, negative_words):
    """
    Valida o sentimento com base nas palavras negativas presentes no texto.
    """
    words = text.lower().split()
    for word in words:
        if word in negative_words:
            return -abs(sentiment_score)  # Retorna um valor negativo
    return sentiment_score

def main(df):
    """
    Função principal para executar o fluxo de pré-processamento e análise de sentimento no DataFrame.
    """
    logging.info("Starting preprocessing and sentiment analysis")

    # Carrega as palavras negativas
    negative_words = load_negative_words('D:/OneDrive - InMotion - Consulting/BusinessCase/Data_Categorization/negative_words_DataFrame.csv')

    num_processes = min(4, multiprocessing.cpu_count())

    with Pool(num_processes) as pool:
        chunks = np.array_split(df, num_processes)
        results = pool.map(process_chunk, chunks)

    results = [r for r in results if r is not None]

    if not results:
        logging.error("All chunks failed to process")
        return

    df = pd.concat(results)

    # Aplica a validação de sentimento
    df['validated_sentiment'] = df.apply(lambda row: validate_sentiment(row['cleaned_content'], row['cleaned_sentiment'], negative_words), axis=1)

    logging.info("Preprocessing and sentiment analysis completed")

    df['original_length'] = df['content_en'].str.len()
    df['cleaned_length'] = df['cleaned_content'].str.len()

    print("\nAverage text length:")
    print(f"Original: {df['original_length'].mean():.2f}")
    print(f"Cleaned: {df['cleaned_length'].mean():.2f}")

    sample_size = min(100, len(df))
    sample = df.sample(sample_size)
    validation_results = sample.apply(validate_preprocessing, axis=1)
    validation_percentage = (validation_results.sum() / sample_size) * 100

    print(f"\nPreprocessing and Sentiment Validation:")
    print(f"Percentage of samples with effective preprocessing and consistent sentiment: {validation_percentage:.2f}%")

    significant_changes = (df['sentiment_difference'] > SENTIMENT_THRESHOLD).sum()
    significant_change_percentage = (significant_changes / len(df)) * 100

    print(f"\nSentiment Change Analysis:")
    print(f"Percentage of samples with significant sentiment change: {significant_change_percentage:.2f}%")

    print("\nSentiment Validation Results:")
    print(f"Samples with changed sentiment: {(df['cleaned_sentiment'] != df['validated_sentiment']).sum()}")
    print(f"Percentage of samples with changed sentiment: {((df['cleaned_sentiment'] != df['validated_sentiment']).sum() / len(df)) * 100:.2f}%")

    logging.info("Analysis completed")

    df.to_csv(os.path.join(output_dir, 'processed_data.csv'), index=False)
    logging.info(f"Processed data saved to {os.path.join(output_dir, 'processed_data.csv')}")

if __name__ == "__main__":
    output_dir = "."

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = pd.read_csv('Business Case PC PM - database - raw_Data.csv', encoding='utf-8')

    df = df.drop(columns=['@'])
    df = df[df['content_en'].notnull()]

    try:
        main(df)
    except Exception as e:
        logging.error(f"An error occurred in main: {str(e)}")

# Para rodar no Git Bash
#   source venv/Scripts/activate
#   python Basic_Text_Preprocessing.py
