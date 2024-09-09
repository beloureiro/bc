import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import pandas as pd
import numpy as np
import spacy
import warnings
from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax
import torch

# Suprimir avisos específicos
warnings.filterwarnings("ignore", message=".*clean_up_tokenization_spaces.*")

# Carregar modelo de NLP do spaCy para processamento de texto em inglês
nlp = spacy.load("en_core_web_sm")

# Carregar tokenizer e modelo BERT para classificação
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=5)

# Função para extrair entidades nomeadas do texto (como nomes de médicos, hospitais, locais)
def extract_entities(text):
    if pd.isna(text) or not isinstance(text, str):
        return {"doctor_name": [], "hospital_name": [], "location": []}

    doc = nlp(text[:1000])  # Limitar o tamanho do texto processado
    entities = {"doctor_name": [], "hospital_name": [], "location": []}
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities["doctor_name"].append(ent.text)
        elif ent.label_ == "ORG":
            entities["hospital_name"].append(ent.text)
        elif ent.label_ in ["GPE", "LOC"]:
            entities["location"].append(ent.text)
    return entities  # Retorna as entidades encontradas no texto

# Nova função para categorizar o texto usando BERT
def categorize_with_bert(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    probabilities = softmax(outputs.logits, dim=1)
    category = torch.argmax(probabilities, dim=1).item()
    
    # Atualizando o mapeamento do índice da categoria para a string correspondente
    categories = {
        0: "Scheduling Issue", 
        1: "Wait Time Issue", 
        2: "Facility Issue", 
        3: "Staff Behavior", 
        4: "Remote Consultation Issue", 
        5: "Quality of Care", 
        6: "Cost Issue", 
        7: "General Issue"
    }
    
    return categories[category]

# Função para categorizar o texto usando palavras-chave mais específicas
def categorize_text(text):
    text = text.lower()
    if any(word in text for word in ["appointment", "schedule", "booking", "availability", "reschedule", "cancel", "slot", "time"]):
        return "Scheduling Issue"
    elif any(word in text for word in ["wait", "delay", "time", "queue", "line", "long", "late", "hours", "minutes"]):
        return "Wait Time Issue"
    elif any(word in text for word in ["environment", "clean", "comfort", "facility", "room", "dirty", "noisy", "air", "temperature", "seat"]):
        return "Facility Issue"
    elif any(word in text for word in ["rude", "unprofessional", "attitude", "behavior", "empathy", "disrespect", "kind", "courteous", "impolite", "manner", "not_respond"]):
        return "Staff Behavior"
    elif any(word in text for word in ["remote", "online", "virtual", "connection", "technical", "internet", "video", "call", "app", "platform", "access", "lag", "glitch"]):
        return "Remote Consultation Issue"
    elif any(word in text for word in ["treatment", "diagnosis", "care", "medical", "quality", "effectiveness", "therapy", "consultation", "follow-up", "prescription", "medication", "drugs", "test", "result", "wrong"]):
        return "Quality of Care"
    elif any(word in text for word in ["cost", "price", "expensive", "affordable", "billing", "charge", "fee", "payment", "insurance", "refund", "coverage", "invoice"]):
        return "Cost Issue"
    else:
        return "General Issue"

# Esta função foi expandida para incluir um número máximo de palavras negativas conforme extras
# Esta é a nova versão da função para categorizar texto, incluindo palavras negativas comuns.

# Função principal de processamento do DataFrame
def process_text(df):
    df = df.copy()  # Evitar SettingWithCopyWarning

    # Substituir valores NaN por strings vazias e converter para string
    df["cleaned_content"] = df["cleaned_content"].fillna("").astype(str)

    # Extração de entidades nomeadas do texto
    df["entities"] = df["cleaned_content"].apply(extract_entities)
    df["doctor_name"] = df["entities"].apply(lambda x: ",".join(x["doctor_name"]))
    df["hospital_name"] = df["entities"].apply(lambda x: ",".join(x["hospital_name"]))
    df["location"] = df["entities"].apply(lambda x: ",".join(x["location"]))

    # Categorização dos depoimentos usando a nova função baseada em palavras-chave
    df["category_keywords"] = df["cleaned_content"].apply(categorize_text)

    # Categorização dos depoimentos usando BERT
    df["category_bert"] = df["cleaned_content"].apply(categorize_with_bert)

    # Lógica para preencher issue_type, urgency_level, resolution_suggestion
    df["issue_type"], df["urgency_level"], df["resolution_suggestion"] = zip(
        *df.apply(refine_issue_classification, axis=1)
    )

    return df

# Função atualizada para refinar a classificação de 'issue_type', 'urgency_level' e 'resolution_suggestion'
def refine_issue_classification(row):
    cleaned_sentiment = row['cleaned_sentiment']

    if "Service Issue" in row['category_bert'] or cleaned_sentiment < -0.5:
        return "Critical", "High", "Immediate Action Required"
    elif cleaned_sentiment < 0:
        return "Non-Critical", "Medium", "Monitor Closely"
    else:
        return "Non-Critical", "Low", "Monitor"

# Função auxiliar para o processamento em paralelo de cada chunk do DataFrame
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')  # Linha ajustada

def process_chunk(chunk):
    try:
        logging.info(f"Processing chunk of size {len(chunk)}")
        result = process_text(chunk)
        logging.info(f"Finished processing chunk of size {len(chunk)}")
        return result
    except Exception as e:
        logging.error(f"Error processing chunk: {e}")
        logging.error(f"Chunk shape: {chunk.shape}")
        logging.error(f"Chunk columns: {chunk.columns}")
        logging.error(f"First few rows of cleaned_content:\n{chunk['cleaned_content'].head()}")
        return chunk  # Retorna o chunk original em caso de erro

# Função para paralelizar o processamento do DataFrame
def process_with_timeout(func, args, timeout=300):
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func, *args)
        try:
            return future.result(timeout=timeout)
        except TimeoutError:
            print(f"Processing timed out after {timeout} seconds")
            return None

def parallelize_dataframe(df, func, n_cores=2, batch_size=500, timeout=300):
    df_split = [df[i:i+batch_size] for i in range(0, len(df), batch_size)]
    with ThreadPoolExecutor(max_workers=n_cores) as executor:
        futures = [executor.submit(
            process_with_timeout, func, (batch,), timeout) for batch in df_split]
        results = [f.result() for f in as_completed(
            futures) if f.result() is not None]
    return pd.concat(results)

# Execução do script principal
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting data processing")

    logging.info("Loading data from CSV")
    df = pd.read_csv(
        'D:/OneDrive - InMotion - Consulting/BusinessCase/Data_Categorization/processed_data.csv', encoding='utf-8')

    if '@' in df.columns:
        df = df.drop(columns=['@'])

    logging.info(f"Data loaded. Shape: {df.shape}")
    logging.info(f"Columns: {df.columns}")
    logging.info(f"Data types: {df.dtypes}")

    try:
        logging.info("Starting parallel processing")
        df = parallelize_dataframe(
            df, process_chunk, n_cores=2, batch_size=500)
        logging.info("Parallel processing completed")

        logging.info("Saving processed data")
        df.to_csv("processed_data_categorized.csv", index=False)
        logging.info(
            "Processed and categorized data saved to 'processed_data_categorized.csv'")
    except Exception as e:
        logging.error(f"An error occurred during processing: {e}")
        logging.info("Saving partial results")
        df.to_csv("processed_data_categorized_partial.csv", index=False)
        logging.info(
            "Partial processed data saved to 'processed_data_categorized_partial.csv'")



# to run the app on gitbash
# python Data_Categorization.py
