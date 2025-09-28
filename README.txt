# Nuevo
## Instalar
> micromamba activate 311

pip install videogrep
pip install vosk

## Preparacion
generar json (modelo default de vosk sm ingles):

videogrep --input nietzsche.mp3 --transcribe 

Usando un modelo custom de vosk https://alphacephei.com/vosk/models:
videogrep -i nietzsche.mp3 --transcribe --model vosk-model-small-es-0.42

Para saber que palabras hay presentes:
videogrep -i nietzsche.mp3 --ngrams 1


Generar clips de palabras interesantes:
videogrep -i nietzsche.mp3  --search "verdad" --export-clips


Search term, as a regular expression. You can add as many of these as you want. For example:


videogrep --input path/to/video --search 'search phrase' --search 'another search' --search 'a third search' --output coolvid.mp4

Ya no existe el --extract de audiogrep, si querés extraer:

python3 extract_words.py

## Uso

mpv verdad/supercut_000*

# Método Viejo
https://github.com/antiboredom/audiogrep

La forma de usar esto es


tenés que si o si hacer esto antes?

audiogrep --input path/to/*.mp3 --transcribe


Despues podes hacer el resto, como extraer:
audiogrep --input path/to/*.mp3 --extract


