import os
import time

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import pandas as pd
from tqdm import tqdm


class LllmClassifierGamma():
    """ Classify the tweets to yes and no according to grammar using llm keeping track on work done """

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path='/home/user/IdeaProjects/gamma-7b-hf')
        self.model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path='/home/user/IdeaProjects/gamma-7b-hf',
            device_map="auto",
            torch_dtype=torch.float16
        )
        with open('../prompts/x_classify_system_prompt_light.txt', 'r') as file:
            self.system_prompt = file.read()


    def classify_tweet(self, tweet_text: str) -> str:
        """
        Classify tweet to be spell and grammar correct ignoring slang, informal, icons and more.
        :param tweet_text: str, cleand (not html) X text
        :return: str, 'yes' if correct and 'no' with reason if not
        """
        #TODO: get instruction model
        chat = [
                {"role": "user", "content": self.system_prompt},
                {"role": "assignment", "content": 'OK'},
                {"role": "user", "content": tweet_text}
            ]
            # temperature=0.0,
            # top_p=0.0,
            # frequency_penalty=0.0,
            # presence_penalty=0.0
        # )
        prompt = self.tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)

        # outputs = self.model.generate(**input_ids)
        inputs = self.tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
        outputs = self.model.generate(input_ids=inputs.to(self.model.device), max_new_tokens=150)
        response = str(self.tokenizer.decode(outputs[0]))

        # simple formatting
        lines = response.split('\n')
        line_count = 0
        for line in lines:
            line_count += 1
            if "**Response:**" in line:
                break
        clean_response = '\n'.join(lines[(line_count + 1):])
        return clean_response

    def classify_and_extract(self, tweet):
        result = self.classify_tweet(tweet)
        if result.lower().startswith('yes') or result.lower().startswith('**yes'):
            return 1, ''
        else:
            return 0, result

if __name__ == "__main__":
    csv_file_path = '../data/clean_train_tweets.csv'
    classified_csv_path = '../data/raw_train_tweets_classified_gamma_light.csv'

    # Load the DataFrame containing tweets to classify
    df = pd.read_csv(csv_file_path)

    # Attempt to load an existing classified DataFrame; if it doesn't exist, initialize it
    try:
        classified_df = pd.read_csv(classified_csv_path)
    except FileNotFoundError:
        classified_df = pd.DataFrame(columns=['index', 'text', 'clean_text', 'classification', 'error'])

    handler = LllmClassifierGamma()
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
        start_time = time.time()
        classifications_errors = (
            batch_df['clean_text'].apply(lambda x: pd.Series(handler.classify_and_extract(x), index=['classification', 'error'])))
        print(f"Execution time for 10: {time.time() - start_time} seconds")

        # Concatenate the results with the original columns from batch_df
        batch_df = pd.concat([batch_df[['index', 'text', 'clean_text']], classifications_errors], axis=1)

        # Append results to classified_df
        classified_df = pd.concat([classified_df, batch_df], ignore_index=True)

        # Save progress
        classified_df.to_csv(classified_csv_path, index=False)
