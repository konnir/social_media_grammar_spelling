<p align="left">
  <img src="https://github.com/konnir/x_grammar_spelling/assets/119952960/f415aef0-dd6b-4223-81be-9ce5d677b53a" alt="anyword_logo" width="150" style="margin-left: 50px;"/>
  <img src="https://github.com/konnir/x_grammar_spelling/assets/119952960/aaae3161-5d93-4e82-87bf-1ac468f1817a" alt="Nir_Kon_Logo_inverted (1)" width="100"/>
</p>

# x_grammar_spelling
Check grammar and spelling on X messages with concideration on use of slang, shortcuts and hashtags.

## Content:
- Collection and pre-processing of X messages:
  - Collect DS - download and validate X messages to be used in DS 
  - Basic clean - empty, duplicated, URL, special charactes 
  - Handle X special - hashtags,
  - Handle slang and shortcuts - mark sleng to be handled seperatly from the main content
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
