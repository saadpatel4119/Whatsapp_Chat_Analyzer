import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set the title in the top of the sidebar with no gap
st.sidebar.markdown("<h1 style='text-align: left; margin: 0px;'>Whatsapp Chat Analyzer</h1>", unsafe_allow_html=True)

# Move the "-By Saad Patel" to the right
st.sidebar.markdown("<div style='text-align: right;'>-By Saad Patel</div>", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("Choose a file")
# Move language selection to the sidebar
languages = ['Select', 'Hindi', 'Marathi', 'French', 'Arabic','Urdu']
selected_language = st.sidebar.selectbox("Select a Language:", languages)

if uploaded_file is not None:
    file_name = uploaded_file.name
    lines = uploaded_file.readlines()  # Read the uploaded file as a list of lines
    decoded_lines = [line.decode("utf-8") for line in lines]  # Decode each line individually
    df = preprocessor.preprocess(decoded_lines)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        import streamlit as st

        # Fetch the statistics
        (
            num_messages,
            words,
            num_video_messages,
            num_image_messages,
            num_audio_messages,
            num_contact_messages,
            num_document_messages,
            num_links,
        ) = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")
        # Create two rows of four columns each
        col1, col2, col3, col4 = st.columns(4)

        # Display the first four statistics in the first row
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Docs Shared")
            st.title(num_document_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # Create a new row for the remaining statistics
        col5, col6, col7, col8 = st.columns(4)

        with col5:
            st.header("Videos Shared")
            st.title(num_video_messages)

        with col6:
            st.header("Images Shared")
            st.title(num_image_messages)

        with col7:
            st.header("Audio Shared")
            st.title(num_audio_messages)

        with col8:
            st.header("Contacts Shared")
            st.title(num_contact_messages)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='#DA2C43')
            plt.xticks(rotation='vertical',fontsize=20)
            plt.yticks(fontsize=20)
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='#990077')
            plt.xticks(rotation='vertical',fontsize=20)
            plt.yticks(fontsize=20)
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        user_heatmap = user_heatmap.fillna(0)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            # Create a colormap based on the percentage values
            cmap = plt.get_cmap('viridis')  # You can choose any colormap you like
            # Normalize the percentage values to fit within the colormap range
            normalize = plt.Normalize(vmin=new_df['percent'].min(), vmax=new_df['percent'].max())
            # Create the color map for the bars based on percentages
            colors = cmap(normalize(new_df['percent']))
            # Create the bar chart with colored bars
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                bars = ax.bar(x.index, x.values, color=colors)  # Assign the colors to the bars      
                plt.xticks(rotation='vertical', fontsize=20)
                plt.yticks(fontsize=20)               
                # Create a legend based on the percentages
                sm = plt.cm.ScalarMappable(cmap=cmap, norm=normalize)
                sm.set_array([])
                cbar = plt.colorbar(sm)
                cbar.set_label('Percentage', fontsize=20)  # Customize the legend label        
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
            
                
        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
    
        # most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1],color='green')
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)

        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            if not emoji_df.empty and not (emoji_df['Count'] == 0).all() and not (emoji_df['Emoji'] == 0).all():
                plt.rcParams['font.family'] = 'Segoe UI Emoji'
                fig, ax = plt.subplots(figsize=(4,4))
                ax.pie(emoji_df['Count'].head(10), labels=emoji_df['Emoji'].head(10), autopct="%0.2f")
                st.markdown(f"<h3>Top 10 used Emojis</h3>", unsafe_allow_html=True)
                st.pyplot(fig)
            else:
                st.write("No data to display.")  # Display a message if there is no data


        sentiment = helper.sentiment(selected_user,df)
        st.title("Sentiment of the chat")
        st.dataframe(sentiment)


        st.title("Translation of the chats")

        if selected_language != 'Select':
            # Translate the selected language and display the result
            translated_result = helper.translate_chat(selected_language, selected_user, df)
            st.markdown(f"<h3>Chats translated in {selected_language}:</h3>", unsafe_allow_html=True)
            st.write(translated_result)
        else:
            st.warning("Language not selected for Translation")













