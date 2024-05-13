<p align="left">
<!--   <img src="https://github.com/konnir/x_grammar_spelling/assets/119952960/f415aef0-dd6b-4223-81be-9ce5d677b53a" alt="anyword_logo" width="150" style="margin-left: 50px;"/> -->
  <img src="https://github.com/konnir/x_grammar_spelling/assets/119952960/aaae3161-5d93-4e82-87bf-1ac468f1817a" alt="Nir_Kon_Logo_inverted (1)" width="100"/>
</p>

# x_grammar_spelling
Check grammar and spelling on X messages with consideration on use of slang, shortcuts and hashtags.

Welcome to the Tweet Checker!
It has trained on social media style messages and will support informal english, and all tweeter special symbols. 

# First, what is it and what it can do (demo taste)?

![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/2b688193-3e8f-4e3f-98c5-6ff086e535b8)

***. Yes, it's a 2010 tweets - there was no Wassup back than.

# How it was made?

Data - Cheng-Caverlee-Lee geo-location tweets, 2010", 5M Tweets (used 50K for POC)
Models:
*. GPT-3.5-Turbo (OpenAI, 175B parameters)
*. DistilBERT (distilbert-base-uncased, 134M parameters, F32, Multilingual, 2019)
Train: 
*. Fine tuned “DistilBERT” on 50k for binary classification task: :Valid / InValid, 
*. PyTorch using Hugging Face
How?
*. Used prompt try and error to get the perfect prompt
*. Predicted 50K tweets with GPT-3.5-Turbo as “Source Of Truth”
Results:
*. General accuracy is 86% (F1, micro), for "Valid" 92% (F1) and for "InValid" 59% (F1, minority class 18%).


# How can I work with it?

![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/90fc849d-599f-4a88-9818-7c806a2cdfd5)

## The code - all in the Git, follow this order for simplicity:
- Server: 
  - ***tweets_server.py*** -  Fast API server code. 
  - ***tweet_predict/tweets_predictor.py*** - Class to classify if Tweets are correct from the Grammar and Spelling only.
- Prediction model:
  - ***/model*** - hold the model and the tokenizer files (GIT LFS). 
- Data Set Exploration:
  - ***ds_exploration/5_M_ds_set_up.ipynb*** - notebook for full data exploration and set up for creating labels and trains.
  - ***ds_exploration/5_M_ds_set_up.ipynb*** - small addition to the above (found later).
- Labels Creations by OpenAI API:
  - ***classification_by_open_ai/llm_classifier.py*** - Classify the tweets to yes and no according to grammar using llm keeping track on work done
  - ***classification_by_open_ai/llm_clean_up_and_order.ipynb*** - notebook to explore and handle all the cleaning and ordering of the OpenAI result (sometimes messy). 
  - ***prompts/x_classify_system_prompt.txt*** - system prompt for X classification (long).
- Fine Tune DistilBERT
  - ***classification_distil_bert/distilbert_x_model.ipynb*** - notebook to explore option for DistilBERT fine tune on the data including class weight and - multiple models, epochs and save TEST for UI demo later. 
- UI and Demo:
  - ***templates/index.html*** - simpleJS based demo to test and get direct impression for demonstration and R&D purposes. 
  - ***static/images*** - images folder for the project. 
  - ***demo_texts/demo_messages.py*** - Class to create a demo of a random message from a list and give back prediction and errors
  - ***static/texts/balanced_test_df.csv*** -  a TEST ds with balanced valid and invalid messages and their errors from OpenAI for the "Demo" button 
- Data:
  - ***data/raw_train_tweets_classified_open_ai.csv*** - about 3M of the full raw data set (git LFS, 688 MB)
  - ***data/clean_train_tweets.csv*** - DS after send to open AI and enriched with "labels" and "error" columns (git LFS, 8 MB)
  - ***data/clean_train_tweets_classified_open_ai.csv*** - ds for train after cleanup OpenAI issues (git LFS, 4 MB)
- Other:
  - ***resources_and_plan/X_resources.ods*** - list of resources for tweets. 

