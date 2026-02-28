import streamlit as st
import speech_recognition as sr
from moviepy import VideoFileClip, concatenate_videoclips
from PIL import ImageTk, Image
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from googletrans import Translator
translator = Translator()
list_of_words=["acidity","hospital","fasten","bandage","heartbreaking","digestion","sneeze","nurse","cotton","drink","medicine","pill","bp","symptoms","doctor","toilet"]
def speech_to_text():
    r = sr.Recognizer()
   

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        st.info("Please speak into the microphone...")
        audio = r.listen(source, timeout=10)

    try:
        text = r.recognize_google(audio,language='te-IN')
        st.success("Speech Recognition Result:")
        st.write(text)
        # Translate and display the translated text
        translated_text = translate_to_english(text)
        st.info("Translated Text:")
        st.write(translated_text)
        clean_text = preprocess_text(translated_text)
        st.write(clean_text)
        #splitting into words
        play_seq=clean_text.split()
        found=0
        if len(play_seq)==1:
            for i in list_of_words:
                if i==clean_text:
                    found=1
                    break
            if found==1:
                # load the video corresponding to the speech
                
                video_file = open('dataset/{}.mp4'.format(clean_text), 'rb')
                video_bytes = video_file.read()

                st.video(video_bytes)
    
                
            else:
                st.error(f"Failed to load video for {clean_text}")
            
        # Generate video based on translated text
        else:
                clips=[]
                for i in play_seq:
                    
                    cnt=list_of_words.count(i)
                    if(cnt==1):
                        video_file = VideoFileClip('dataset/{}.mp4'.format(i), 'rb')
                        clips.append(video_file)
                final = concatenate_videoclips(clips,method='compose')
                # Save the final video to a file
                final_path = 'dataset/{}.mp4'.format(clean_text)
                final.write_videofile(final_path, codec='libx264')
                
                try:
                    command=clean_text
                    # load the video corresponding to the speech
                    video_file = open('Rishika/dataset/{}.mp4'.format(clean_text), 'rb')
                    video_bytes = video_file.read()

                    st.video(video_bytes)
                    
                    
                except:
                    
                    st.error(f"అవతార్ లోడ్ చేయడం విఫలమైంది,పదము డేటాసెలో అందుబాటులో లేదు")
        
    except sr.UnknownValueError:
        st.warning("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
# Function to translate text to English
def translate_to_english(text):
    
    translation = translator.translate(text, src='te', dest='en')
    return translation.text.lower()
# Function to generate video

def preprocess_text(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(filtered_tokens)        
def main():
    st.title("Inclusive Healthcare Journey: Virtual Communication for Hearing-Impaired Patients in Telugu States Using Gestures")

    st.write(
        "This is a simple speech-to-avatar application using Streamlit and SpeechRecognition. Click the button below and start speaking into your microphone."
    )

    if st.button("Start Speech Recognition"):
        speech_to_text()

if __name__ == "__main__":
    main()