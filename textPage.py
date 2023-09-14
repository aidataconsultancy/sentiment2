import streamlit as st
import streamlit.components.v1 as components
from textblob import TextBlob
from PIL import Image
import text2emotion as te
import plotly.graph_objects as go

def plotPie(labels, values):
    fig = go.Figure(
        go.Pie(
        labels = labels,
        values = values,
        hoverinfo = "label+percent",
        textinfo = "value"
    ))
    st.plotly_chart(fig)

    
def getPolarity(userText):
    tb = TextBlob(userText)
    polarity = round(tb.polarity, 2)
    subjectivity = round(tb.subjectivity, 2)
    if polarity>0:
        return polarity, subjectivity, "Positive"
    elif polarity==0:
        return polarity, subjectivity, "Neutral"
    else:
        return polarity, subjectivity, "Negative"

def getSentiments(userText, type):
    if(type == 'Positive/Negative/Neutral - TextBlob'):
        polarity, subjectivity, status = getPolarity(userText)
        if(status=="Positive"):
            image = Image.open('./images/positive.PNG')
        elif(status == "Negative"):
            image = Image.open('./images/negative.PNG')
        else:
            image = Image.open('./images/neutral.PNG')
        col1, col2, col3 = st.columns(3)
        col1.metric("Polarity", polarity, None)
        col2.metric("Subjectivity", subjectivity, None)
        col3.metric("Result", status, None)
        st.image(image, caption=status)
    elif(type == 'Happy/Sad/Angry/Fear/Surprise - text2emotion'):
        emotion = dict(te.get_emotion(userText))
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Happy 😊", emotion['Happy'], None)
        col2.metric("Sad 😔", emotion['Sad'], None)
        col3.metric("Angry 😠", emotion['Angry'], None)
        col4.metric("Fear 😨", emotion['Fear'], None)
        col5.metric("Surprise 😲", emotion['Surprise'], None)
        plotPie(list(emotion.keys()), list(emotion.values()))
        

def renderPage():
    st.title("Sentiment Analysis 😁😐☹️😖😲😱😡")
    components.html("""<hr style="height:3px;border:none;color:#333;background-color:#333; margin-bottom: 10px" /> """)
    # st.markdown("### Sentiment Analysis of User-Input Text")
    st.subheader("Sentiment Analysis of User-Input Text")
    st.text("")
    st.markdown("With this tool, you can easily analyze the sentiment and emotions associated with the text you provide. Follow these simple steps to get detailed analysis results:")
    st.markdown("### Text Entry:")
    st.markdown("It can be a sentence, a paragraph, or even an entire article.")
    st.markdown("### Type of Analysis:")
    st.markdown("Instructions: Choose from the available analysis options. Each option provides a different perspective on the sentiments and emotions of the text.")
    st.markdown("- Positive/Negative/Neutral - TextBlob: This analysis will classify the text into one of these three categories, indicating whether the overall tone is positive, negative, or neutral.")
    st.markdown("- Happy/Sad/Angry/Fear/Surprise - text2emotion: This analysis delves deeper into the specific emotions present in the text. It will identify if the content reflects emotions of happiness, sadness, anger, fear, or surprise.")
    st.markdown("### Get Results:")
    st.markdown("Once you have entered the text and selected the type of analysis you want, click on the corresponding button to process the information.")
    st.markdown("Within seconds, the tool will display the results of the analysis based on the provided text.")

    st.text("")
    userText = st.text_input('In the field labeled "Input text HERE", enter the text you wish to analyze. ', placeholder='Input text HERE')
    st.text("")
    type = st.selectbox(
     'Choose from the available analysis options. Each option provides a different perspective on the sentiments and emotions of the text.',
     ('Positive/Negative/Neutral - TextBlob', 'Happy/Sad/Angry/Fear/Surprise - text2emotion'))
    st.text("")
    if st.button('Predict'):
        if(userText!="" and type!=None):
            st.text("")
            st.components.v1.html("""
                                <h3 style="color: #0284c7; font-family: Source Sans Pro, sans-serif; font-size: 28px; margin-bottom: 10px; margin-top: 50px;">Result</h3>
                                """, height=100)
            getSentiments(userText, type)
