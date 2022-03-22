print("starting")
from unicodedata import name
from playsound import playsound

from google.cloud import texttospeech

# Instantiates a client
#client = texttospeech.TextToSpeechClient()
audioFolder = "Audio/"

syntesizedText = "9:00 AM, Double Wide London "

#London: "en-GB" Female
#China:  
languageCode = "en-GB"
voiceName = "en-GB" # A: Higher M | B: 2nd Higher M | C: Lower F | D: Deeper M | E: Higher F | F: High Female | G: Normal F | I: Higher M | J: Higher M | 

###GENDER of VOICE
voiceGender = "FEMALE" #FEMALE/MALE/
if voiceGender == "FEMALE":
   genderString =  texttospeech.VoiceSelectionParams(language_code=languageCode,name= voiceName, ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
elif voiceGender == "MALE":
    genderString =  texttospeech.VoiceSelectionParams(language_code=languageCode, name= voiceName, ssml_gender=texttospeech.SsmlVoiceGender.MALE)
else:
    genderString =  texttospeech.VoiceSelectionParams(language_code=languageCode,name= voiceName, ssml_gender=texttospeech.SsmlVoiceGender.MALE)
###

response =  texttospeech.TextToSpeechClient().synthesize_speech(
    input=texttospeech.SynthesisInput(text=syntesizedText),
    voice = genderString,
    audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
)

# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')

print("Playing sound")

playsound("output.mp3")

print("Done playing sound")