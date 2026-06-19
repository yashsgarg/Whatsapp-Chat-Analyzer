import matplotlib.pyplot as plt
import streamlit as st
import preprocessor
import helper
from matplotlib import rcParams
import seaborn as sns


st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)


    # fetch  unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "overall")
    selected_users = st.sidebar.selectbox("Show analysis with respect to", user_list)

    if st.sidebar.button("Show Analysis"):

        # Top Stats
        num_messages, words,  num_media_msg, num_links = helper.fetch_stats(selected_users, df)
        st.title("Top Statistics :")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Total Messages:")
            st.title(num_messages)
        with col2:
            st.subheader("Total Words:")
            st.title(words)
        with col3:
            st.subheader("Total Media Shared:")
            st.title(num_media_msg)
        with col4:
            st.subheader("Total links Shared:")
            st.title(num_links)

        # monthly timeline
        st.header('Monthly timeline-')
        timeline = helper.monthly_timeline(selected_users, df)
        fig, ax = plt.subplots()
        plt.plot(timeline['time'], timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.header('Daily timeline-')
        daily_timeline = helper.daily_timeline(selected_users, df)
        fig, ax = plt.subplots()
        plt.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.header('Activity Map-')
        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Most busy day')
            busy_day = helper.week_activity_map(selected_users, df)
            fig,  ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='pink')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.subheader('Most busy month')
            busy_month = helper.month_activity_map(selected_users, df)
            fig,  ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # heatmap
        # st.header('Weekly Activity Map')
        # user_heatmap = helper.week_activity_map(selected_users, df)
        # fig, ax = plt.subplots()
        # ax = sns.heatmap(user_heatmap)
        # st.pyplot(fig)


        # finding the busiest users in the group
        if selected_users == "overall":
            st.header('Most_Busy_Users-')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
               ax.bar(x.index, x.values, color='grey')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # wordcloud
        st.header('Word Cloud-')
        df_wc = helper.create_wordcloud(selected_users, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_users, df)
        fig, ax = plt.subplots()
        ax.bar(most_common_df[0],most_common_df[1])
        plt.xticks(rotation = 'vertical')
        st.header("Most Common words-")
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_analyse(selected_users, df)
        st.header("Emoji Analyse-")
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            # Set a font that supports emojis
            rcParams['font.family'] = 'Segoe UI Emoji'
            fig, ax = plt.subplots()
            ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct="%0.2f")
            st.pyplot(fig)








