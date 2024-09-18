# DocPlanner Sentiment Categorization App

This repository contains the **DocPlanner Sentiment Categorization App**, a case study demonstrating the use of **Python** to create an interactive dashboard leveraging advanced **Natural Language Processing (NLP)** techniques. The project categorizes and analyzes patient reviews to generate valuable insights from unstructured textual data.

## Features

- **Sentiment Analysis**: Automatically evaluates the sentiment of patient feedback (positive, negative, neutral) using models like **VADER** and **BERT** for precise sentiment classification.
- **Text Categorization**: Classifies feedback into predefined categories such as `Service Issue`, `Cost Issue`, and `Product Effectiveness`, among others, identifying key pain points in patient reviews.
- **Interactive Dashboard**: Visualizes the processed data through dynamic charts and tables, enabling filtering by country, sentiment, and other relevant indicators.
- **Text Processing**: The text is cleaned, tokenized, and lemmatized using **NLTK**, with targeted sentiment adjustments made through a custom dictionary of negative words to improve accuracy in critical reviews.

## Methodology Overview

This project is part of the **Business Case Web App**, designed to explain the **Business Case Framework** in four stages. The framework starts by mapping the patient lifecycle, identifying critical touchpoints, and analyzing user feedback. Two Python-based NLP algorithms were developed specifically for this framework: the first focuses on text processing and sentiment analysis, while the second organizes the data and correlates the sentiment data with specific processes (touchpoints), generating sentiment scores for each process. These insights help in identifying key pain points, conducting root cause analysis, and guiding strategic action plans to improve patient care.

## Demonstration

You can access the application directly on Streamlit via the following link:

í´— [DocPlanner Sentiment Categorization App](https://dplanner.streamlit.app/)

## Technologies Used

- **Python**: Core language for the development of the application.
- **Streamlit**: Framework for creating interactive dashboards in Python.
- **NLTK** and **VADER**: Used for text processing and sentiment analysis.
- **spaCy** and **BERT**: Used for natural language processing, tokenization, and text classification.
- **Pandas**: For large-scale data manipulation.
- **Matplotlib**: Library for generating interactive data visualizations.
- **Multiprocessing**: To enable parallel processing for performance optimization.
- **JIT Compilation**: For additional performance enhancements.

## Project Structure

```
|-- processed_data.csv         # Pre-processed data used in the application
|-- app.py                     # Main application file for Streamlit
|-- requirements.txt           # Project dependencies
|-- README.md                  # This file
```

## How to Run the Project Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/USERNAME/REPO_NAME.git
   ```

2. Navigate to the project directory:
   ```bash
   cd REPO_NAME
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

5. Open the application in your browser at:
   ```bash
   http://localhost:8501
   ```

## Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request.


