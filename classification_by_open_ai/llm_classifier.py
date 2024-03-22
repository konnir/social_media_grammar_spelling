import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
from tqdm import tqdm


class LllmClassifier():
    """ Classify the tweets to yes and no according to grammar using llm keeping track on work done """

    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.system_prompt = None
        with open('../prompts/x_classify_system_prompt.txt', 'r') as file:
            self.system_prompt = file.read()


    def classify_tweet(self, tweet_text: str) -> str:
        """
        Classify tweet to be spell and grammar correct ignoring slang, informal, icons and more.
        :param tweet_text: str, cleand (not html) X text
        :return: str, 'yes' if correct and 'no' with reason if not
        """
        #TODO: check if more clean shoudl be applied (like emojis, urls, hashtags and more)

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # Specify the model here
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": tweet_text}
            ],
            temperature=0.0,
            top_p=0.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].message.content

    def classify_and_extract(self, tweet):
        result = self.classify_tweet(tweet)
        if result.lower().startswith('yes'):
            return 1, ''
        else:
            return 0, result

if __name__ == "__main__":
    csv_file_path = '../data/clean_train_tweets.csv'
    classified_csv_path = '../data/raw_train_tweets_classified_open_ai.csv'

    # Load the DataFrame containing tweets to classify
    df = pd.read_csv(csv_file_path)

    # Attempt to load an existing classified DataFrame; if it doesn't exist, initialize it
    try:
        classified_df = pd.read_csv(classified_csv_path)
    except FileNotFoundError:
        classified_df = pd.DataFrame(columns=['index', 'text', 'clean_text', 'classification', 'error'])

    handler = LllmClassifier()
    if 'index' not in df.columns:
        df.reset_index(inplace=True)
    # Ensure index is the first column if it's not already in the DataFrame
    if 'index' not in df.columns:
        df.reset_index(inplace=True)

    # Iterate through messages in df, 10 at a time
    counter = 0
    for start in tqdm(range(0, len(df), 10)):
        # Select a batch of 10 messages
        batch_df = df.iloc[start:start+10]

        # Filter out messages already classified
        batch_df = batch_df[~batch_df.index.isin(classified_df['index'])]
        if len(batch_df) < 1:
            print('skip')
            continue

        # Apply classify_and_extract function
        classifications_errors = (
            batch_df['clean_text'].apply(lambda x: pd.Series(handler.classify_and_extract(x), index=['classification', 'error'])))

        # Concatenate the results with the original columns from batch_df
        batch_df = pd.concat([batch_df[['index', 'text', 'clean_text']], classifications_errors], axis=1)

        # Append results to classified_df
        classified_df = pd.concat([classified_df, batch_df], ignore_index=True)

        # Save progress
        classified_df.to_csv(classified_csv_path, index=False)