## Content (short summary):
- Collection and pre-processing of X messages:
  - Tried to look on X API to scrape tweets from there and got cold shoulder from the new Management, only 1500 can be scraped for day with frighting license. 
  - Collected many tweets data sets from all over the internet (turn out that the license on X change and many were deleted).
  - The chosen data set is a huge (5M) messages:
    - US tweets on different subjects created for geo-location research.
    - collected in 2009-2010 (more than enough for POC use, old informal English and terms.
    - From about 110K different users.
    - DS Source: https://archive.org/details/twitter_cikm_2010
    - Article: https://www.researchgate.net/publication/221614898_You_are_where_you_Tweet_A_content-based_approach_to_geo-locating_Twitter_users
  - Basic clean - empty, duplicated, URL, special characters
    - Fairly clean DS - main work was to remove just one @ annotation and to decode html.  
  - Handle X special -
    - Tweeter has many signs and types like Hashtags and DM messages, decided to keep as is.
    - Emoji, many in my DS and also decided to keep them as is. 
  - Handle slang and shortcuts:
    - After researching a little wi decided to keep all slang as is.
    - Same for shortcuts and other, seems like the LLM classifiers later can deal with them.
  - General:
    - DS is 140 character in the majority (see below for box plots), I decided to clean all above 280 characters and below 3 out of the DS and POC. 
- DS creation (with OpenAI GPT.3.5-Turbo):
  - Looking to create a ground of truth I choose the OpenAI due to the API availability.
  - The "playground" OpenAI offer helped me to form the right pompt for my tweets and evalute the quality. 
  - pros:
    - Industry standard.
    - Availability.
    - low price.
    - Fast.
  - Cons:
    - Limit of 10k messages a day (I'm very low on the tears, company get much more)
    - Not as good as gpt-4.0-turbo.
    - API not perfect, you can't set temperature=0 and top_p=0. 
- Classifier Creation:
  - DistilBert was chosen due to the each of train and proven record on text simple classifications tasks.
  - Pros:
    - 65M parameters but get the work done for simple tasks.
    - Light, ~200MB with 65M parameters.
    - Fast on GPU and CPU if needed for inference.
    - Short train time compared to Bert / Roberta / GPT-2 that were candidate for this.
  - Cons:
    - I took Hugging Face version with PyTorch, it was probably not the best: change the class weights and everyhting didn't work from there. 
- Web service:
  - Create Rest server to receive messages and return classifications thorough predictor. 
  - Expends to multiple messages for later GPU utilization. 
- Demo UI:
  - For visualization and deeper understanding of the data and the problem domain. 
  - Create a simple ui to type the message and present if OK or FIX. 
  - Expand ui to show the OpenAi answer on the message (from test).
 
## Data Exploration (see /ds_exploration/5_M_ds_set_up.ipynb):
- 3,609,675 tweets.
- First step, take the first 5 lines to see how to work here:<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/ecad9926-2213-4ae7-936f-886b41a04201)

- Let's go for df:<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/f0ea291e-257e-4c6e-a456-c65ca9e0acb0)

- 80,807 nulls were dropped.
- 119,065 duplicates were dropped (left one).
- 939 messages shorter than 4 characters were doped (our task is context).<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/b015d5c8-1532-4e9f-b5b3-477188d8bdd9)

- longest message is: 31,135 characters.
- Looking on long messages:<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/9667a0d0-cceb-4fcd-9433-6611bdefb713)

- Decided to keep the limit of tweeter (280) and droped all longer than this.
- Looking on messages length:<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/5e80b75a-9bbe-48ee-9113-2caf7b0b1327)

- most frequent length is 140 (box plot later)
- Looking on Tweeter specials: RT (22K), DM(13K), "t.com" - no need to remove them.
- Decide to convert all text from html to plain text (came out in the icons). 
- Looking into icons:<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/b4a901da-e31b-4fa2-b44a-6a3ddc39d071)

- Looking on icons and symboles, also no need to remove:<br>
 ![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/fc8b5919-5bcb-4d1c-a3a0-58dff8aca0f3)

- save to clean_train_tweets.csv for later work. 

# Create Data Set with LLM, OpenAI GPT.3.5-Turbo - (see classification_by_open_ai/llm_classifier.py):
- First step, adapt prompt in the playground of OpenAI and send a lot of messages:
- https://platform.openai.com/playground/p/default-grammar?mode=chat&model=gpt-3.5-turbo<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/72b15340-87c5-42c8-a6c3-0dc633909df8)

- Selected system promt (consulted with GPT4 * 4):<br>
You are a sophisticated tool developed for scrutinizing Twitter messages. Your primary responsibility is to identify and correct spelling and grammar mistakes within these messages. Although Twitter is known for its informal language and slang, your objective includes distinguishing between acceptable informal expressions and actual spelling or grammatical inaccuracies. This means contractions should be used correctly (e.g., "I'm" instead of "im"), and verbs should be in their proper form (e.g., "makin" instead of "makin"), even in the midst of slang or informal contexts. Your analysis should bypass the slang itself unless it directly leads to a spelling or grammatical mistake. Upon reviewing a message, respond with "yes" if it adheres to standard spelling and grammar rules, considering the nuances of Twitter's informal communication. If any errors are present, reply with "no" and concisely specify each error found, emphasizing solely the spelling and grammatical issues without critiquing the informal or slang usage, unless it constitutes an error in spelling or grammar.<br>
- Selected model: GPT3-3.5-Turbo:
- Pros:
  - Fordable, classify 10K messages ~1.5 with this long prompt...
  - Quite accurate in most cases and know informal English and social media tweets.
