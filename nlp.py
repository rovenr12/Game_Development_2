import re
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

spacy_nlp = spacy.load("en_core_web_sm")

# Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

def clean_text(text):
    # remove unicode characters
    text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)

    print(text)

    # get only noun and verbs
    doc = spacy_nlp(text)

    for token in doc:
        print(token.lemma_, token.pos_)

    words = [token.lemma_ for token in doc if token.pos_ in ["VERB", "ADJ", "ADV"] and not token.is_stop]

    print(words)

    return words


#calculate the intensity of sentiments in the given sentence
def get_sentiment_score(sentence):
    sentiment_dict = sid_obj.polarity_scores(sentence)
    intensity = sentiment_dict['compound']
  
    return intensity
