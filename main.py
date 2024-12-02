## Import Statements
from api_secrets import API_KEY_ASSEMBLYAI 
import os
import assemblyai as aai

## Imput File Setup
# assign directory
directory = ''

## API Setup
# replace with your API key
aai.settings.api_key = API_KEY_ASSEMBLYAI

## Speaker Labels Setup
config = aai.TranscriptionConfig(speaker_labels=True)

## Transcriber Setup
transcriber = aai.Transcriber()

## Word Replace Setup
words = [""]
words_replace = [""]
wrdlen = len(words)
 
## Iterate over files in directory
for filename in os.listdir(directory):
    # create output file
    out = filename[:-4] + ' output.txt'
    
    # get file
    audio = os.path.join(directory, filename)
    
    # checking if it is a file
    if os.path.isfile(audio):
        print(audio + " transcribing...")

        # create transcript
        transcript = transcriber.transcribe(audio, config)

        # check transcript status
        if transcript.status == aai.TranscriptStatus.error:
            # print error message
            print(transcript.error)
        else:
            # separate transcript into paragraphs
            paragraphs = transcript.get_paragraphs()

            # print each paragraph
            for paragraph in paragraphs:  

                # replace words
                for i in range(wrdlen):
                    paragraph.text = paragraph.text.replace(words[i], words_replace[i])

                ## If want speaker tags, uncomment this section
                # for utterance in transcript.utterances:
                #     with open(out, 'a') as file:
                #         file.write(f"Speaker {utterance.speaker}: {paragraph.text}\n\n")
                
                ## If do not want speaker tags, uncomment this section
                with open(out, 'a') as file:
                    file.write(f"{paragraph.text}\n\n")

            # summarize word replacements
            matches = transcript.word_search(words)

            for match in matches:
                print(f"Found '{match.text}' {match.count} times in the transcript")

# Let user know process is complete
print(f'done transcribing: transcription found in {out}')