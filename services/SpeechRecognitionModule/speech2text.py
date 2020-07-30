import speech_recognition as sr

def recognise_file(file, lang='de'):
    if lang == 'de':
        lang = 'de-DE'
    elif lang == 'en':
        lang = 'en-EN'
    elif lang == 'ru':
        lang = 'ru-RU'

    r = sr.Recognizer()
    
    with sr.AudioFile(file) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text, language=lang)
            print('Converting audio transcripts into text ...')
            print(text)
            return text
        except:
            print('Sorry.. run again...')

def recognise_mic(lang='de'):
    if lang == 'de':
        lang = 'de-DE'
    elif lang == 'en':
        lang = 'en-EN'
    elif lang == 'ru':
        lang = 'ru-RU'

    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks")
        
        try:
            text = r.recognize_google(audio_text, language=lang)
            print("Text: "+text)
            return text
        except:
            print("Sorry, I did not get that")