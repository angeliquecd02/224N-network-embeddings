import nltk
import re
import json
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pickle

# Download necessary NLP resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))

    # Lowercasing & removing special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())
    #remove urls
    text = re.sub(r"http[s]?\S+|www\.\S+", "", text)

    # Tokenization
    tokens = word_tokenize(text)

    # Removing stopwords and lemmatizing
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]

    return tokens

def subreddit_to_text(in_dir,out_dir):
    for filename in os.listdir(in_dir):
        input_file = os.path.join(in_dir,filename)
        output_file = os.path.join(out_dir,filename)
        with open(input_file, "r", encoding="utf-8") as infile, open(output_file, 'w') as outfile:
            all_data = json.load(infile)  # Load JSON data
            text_data = [post["selftext"] for post in all_data]
            processed_data = [preprocess_text(line) for line in text_data]
            for example in processed_data:
                outfile.write(str(example)+"\n")
# Process all text

def main():
    subreddit_to_text("../raw_data/sample_1/filtered_data","../text")

if __name__ == "__main__":
    main()
