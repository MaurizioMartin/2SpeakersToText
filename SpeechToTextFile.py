# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 09:23:13 2018

@author: macl3
"""
import io
import os
import csv
#from google.cloud import speech
from google.cloud.speech import enums
from google.cloud import speech_v1p1beta1 as speech
#import speech_recognition as sr
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/macl3/.spyder-py3/TFG/SpeechRecognition/TFGMaurizioMartin-69a88799a254.json"
print('Credentials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))

client = speech.SpeechClient()
ID_title = 1
file_name= 'resources/psanchez60.wav'
with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()
    audio = speech.types.RecognitionAudio(content=content)

config = speech.types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='es-ES',
        audio_channel_count=2,
        enable_separate_recognition_per_channel=True,
        enable_speaker_diarization=True,
        diarization_speaker_count=2)


print('Waiting for operation to complete...')
response = client.recognize(config, audio)

for i, result in enumerate(response.results):
    alternative = result.alternatives[0]
    print('-' * 20)
    print('First alternative of result {}'.format(i))
    print(u'Transcript: {}'.format(alternative.transcript))
    print(u'Channel Tag: {}'.format(result.channel_tag))

# The transcript within each result is separate and sequential per result.
# However, the words list within an alternative includes all the words
# from all the results thus far. Thus, to get all the words with speaker
# tags, you only have to take the words list from the last result:
result = response.results[-1]

words_info = result.alternatives[0].words
speaker1=[]
speaker2=[]
stringspeaker1=''
stringspeaker2=''
x= None
# Printing out the output:
n=1
for word_info in words_info:
    
    print("word: '{}', speaker_tag: {}".format(word_info.word,
                                               word_info.speaker_tag))
      
    if word_info.speaker_tag is 1:
       if(x == False):
           speaker2.append(str(n)+"|"+stringspeaker2)
           n=n+1
       stringspeaker1 = stringspeaker1 + word_info.word + " "
       stringspeaker2 = ""
       x = True
    else:
        if(x == True):
            speaker1.append(str(n)+"|"+stringspeaker1)
            n=n+1
        stringspeaker2 = stringspeaker2 + word_info.word + " "
        stringspeaker1 = ""
        x = False
if(x):
    speaker1.append(str(n)+"|"+stringspeaker1)
else:
    speaker2.append(str(n)+"|"+stringspeaker2)
    
  
print(speaker1)
print(speaker2)
   

""" Empezar a escribir en csv 


    conversation_lines
ID_line
ID_title
Title
RoleCharacter
Line

"""


for speaker1spl in speaker1:
    ID_line = speaker1spl.split('|')[0]
    Line = speaker1spl.split('|')[1]
    Role = 1
    conversation_lines = [ID_line,ID_title,file_name.split('/')[1],Role,Line]
    myFile = open('conversation_lines.csv', 'a', newline='')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerow(conversation_lines)
for speaker2spl in speaker2:
    ID_line = speaker2spl.split('|')[0]
    Line = speaker2spl.split('|')[1]
    Role = 2
    conversation_lines = [ID_line,ID_title,file_name,Role,Line]
    myFile = open('conversation_lines.csv', 'a', newline='')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerow(conversation_lines)
print("Conversation_title_metadata complete")