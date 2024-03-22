import os

import pandas as pd

class DemoMessages():
    """ Class to create a demo of a random message from a list and give back prediction and errors."""

    def __init__(self):
        static_demo_file = 'static/texts/demo_tweets.csv'
        if os.path.exists(static_demo_file):
            self.demo_df = pd.read_csv('static/texts/balanced_test_df.csv')
        else:
            self.demo_df = pd.read_csv('../static/texts/balanced_test_df.csv')


    def get_demo_tweet(self) -> str:
        """ random text from the csv list """
        return self.demo_df.sample(1).iloc[0]['clean_text']

    def get_demo_label(self, text: str) -> int:
        """ Find the label based on the text """
        label_row = self.demo_df[self.demo_df['clean_text'] == text]
        if len(label_row) > 0:
            return label_row.iloc[0]['labels']
        else:
            return -1

    def get_demo_error(self, text: str) -> str:
        """ Find the error based on the text """
        error_row = self.demo_df[self.demo_df['clean_text'] == text]
        if len(error_row) > 0:
            error = error_row.iloc[0]['error']
            return error if not pd.isna(error) else ''
        return ''


if __name__ == '__main__':
    handler = DemoMessages()
    text = handler.get_demo_tweet()
    label = handler.get_demo_label(text)
    error = handler.get_demo_error(text)
    print(f"Text = {text} \nLabel = {label} \nError = {error}")
