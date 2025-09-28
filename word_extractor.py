import json
import os
from pydub import AudioSegment
from pathlib import Path
import re

def extract_words_from_audio(mp3_file_path, json_file_path, output_dir="./extracted_words"):
    """
    Extrae palabras individuales de un archivo de audio basándose en la transcripción JSON.
    
    Args:
        mp3_file_path (str): Ruta al archivo MP3 original
        json_file_path (str): Ruta al archivo JSON con la transcripción
        output_dir (str): Directorio donde guardar las palabras extraídas
    """
    
    # Crear directorio de salida si no existe
    Path(output_dir).mkdir(exist_ok=True)
    
    # Cargar el archivo de audio
    print(f"Cargando audio: {mp3_file_path}")
    audio = AudioSegment.from_mp3(mp3_file_path)
    
    # Cargar el JSON
    print(f"Cargando transcripción: {json_file_path}")
    with open(json_file_path, 'r', encoding='utf-8') as f:
        transcription = json.load(f)
    
    # Contador para palabras repetidas
    word_counter = {}
    
    # Procesar cada segmento de la transcripción
    for segment in transcription:
        # Verificar si el segmento tiene palabras individuales
        if 'words' not in segment:
            continue
            
        # Procesar cada palabra en el segmento
        for word_info in segment['words']:
            word = word_info['word'].lower().strip()
            start_time = word_info['start']
            end_time = word_info['end']
            
            # Limpiar la palabra de caracteres especiales para el nombre del archivo
            clean_word = re.sub(r'[^\w\s-]', '', word)
            clean_word = re.sub(r'\s+', '_', clean_word)
            
            # Saltar si la palabra está vacía después de la limpieza
            if not clean_word:
                continue
            
            # Verificar si es una palabra individual (no una frase)
            # Consideramos que si tiene espacios o es muy larga, podría ser una frase
            if len(clean_word.split('_')) > 1 and len(clean_word) > 15:
                print(f"Saltando posible frase: '{word}'")
                continue
            
            # Manejar palabras repetidas
            if clean_word in word_counter:
                word_counter[clean_word] += 1
                filename = f"{clean_word}_{word_counter[clean_word]}.mp3"
            else:
                word_counter[clean_word] = 1
                filename = f"{clean_word}.mp3"
            
            # Ruta completa del archivo de salida
            output_path = os.path.join(output_dir, filename)
            
            # Extraer el segmento de audio (convertir segundos a milisegundos)
            start_ms = int(start_time * 1000)
            end_ms = int(end_time * 1000)
            
            # Agregar un pequeño padding para evitar cortes abruptos
            padding = 100  # 100ms de padding
            start_ms = max(0, start_ms - padding)
            end_ms = min(len(audio), end_ms + padding)
            
            word_segment = audio[start_ms:end_ms]
            
            # Guardar el archivo
            word_segment.export(output_path, format="mp3")
            
            print(f"Extraída: '{word}' -> {filename} ({start_time:.2f}s - {end_time:.2f}s)")
    
    print(f"\nExtracción completada. Total de palabras extraídas: {sum(word_counter.values())}")
    print(f"Palabras únicas: {len(word_counter)}")
    print(f"Archivos guardados en: {output_dir}")

def main():
    """
    Función principal para ejecutar el extractor.
    Modifica las rutas según tus archivos.
    """
    
    # Rutas de los archivos (modifica estas según tus archivos)
    mp3_file = "nietzsche.mp3"  # Cambia por la ruta de tu archivo MP3
    json_file = "nietzsche.json"  # Cambia por la ruta de tu archivo JSON
    
    # Verificar que los archivos existen
    if not os.path.exists(mp3_file):
        print(f"Error: No se encontró el archivo de audio: {mp3_file}")
        return
    
    if not os.path.exists(json_file):
        print(f"Error: No se encontró el archivo JSON: {json_file}")
        return
    
    # Ejecutar la extracción
    try:
        extract_words_from_audio(mp3_file, json_file)
    except Exception as e:
        print(f"Error durante la extracción: {str(e)}")

if __name__ == "__main__":
    # Ejemplo de uso alternativo con argumentos específicos
    # extract_words_from_audio("mi_audio.mp3", "mi_transcripcion.json", "./palabras_extraidas")
    
    main()
