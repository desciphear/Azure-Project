# Required Libraries
from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speech_rec
from playsound import playsound
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


# Loading Endpoint, Keys and Region for resources from configuration file
global speech_config
load_dotenv()
ai_endpoint=os.getenv('AI_SERVICE_ENDPOINT')
ai_txt_key=os.getenv('AI_SERVICE_KEY')
ai_key = os.getenv('SPEECH_KEY')
ai_region = os.getenv('SPEECH_REGION')
speech_config = speech_rec.SpeechConfig(ai_key, ai_region)


#Text to Speech convertor
def TranscribeInput():
   
    global command
    
    #Creating AudioConfig to Take input from microphone
    audio_config = speech_rec.AudioConfig(use_default_microphone=True)

    #Calling Speech Recognizer
    speech_recognizer = speech_rec.SpeechRecognizer(speech_config, audio_config)
    print('Speak Now...')

    #Taking Audio Input and converting into text
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_rec.ResultReason.RecognizedSpeech:
          command = speech.text
          print(command)
     
    else:
          print(speech.reason)
          cancellation = speech.cancellation_details
          print(cancellation.reason)
          print(cancellation.error_details)
    
    #Returning Output as Sring stored in command variable
    return command


#Function to Analyze Sntiment of spoken sentence
def analyzer():
    global output

    #Taking Text Input from TranscribeInput function
    command = TranscribeInput()

    #Configuring Credentials and Creating Client 
    credential = AzureKeyCredential(ai_txt_key)
    ai_client = TextAnalyticsClient(endpoint=ai_endpoint,credential=credential)
    
    #Analyzing Sentiment From The Text
    sentimentAnalysis = ai_client.analyze_sentiment(documents=[command])[0]

    #Taking output as String
    txt = sentimentAnalysis.sentiment

    #Printing Final Output
    output = 'Sentiment of Given Speech is ' + txt
    return output


#Function To give Audio Output
def Speak():

    #Choosing Voice for output and Creating Speech Synthesizer for spoken Output
    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
    speech_synthesizer = speech_rec.SpeechSynthesizer(speech_config)
    
    #Calling Function To Generate Output Audio
    speak = speech_synthesizer.speak_text_async(output).get()
    if speak.reason != speech_rec.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
    else:
        print(speak)


#Main Function
def main():
    try: 
        
        print('Ready to use speech service in:', speech_config.region)
        
        #Asking User For Input
        while True:
         
         User_input = input('\nEnter Quit to Stop and Press any key to continue: ')
         

         if User_input.lower() != 'quit':
            command = analyzer()     
            if command.lower() != '':
                Speak()
            else:
                print('\nSpeak After Speak Now Is Printed')
         else:
             print('User Quit The Program') 
             break

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
