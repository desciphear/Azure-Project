# Required Libraries
import streamlit as st
from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speech_rec
from playsound import playsound
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


# Loading Endpoint, Keys and Region for resources from configuration file
global speech_config
global command
load_dotenv()
ai_endpoint=os.getenv('AI_SERVICE_ENDPOINT')
ai_txt_key=os.getenv('AI_SERVICE_KEY')
ai_key = os.getenv('SPEECH_KEY')
ai_region = os.getenv('SPEECH_REGION')
speech_config = speech_rec.SpeechConfig(ai_key, ai_region)

st.title("Speech Sentiment Analyzer")
st.write('Ready to use speech service in:', speech_config.region)

#Text to Speech convertor
def TranscribeInput():
   
    
    
    command = ''
    #Creating AudioConfig to Take input from microphone
    audio_config = speech_rec.AudioConfig(use_default_microphone=True)

    #Calling Speech Recognizer
    speech_recognizer = speech_rec.SpeechRecognizer(speech_config, audio_config)
    st.write('Speak Now...')

    #Taking Audio Input and converting into text
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_rec.ResultReason.RecognizedSpeech:
          command = speech.text
          st.write(command)
     
    else:
          command = ''
          st.write(speech.reason)
          
          
    
    #Returning Output as Sring stored in command variable
    return command


#Function to Analyze Sntiment of spoken sentence
def analyzer():
    global output
    
    #Taking Text Input from TranscribeInput function
    command = TranscribeInput()
    
    #error saver
    

    print(command)
    #Configuring Credentials and Creating Client 
    credential = AzureKeyCredential(ai_txt_key)
    ai_client = TextAnalyticsClient(endpoint=ai_endpoint,credential=credential)
    
    #Analyzing Sentiment From The Text
    if command != '':
        
        sentimentAnalysis = ai_client.analyze_sentiment(documents=[command])[0]

        #Taking output as String
        txt = sentimentAnalysis.sentiment
        score = sentimentAnalysis.confidence_scores
         
        #Printing Final Output
        output = 'Sentiment of Given Speech is ' + txt +" with confidence scores: \n"+f"\n Positive: {score.positive:.2f} \n Negative: {score.negative:.2f} \n Neutral: {score.neutral:.2f}"
    else:
        
        output = 'No Input Provided by the user'

    return output


#Function To give Audio Output
def Speak():

    #Choosing Voice for output and Creating Speech Synthesizer for spoken Output
    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
    speech_synthesizer = speech_rec.SpeechSynthesizer(speech_config)
    
    #Calling Function To Generate Output Audio
    speak = speech_synthesizer.speak_text_async(output).get()
    st.write(output)
    if speak.reason != speech_rec.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
    else:
        print(speak)




User_input = st.button('Click To Use Application')
if User_input == True:
     
    command = analyzer()
    if command.lower() != '':
                     
                Speak()
    elif command == 'No Input Provided by the user':
        st.write('No Speech Given Please Speak after Speak Now Appear On Screen')



