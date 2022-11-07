import html

from google.cloud import texttospeech

def text_to_ssml(text):
    escaped_lines = html.escape(text)
    ssml = "{}".format(
        escaped_lines.replace("¥n", '¥n<break time="1s"/>')
    )
    return ssml

def ssml_to_speech(ssml, file, language_code):
    gender = texttospeech.SsmlVoiceGender.FEMALE
    ttsClient = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=ssml)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=gender
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = ttsClient.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    with open(file, 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file ' + file)
    return file

if __name__ == '__main__':
    print('speech')