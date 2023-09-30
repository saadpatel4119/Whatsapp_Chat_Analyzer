# Whatsapp Chat Analyzer

### Introduction
In this project, I have proposed a WhatsApp Chat Analyzer. WhatsApp chats consist of various types of 
communications within groups and personal chats, covering a wide range of topics. These chats contain 
valuable data that can be leveraged for technologies like machine learning. The quality of machine learning 
models heavily depends on the quality and richness of the data provided for training. This application aims 
to offer a comprehensive analysis of WhatsApp chat data. One of the key advantages of this application is 
its simplicity in implementation, relying on widely-used Python libraries such as seaborn, pandas, numpy, 
streamlit, matplotlib and nltk. These libraries are commonly employed for creating data frames, generating 
various types of graphs and visualizations, finding the sentiment of the chats and translating the chats into 
desired language. The results of the analysis are presented on the web, accessible through a Heroku link. 
This means that the application can be run on a wide range of devices that support web browsers, making 
it accessible and user-friendly for a broad audience.

### Python Libraries Used
- pandas==1.3.3
- numpy==1.21.2
- seaborn
- plotly
- matplotlib
- streamlit
- urlextract
- wordcloud
- regex
- emoji==1.7.0
- nltk
- deep-translator

### Advantages of the Proposed System 
- Shows Top Statistics of the chats such as Total Messages, Total Words, Docs Shared, Links Shared, Videos Shared, Images Shared, Audio Shared, Contacts Shared
- Attractive visualizations and useful data frames for Monthly Timeline, Daily Timeline, Most busy day, Most busy month, Weekly Activity Map, Most Busy Users, Word cloud chart for most commonly used words, Pie chart representation for 10 widely used emoji.
- Sentiment Analysis whether the chat is positive, negative or neutral based on polarity score
- Translation of the chats into desired language

### RESULTS AND DISCUSSION
This project is created using python programming language and deployed on Heroku web. 
Working of project: 
- User go to sidebar and click on browse file. 
- Select WhatsApp chat text file and import it for analysis. 
- User have choice for overall analysis or specific user analysis from whole group. 
- After selecting user, User click on “Select a language” and can select a desired language from a dropdown 
list.
- After Language selection, User can click on show analysis button to show results of the imported text file

##### For more details, do check out the Project Report provided in the repository.