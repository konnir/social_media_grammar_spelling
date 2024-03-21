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


## Content (short summary:
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
- DS creation:
  - Spell check
  - Grammer check
  - Clasify and prepare all data
- Classifier Creation:
  - POC check on few classifiers with results
  - Train test split and check eqality
  - Train classifier
  - Try to different aproch (if time allow)
- Web service:
  - Create Rest server to receive messages and return classificatons
  - Expend to mutiple messaes
- Demo UI:
  - Create a siple ui to type the message and present correctness
  - Expand ui to show the erros (if time allow)     

## Licence:
- The work here is for reasearch purpose.
- All Original code done by the author is free to us in any way. 
- Data or / and third party used here belong to their creators and it's user responsiblity to comply with their licences. 
- X dataset belong to X (Tweeter), it's user responsiblity to comply with their licences. 
