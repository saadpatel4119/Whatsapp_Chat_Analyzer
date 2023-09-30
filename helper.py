from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import re
import regex
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator


extract = URLExtract()
num_document_messages=[]
links = []

def fetch_stats(selected_user,df):
    global num_document_messages
    global links

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    #fetch the number of video messages 
    num_video_messages = df[df['message'] == '\u200evideo omitted'].shape[0]

    #fetch the number of image messages 
    num_image_messages = df[df['message'] == '\u200eimage omitted'].shape[0]

    #fetch the number of audio messages 
    num_audio_messages = df[df['message'] == '\u200eaudio omitted'].shape[0]

    #fetch the number of contact messages 
    num_contact_messages = df[df['message'] == '\u200eContact card omitted'].shape[0]

    #fetch the number of document messages 
    document_pattern = r'.*\u200edocument omitted'
    # Use regex to find strings containing the pattern
    for s in df['message']:
        if re.search(document_pattern, s):
            num_document_messages.append(s)

    #fetch the number of URL messages 
    extractor = URLExtract()
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages,len(words),num_video_messages,num_image_messages,num_audio_messages,num_contact_messages,len(num_document_messages),len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

# Read Hinglish stopwords from a file
with open('stop_hinglish.txt', 'r', encoding='utf-8') as file:
    hinglish_stop_words = set(word.strip() for word in file)

def process_text(text):
    # Step 1: Convert to lowercase
    text = text.lower()
    
    # Step 2: Remove non-alphanumeric characters and emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F700-\U0001F77F"  # alchemical symbols
                               u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                               u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                               u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                               u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                               u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                               u"\U0001FB00-\U0001FBFF"  # Symbols for Legacy Computing"
                               "]+", flags=re.UNICODE)
    
    text = emoji_pattern.sub('', text)  # Remove emojis using regex

    # Step 3: Remove non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Step 4: Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words and word not in hinglish_stop_words])
    
    return text

def remove_emojis(text):
    return emoji.demojize(text)

def create_wordcloud(selected_user,df):
    global num_document_messages
    global links

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']

    # List of strings to remove
    strings_to_remove = ['\u200eimage omitted', '\u200evideo omitted', '\u200eaudio omitted','\u200eContact card omitted','\u200eThis message was deleted.']

    # Remove rows containing any of the specified strings
    temp = temp[~temp['message'].isin(strings_to_remove)]
    temp = temp[~temp['message'].isin(links)]
    temp = temp[~temp['message'].isin(num_document_messages)]
    # Apply the emoji removal function to the 'content' column
    temp['message'] = temp['message'].apply(remove_emojis)
    # Apply the processing function to the 'content' column
    temp['message'] = temp['message'].apply(process_text)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']

    # List of strings to remove
    strings_to_remove = ['\u200eimage omitted', '\u200evideo omitted', '\u200eaudio omitted','\u200eContact card omitted','\u200eThis message was deleted.']

    # Remove rows containing any of the specified strings
    temp = temp[~temp['message'].isin(strings_to_remove)]
    temp = temp[~temp['message'].isin(links)]
    temp = temp[~temp['message'].isin(num_document_messages)]
    temp['message'] = temp['message'].apply(remove_emojis)
    temp['message'] = temp['message'].apply(process_text)

    words = []

    for message in temp['message']:
        for word in message.split():
            words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def split_count(text):
    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI['en'] for char in word):
            emoji_list.append(word)
    
    return emoji_list

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []

    for message in df['message']:
        emojis.extend(split_count(message))

    if not emojis:  # Check if the list of emojis is empty
        return pd.DataFrame({'Emoji': [0], 'Count': [0]})

    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counts.items(), columns=['Emoji', 'Count'])
    emoji_df = emoji_df.sort_values(by='Count', ascending=False)

    return emoji_df


def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

def get_sentiment_polarity(message, sentiment_analyzer):
    sentiment_scores = sentiment_analyzer.polarity_scores(message)
    sentiment = sentiment_scores['compound']

    if sentiment >= 0.05:
        return 'Positive',sentiment
    elif sentiment <= -0.05:
        return 'Negative',sentiment
    else:
        return 'Neutral',sentiment
    
def sentiment(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']

    # List of strings to remove
    strings_to_remove = ['\u200eimage omitted', '\u200evideo omitted', '\u200eaudio omitted','\u200eContact card omitted','\u200eThis message was deleted.']

    # Remove rows containing any of the specified strings
    temp = temp[~temp['message'].isin(strings_to_remove)]
    temp = temp[~temp['message'].isin(links)]
    temp = temp[~temp['message'].isin(num_document_messages)]
    temp['message'] = temp['message'].apply(remove_emojis)
    temp['message'] = temp['message'].apply(process_text)
    # Initialize the sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Concatenate all messages into a single text
    all_messages = " ".join(temp['message'])

    # Apply sentiment analysis to the combined "message" column
    sentiment,polarity = get_sentiment_polarity(all_messages, analyzer)
    sentiment_list = [sentiment]
    polarity_list = [polarity]
    sentiment_df = pd.DataFrame({'Sentiment': sentiment_list, 'Polarity': polarity_list})
    return sentiment_df

def translate_chat(selected_language, selected_user, df):
    # Map user-friendly language names to language codes
    language_mapping = {
        'Hindi': 'hi',
        'Marathi': 'mr',
        'French': 'fr',
        'Arabic': 'ar',
        'Urdu': 'ur',
    }
    target_language = language_mapping[selected_language]

    # Fetch the messages for the selected user (if not 'Overall')
    if selected_user != 'Overall':
        df_filtered = df[df['user'] == selected_user]
    else:
        df_filtered = df

    # Remove unwanted messages
    temp_df = df_filtered[df_filtered['user'] != 'group_notification']
    strings_to_remove = ['\u200eimage omitted', '\u200evideo omitted', '\u200eaudio omitted',
                         '\u200eContact card omitted', '\u200eThis message was deleted.']
    temp_df = temp_df[~temp_df['message'].isin(strings_to_remove)]
    temp_df = temp_df[~temp_df['message'].isin(links)]
    temp_df = temp_df[~temp_df['message'].isin(num_document_messages)]

    # Translate each message individually and store them in a new column
    temp_df['translated_message'] = temp_df['message'].apply(
        lambda message: GoogleTranslator(source='auto', target=target_language).translate(message)
    )

    # Create 'translated_chat' by combining user names and translated messages
    translated_chat = ""
    for _, row in temp_df.iterrows():
        user = row['user']
        translated_message = row['translated_message']
        translated_chat += f"{user}:\n{translated_message}\n\n"

    return translated_chat














