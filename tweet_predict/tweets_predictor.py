import os

from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import html
import torch

MIN_TEXT_LENGTH = 4
MAX_TEXT_LENGTH = 280
OK = "valid"
FIX = "invalid"

class TweetsPredictor():
    """A Class to classify if Tweets are correct from the Grammar and Spelling only."""

    def __init__(self, model_directory: str):
        """
        Init a new TweetsPredictor with a given DistilBertForSequenceClassification.
        :param model_directory: str, path to model directory with Model (safeTensors and Tokenizer files)
        TODO: ONNYX convert and serve for x3-5 speed
        """
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_directory)
        self.model = DistilBertForSequenceClassification.from_pretrained(model_directory)
        # Supporting CPU and GPU - ok on CPU
        if torch.cuda.is_available():
            self.model = self.model.to('cuda')
        self.model.eval()

    def predict(self, text) -> str:
        """
        Predict on one tweet
        :param text: str, tweet raw text to predict on
        :return: str, "0"=Issue/s in text, "1"=Good text
        TODO: Support multiple message and batch then for one GPU action
        """
        # Convert HTML to text
        text = html.unescape(text)
        # Restrictions - length (since it's a 0/1 classifier, it's 0)
        if len(text) < MIN_TEXT_LENGTH or len(text) > MAX_TEXT_LENGTH:
            print(f"Text in size {len(text)} not supported.")
            return FIX
        # Pass - only @ (this is for user, we don't check and it's ok ->1)
        if text.strip().startswith("@") and not " " in text.strip():
            return OK

        # Tokenize and predict
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=350)
        # GPU use here is mostly to be consistent since for one message it's not that important
        #   (later there will be batch here according to use profile)
        if torch.cuda.is_available():
            inputs = {name: tensor.to(self.model.device) for name, tensor in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        predicted_class_id = logits.argmax(-1).item()
        return OK if str(predicted_class_id) == "1" else FIX

# sanity to test easily new models
if __name__ == "__main__":
    text_1 = "@thediscovietnam coo.  thanks. just dropped you a line."
    handler = TweetsPredictor('/home/user/IdeaProjects/x_grammar_spelling/model')

    while True:
        text = input("Enter text for prediction (type 'exit' to quit): ")
        if text == 'exit':
            break
        prediction = handler.predict(text)
        print(f"Prediction: {prediction}")