- Cons:
  - GPT-4.0-Turbo is much better but cost x10.
  - Limits on daily and hourly tokens.
- Ho to classify?
- It's a long task so we send 10 messages and save response (proved to be right, connection not always stable).
- API: Temperature and top_p not workig on the API but result are generally good and we can deal with errors.
- Creating "raw_train_tweets_classified_open_ai.csv"

## Pre-Process for train (look at /classification_by_open_ai/llm_clean_up_and_order.ipynb):
- First look:<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/2b675a3f-f9fb-49dc-a9e4-c69648c4a0c7)

- ones = 24K
- zeros = 6.5K
- fixes to OpenAI result:
  - "yes" -> 1:<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/dfdb3574-1a62-4b3a-ac75-32502f2560e1)

  - "no errors found" -> 1:<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/f1f95841-04fc-411e-9643-1472166a543d)

  - "no errors" -> 1<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/aa93a43f-bae9-48e4-8458-5e44f1d1a7ee)

  - also "no, there are no errors" -> 1
    
- Now the time to look on the DS (~30K):<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/928720c9-298f-43a8-bcef-4ce3b57158d8)
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/3bf45b80-1620-4ccf-bec8-939e25018ecc)

- saving to "clean_train_tweets_classified_open_ai.csv" for further work. 

## Train  (look at /classification_by_open_ai/distilbert_x_model.ipynb):
- Model is DistilBERT - small 66M parameters that is recommended everywhere to this task and can allow multiple train in low budget.
- In the future bigger models shoudl be tested.
- Framework is PyTorch on Hugging Face for simplicity. 
- First look the text length we can see a little bias between ones and zeros in term of length:<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/4e1cf860-c4e5-4be6-8282-30bf6ba72e92)

- Splitting to train and test.
- For now validation is not splitted due to issues with HF infrastructure.
- Another look on the test train:<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/20467fcb-a569-4bc1-88f7-e0af7c848f9f)
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/cd459514-567e-4366-b105-6cc668f4fb75)

- Tokenizing and preparing data loader.
- Pay attention max_lenght chosen to 350 tokens since our tweets are 280 Words top (English).
- Model = DistilBertForSequenceClassification
- training_args -> default laeaning rate, batch = 32 (about 11GB of GPU memory)
- Train sample of 1K just to see it's working and predict on 1 -> all ok.
- Try bigger train and result are not good so deciding on "Class Weight" (in latest HF version you need to do it by override).
- CustomTrainer - specially to overwrite compute_loose for class weights.
- CustomCallback - Save the models during the epochs.
- Issues: couldn't set validation and on epoch there is no train loss data, managed to bypass with wandb but had to track all losses.
-  Train view of wandb:<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/b6a7feb3-be75-49c2-97ae-a5e6130fcc3c)

- Result for class weights model:
- Epoch 6:<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/82a4f834-f6f6-463e-9911-68b56a4af328)
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/3e48ab4c-47f5-4b33-97ca-d703d46959d2)

- Look on the real result show our data is still low:<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/17706122-0070-442f-88a1-049352bbf384)

- Epoch 2 (best on the minority class):<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/704fee29-7834-450f-a7d9-6e090f1ee9ce)
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/157f4a9f-8335-420c-8d0b-5525f435074c)

- Trying with even_dataset (remove ones so zeros=ones):<br>
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/7dd90302-d2ec-43c3-ae20-f94e8c4f1c53)
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/df120b58-71d6-4a53-9b8c-66c095988717)

- Time to decide: for now the balanced result (ones=zeros) is not the best but with higher recall and will be too strict on fix (we miss less), going for it.
- We must have more data, specially zeros. 

## Buiding Predict (see tweets_server.py and tweet_predict/tweets_predictor.py):
- Prediction server, using the chosen model and predict result.
- Future to predict on many request at ones. 
- Use GPU, future improvement is to use ONNX for up to *5 faster (need to know the hardware and the profile).
- Rest Server based on Fast AI:
  - POST
  - /correct_tweet
  - data in form.
  - Response: Json with 0 for wrong and 1 for correct (Strings)
  - See image at the top for usage in postman.

## Demo UI:
- Simple demo ui in js.
- Takes messages from test (pre-loaded csv) and show the OpenAI response to the text.
- Allow to check any tweet for direct impression.
- See image at the page top. 

## License:
- The work here is for research purpose.
- All Original code done by the author is free to use in any way. 
- Data or / and third party used here belong to their creators and it is user responsibility to comply with their licenses. 
- X dataset belong to X (Tweeter), it is user responsibility to comply with their licenses. 
