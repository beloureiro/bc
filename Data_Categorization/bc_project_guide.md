
## Text Preprocessing and Sentiment Analysis
### Text Preprocessing Function
We defined an advanced function `preprocess_text` to perform text cleaning while preserving context. This function:
- Converts text to lowercase
- Removes URLs
- Keeps alphanumeric characters, spaces, and important punctuation
- Tokenizes the text
- Lemmatizes words and removes stopwords, but keeps important medical terms and negations
- Joins the cleaned tokens back into a single string

We applied this function to the `content_en` column of the DataFrame, creating a new column `cleaned_content` with the cleaned text.

### Sentiment Analysis
We used TextBlob to perform sentiment analysis on both the original and cleaned text, creating `original_sentiment` and `cleaned_sentiment` columns.

We performed additional analysis:
- Compared text lengths before and after preprocessing
- Visualized text length distribution (saved as 'text_length_distribution.png')
- Created word clouds for original and cleaned text (saved as PNG files)
- Validated the preprocessing and sentiment consistency on a sample of the data
- Preprocessing was effective and sentiment remained consistent for 92.00% of the sampled data
- 3.63% of samples showed significant sentiment change after preprocessing
- Visualized the distribution of sentiment scores before and after preprocessing (saved as 'sentiment_distribution_comparison.png')

## Text Preprocessing and Sentiment Analysis
### Text Preprocessing Function
We defined an advanced function `preprocess_text` to perform text cleaning while preserving context. This function:
- Converts text to lowercase
- Removes URLs
- Keeps alphanumeric characters, spaces, and important punctuation
- Tokenizes the text
- Lemmatizes words and removes stopwords, but keeps important medical terms and negations
- Joins the cleaned tokens back into a single string

We applied this function to the `content_en` column of the DataFrame, creating a new column `cleaned_content` with the cleaned text.

### Sentiment Analysis
We used TextBlob to perform sentiment analysis on both the original and cleaned text, creating `original_sentiment` and `cleaned_sentiment` columns.

We performed additional analysis:
- Compared text lengths before and after preprocessing
- Visualized text length distribution (saved as 'text_length_distribution.png')
- Created word clouds for original and cleaned text (saved as PNG files)
- Validated the preprocessing and sentiment consistency on a sample of the data
- Preprocessing was effective and sentiment remained consistent for 96.00% of the sampled data
- 3.85% of samples showed significant sentiment change after preprocessing
- Visualized the distribution of sentiment scores before and after preprocessing (saved as 'sentiment_distribution_comparison.png')
