This Python program utilizes Azure Cognitive Services to analyze the sentiment of spoken words.

Features
    Transcribes user input using Speech-to-Text functionality.
    Analyzes the sentiment of the transcribed text using Text Analytics.
    Provides spoken feedback on the sentiment analysis using Text-to-Speech.

Requirements
    Python 3.6+
    Azure Cognitive Services account with access to:
        Speech Services
        Text Analytics

Installation
    Install required libraries:
    Bash
    pip install python-dotenv azure-cognitiveservices-speech playsound azure-ai-textanalytics  


Add your Azure Cognitive Services keys and endpoint to .env File:
    AI_SERVICE_ENDPOINT=<Your Text Analytics endpoint URL>
    AI_SERVICE_KEY=<Your Text Analytics subscription key>
    SPEECH_KEY=<Your Speech Services subscription key>
    SPEECH_REGION=<Your Speech Services region (e.g., westus)>

Usage
    Run the program:
        Bash
        python main.py


Application
    There is also a simple application provided in file which requires Streamlit to be installed
     Bash
      pip install streamlit


Speak a sentence when prompted by "Speak Now...".
    The program will analyze the sentiment of your speech and provide spoken feedback (e.g., "Sentiment of Given Speech is positive").
    Enter "quit" to stop the program, or press any key to continue analyzing new sentences.

Notes
    This program utilizes pre-defined Azure Cognitive Services resources. Make sure to replace the placeholders in the .env file with your own credentials and endpoint URL.
    The program uses a loop to continuously prompt the user for input. Enter "quit" to terminate the loop and exit the program.