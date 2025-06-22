AFRO EQUALITY



Empowering People of African Descent: Hate Speech, Violence and Racism- Training on Digital Skills and Civic Participation

I conducted a comprehensive sentiment analysis of online press and social media content across Greece, Italy, and Spain. The initial phase involved scraping online press articles to extract their text and titles, complemented by acquiring tweets labeled for hate speech from the TweetEval dataset available on Hugging Face. For sentiment evaluation, we employed VADER (Valence Aware Dictionary and sEntiment Reasoner), a lexicon and rule-based tool that assigns a compound sentiment score alongside specific scores for positive and negative sentiments. To enhance our analysis, we integrated API calls to ChatGPT 4.0-mini, utilizing a meticulously crafted prompt refined through extensive experimentation. This approach enabled us to classify texts for the presence of racial hate speech targeting Black individuals and to assess whether the author's intent was racially motivated. Our goal was to construct a dataset encompassing columns for text, title, newspaper, sentiment, hate speech, hate speech explanation, author's motivation, and an explanation of the author's motivation. Leveraging large language models like ChatGPT facilitated the generation of detailed explanations for hate speech and the author's intent, thereby enriching the dataset with nuanced insights.


Codes for scraping online articles:

For Greek articles (athinorama, proto_thema, Kathimerini):
	- greek_web_scraping_athinorama.py
	- greek_web_scraping_proto_thema.py
	- greek_web_scraping_kathimerini.py


For Spanish articles (el diario, el pais):
	- spanish_web_scraping_el_diario.py
	- spanish_web_scraping_el_pais.py

For Italian articles ():
	-


For Tweets:

- tweet_dataset_download_hate_speech.py

Download and save the text of tweets labeled for hate speech from the TweetEval dataset. The TweetEval dataset is available on Hugging Face.	

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Sentiment Analysis code:

- Vader_Sentiment.py

VADER (Valence Aware Dictionary and sEntiment Reasoner): uses a lexicon and rule-based approach to evaluate the sentiment of text data. 
It's particularly well-suited for analyzing social media, news articles, and other forms of online text.

KEY FEATURES:
    Pre-Trained Sentiment Lexicon:
    VADER relies on a lexicon (a dictionary) of words that have been scored for their sentiment intensity (Positive words like "great," "awesome," or "fantastic" have high positive scores).
    Handles Sentiment Modifiers:
    VADER accounts for intensifiers, negations, and other modifiers that influence sentiment (Intensifiers: Words like "very" or "extremely" increase sentiment intensity). 
    Works Well for Short Text
    Emoticons, Slang, and Punctuation
    VADER recognizes emojis, internet slang, and punctuation to capture a better sentiment in informal text ("I love it!! 😊" will have a stronger positive sentiment due to the exclamation points and smiley face).
    Scores for Sentiment Polarity:
    VADER provides a compound sentiment score and scores for each sentiment category:
        Positive Score: Measures the intensity of positive sentiment.
        Negative Score: Measures the intensity of negative sentiment.
        Neutral Score: Measures the intensity of neutral sentiment.
        Compound Score: A normalized score between -1 (most negative) and +1 (most positive). It reflects the overall sentiment of the text.

================================================================================================================================================================================================================================
================================================================================================================================================================================================================================

ChatGPT-4o Mini:
We integrated API calls to ChatGPT 4.0-mini, utilizing a meticulously crafted prompt refined through extensive experimentation.


Prompt for classifying online articles:

 	You are a political scientist with profound expertise in hate speech and discrimination. You are given the following newspaper article. Your task is to determine:

        	1. Whether the article contains racial hate speech against People of African Descent.
        	2. Whether the motivation of the author of the article is racist.

        Please provide your answers in the following CSV format:
        Yes or No, Explanation of the first answer without any punctuation, Yes or No, Explanation of the second answer without any punctuation

        Ensure that your response strictly follows this format, using commas to separate each element, and omitting all punctuation marks in the explanations.


-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Prompt for classifying tweets:

        ## Goal:
        You are a political scientist with expertise in hate speech and discrimination. Your task is to analyze the following tweet and determine:

        1. Whether the tweet contains racial hate speech against People of African Descent (Black people).
        2. Whether the author's motivation for writing the tweet is hateful or racist.

        ## Return Format:
        Your response must strictly follow this format:
        Yes or No, Explanation of the first answer without any punctuation, Yes or No, Explanation of the second answer without any punctuation

        - Separate each part with a comma.
        - The explanations should not contain any punctuation (periods, commas, colons, etc.).
        - Provide concise but clear reasoning.

        ## Warnings:
        - Do not include extra text outside of the required format.
        - If the tweet is neutral or unclear, classify it as "No" with a clear justification.
        - Avoid assumptions beyond what is explicitly stated in the tweet.

================================================================================================================================================================================================================================
================================================================================================================================================================================================================================

Final Outcome:





