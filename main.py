import random
import string
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from textblob.np_extractors import ConllExtractor
from textblob import TextBlob

nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

extractor = ConllExtractor()

class DoraBot:
    def __init__(self):
        self.generic_responses = [
            "That's quite interesting. Please tell me more.",
            "Hmm... go on.",
            "Why do you think that?",
            "I didn’t expect that. Could you elaborate?",
            "Fascinating. What happened next?",
            "Really? What makes you say that?"
        ]

        self.topics = {
            "weather": ["Seems like weather always finds a way into conversation.", 
                        "Rain or shine, I'm always here."],
            "sports": ["Sports fans are passionate! Which team do you follow?", 
                       "Do you play or just watch?"],
            "music": ["Music connects us all. Got a favorite genre?", 
                      "What kind of music do you enjoy?"],
            "food": ["I'm more of a digital snacker. What's your go-to meal?", 
                     "Now I’m curious — sweet or spicy?"],
            "movies": ["Cinemas or streaming?", "I bet you enjoy a good plot twist."],
            "technology": ["Tech changes so fast! Anything new you’re excited about?",
                           "I guess I’m biased, but I love AI."]
        }

        self.memory = []
        self.previous_input = ""
        self.stop_words = set(stopwords.words('english'))
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def clean_input(self, text):
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        tokens = nltk.word_tokenize(text)
        return [word for word in tokens if word not in self.stop_words]

    def detect_topic(self, words):
        for word in words:
            if word in self.topics:
                self.memory.append(word)
                return word
        return None

    def analyze_sentiment(self, text):
        scores = self.sentiment_analyzer.polarity_scores(text)
        if scores['compound'] >= 0.5:
            return "positive"
        elif scores['compound'] <= -0.5:
            return "negative"
        else:
            return "neutral"

    def respond(self, user_input):
        cleaned_words = self.clean_input(user_input)
        sentiment = self.analyze_sentiment(user_input)
        topic = self.detect_topic(cleaned_words)

        if topic:
            return random.choice(self.topics[topic])
        elif sentiment == "positive":
            return "I'm glad to hear that. 😊"
        elif sentiment == "negative":
            return "Oh no, that doesn't sound good. Want to talk about it?"
        elif self.memory:
            remembered_topic = random.choice(self.memory)
            return f"Earlier you mentioned {remembered_topic}. {random.choice(self.topics[remembered_topic])}"
        else:
            return random.choice(self.generic_responses)

    def chat(self):
        print("Hello, I am Dora, your conversational bot.")
        print("You can type 'bye' anytime to exit.")

        while True:
            user_input = input("> ").strip()

            if user_input.lower() == "bye":
                print("It was nice talking to you. Take care! 👋")
                break
            
            user_input_blob = TextBlob(user_input, np_extractor=extractor)

            test = TextBlob(user_input)

            if user_input_blob.polarity <= -0.5:
                print("Oh dear, that sounds bad. ")
            elif user_input_blob.polarity <= 0:
                print("Hmm, that's not great. ")
            elif user_input_blob.polarity <= 0.5:
                print("Well, that sounds positive. ")
            elif user_input_blob.polarity <= 1:
                print("Wow, that sounds great. ")
            
            response = self.respond(user_input)
            print(response)
            translated = test.sentiment
            print(str(translated))

if __name__ == "__main__":
    bot = DoraBot()
    bot.chat()
