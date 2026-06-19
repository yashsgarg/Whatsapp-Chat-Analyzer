import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_users, df):
    if selected_users != "overall":
       df = df[df['user'] == selected_users]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for messages in df['message']:
        words.extend(messages.split())

    # fetch the number of media messages
    num_media_msg = df[df['message'] == "<Media omitted>\n"].shape[0]

    # fetch the links shared
    links = []
    for messages in df['message']:
        links.extend(extract.find_urls(messages))

    return num_messages, len(words),  num_media_msg, len(links)

# fetch most busy users
def most_busy_users(df):
    x = df['user'].value_counts().head(6)
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'}
    )
    return x, df

def create_wordcloud(selected_users, df):
    if selected_users != "overall":
       df = df[df['user'] == selected_users]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc =wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_users, df):
    # f = open("stop_hinglish.txt","r")
    # stop_words = f.read()

    if selected_users != "overall":
      df = df[df['user'] == selected_users]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        # for word in message.lower().split():
        #     if word not in stop_words:
          words.extend(message.split())

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_analyse(selected_users, df):
      if selected_users != "overall":
         df = df[df['user'] == selected_users]
     #
     # emojis = []
     # for message in df['message']:
     #     emojis.extend([c for c in message if c in emoji.is_emoji(c)])
     #
     # emoji_df =pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
     # return emoji_df

      emojis = []
      for message in df['message']:
          if isinstance(message, str):  # Ensure the message is a string
             emojis.extend([c for c in message if emoji.is_emoji(c)])

      # Count the emojis and create a DataFrame
      emoji_counts = Counter(emojis)
      emoji_df = pd.DataFrame(emoji_counts.most_common(), columns=['emoji', 'count'])
      return emoji_df

def monthly_timeline(selected_users, df):
    if selected_users != "overall":
        df = df[df['user'] == selected_users]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

def daily_timeline(selected_users, df):
    if selected_users != "overall":
        df = df[df['user'] == selected_users]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_users, df):
    if selected_users != "overall":
        df = df[df['user'] == selected_users]

    return df['day_name'].value_counts()

def month_activity_map(selected_users, df):
    if selected_users != "overall":
        df = df[df['user'] == selected_users]

    return df['month'].value_counts()


# def activity_heatmap(selected_users, df):
#     if selected_users != "overall":
#         df = df[df['user'] == selected_users]
#
#     # Full list of days and periods
#     days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     periods = [f"{h}-{(h + 1) % 24}" for h in range(24)]  # 0-1, 1-2, ..., 23-0
#
# # Ensure user_heatmap has all days and periods
#     user_heatmap = df.pivot_table(
#           index='day_name', columns='period', values='message', aggfunc='count'
#     ).reindex(index=days, columns=periods, fill_value=0)
#
#     return user_heatmap


