import pyttsx3 

engine = pyttsx3.init()

var = "820', 'Double Bottom', 'Stop Run', China"
engine.setProperty('rate', 300)


voices = engine.getProperty('voices')
print(voices[0])
for voice in voices:
    print(voice)
    engine.setProperty('voice', voice.id)
    engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()