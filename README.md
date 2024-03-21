<p align="left">
<!--   <img src="https://github.com/konnir/x_grammar_spelling/assets/119952960/f415aef0-dd6b-4223-81be-9ce5d677b53a" alt="anyword_logo" width="150" style="margin-left: 50px;"/> -->
  <img src="https://github.com/konnir/x_grammar_spelling/assets/119952960/aaae3161-5d93-4e82-87bf-1ac468f1817a" alt="Nir_Kon_Logo_inverted (1)" width="100"/>
</p>

# x_grammar_spelling
Check grammar and spelling on X messages with concideration on use of slang, shortcuts and hashtags.

Welcome to the Tweet Checker!
It has trained on social media style messages and will support informal english, and all tweeter special symbols. 

# First, what is can it do (demo taste)?

![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/43631bb7-f70f-4742-8d18-74da09facc90)

# Scond, How can I work with it?

![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/01227d23-e5dd-4006-b541-3502d995fb8c)


## Content (short summary):
- Collection and pre-processing of X messages:
  - Tried to look on X API to scrape tweets from there and got cold sholder from the new Management, only 1500 can be scraped for day with frightning licence. 
  - Collected many tweets data sets from all over the internet (turn out that the licence on X change and many were deleted).
  - The chosen data set is a hugee (4.5M) messages:
    - US tweets on different subjects created for geo-location research.
    - collected in 2009-2010 (more than enough for POC use, old informal english and terms.
    - From aboove 110K different users.  
  - Basic clean - empty, duplicated, URL, special charactes
    - Fairly clean DS - main work was to remove just one @ annotation and to decode html.  
  - Handle X special -
    - Tweeter has many signs and types like Hashtags and DM messages, decidet to keep as is.
    - Emoji, many in my DS and also decided to keep them as is. 
  - Handle slang and shortcuts:
    - After reaserching a little wi decided to keep all slang as is.
    - Same for shortcuts and other, seems like the LLM classifiers later can deal with them.
  - General:
    - DS is 140 character in the majority (see below for box plots), I decided to clean all above 280 charactes and below 3 out of the DS and POC. 
- DS creation (with OpenAI GPT.3.5-Turbo):
  - Looking to create a ground of truth I choose the OpenAI due to the API availability.
  - The "playground" OpenAI offer helped me to form the right promt for my tweets and evalute the quality. 
  - pros:
    - Proven industry statndard.
    - Availability.
    - low price.
    - Fast.
  - Cons:
    - Limit of 10k messages a day (I'm very low on the tears, company get much more)
    - Not as good as gpt-4.0-trubo.
    - API not perfect, you can't realy set temprature=0 and top_p=0. 
- Classifier Creation:
  - DistilBert was chosen due to the eash of train and proven record on text simple calssifications tasks.
  - Pros:
    - 65M parameters but get the work done for simple tasks.
    - Light, ~200MB with 65M parameters.
    - Fast on GPU and CPU if needed for inference.
    - Short train time compared to Bert / Roberta / GPT-2 that were candidate for this.
  - Cons:
    - I took Hugging Face version with PyTorch, it was proably not the best: change the class weights and everyhting didn't work from there. 
- Web service:
  - Create Rest server to receive messages and return classificatons thorough predictor. 
  - Expends to mutiple messages for later cpu utilization. 
- Demo UI:
  - For visualization and deeper understanding of the data and the problem domain. 
  - Create a siple ui to type the message and present if OK or FIX. 
  - Expand ui to show the OpenAi answer on the message (from test).
 
## Data Exploration (see /ds_exploration/5_M_ds_set_up.ipynb):
- 3,609,675 tweets.
- First step, take the first 5 lines to see how to work here:
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/ecad9926-2213-4ae7-936f-886b41a04201)

- Let's go for df:
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/f0ea291e-257e-4c6e-a456-c65ca9e0acb0)

- 80,807 nulls were droped.
- 119,065 duplicates were droped (left one).
- 939 messages shorter than 4 characters were doped (our task is context).
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/b015d5c8-1532-4e9f-b5b3-477188d8bdd9)

- longest message is: 31,135 characters.
- Looking on long messages:
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/9667a0d0-cceb-4fcd-9433-6611bdefb713)

- Decided to keep the limit of tweeter (280) and droped all longer than this.
- Looking on messages lenth:
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/5e80b75a-9bbe-48ee-9113-2caf7b0b1327)

- most frequent length is 140 (box plot later)
- Looking on Tweeter specials: RT (22K), DM(13K), "t.com" - no need to remove them.
- Decide to convert all text from html to plain text (came out in the icons). 
- Looking into icons:
![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/b4a901da-e31b-4fa2-b44a-6a3ddc39d071)

- Looking on icons and symboles, also no need to remove:
 ![image](https://github.com/konnir/x_grammar_spelling/assets/119952960/fc8b5919-5bcb-4d1c-a3a0-58dff8aca0f3)

- save to clean_train_tweets.csv for later work. 





## Licence:
- The work here is for reasearch purpose.
- All Original code done by the author is free to us in any way. 
- Data or / and third party used here belong to their creators and it's user responsiblity to comply with their licences. 
- X dataset belong to X (Tweeter), it's user responsiblity to comply with their licences. 
