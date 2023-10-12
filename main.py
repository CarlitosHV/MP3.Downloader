from pytube import YouTube
from moviepy.editor import *
import os
import re


def format_video_title(title):
    # Reemplazamos guiones bajos y quitamos caracteres no permitidos
    formatted_title = re.sub(r'[\\/:"*?<>|]', '', title)
    return formatted_title


while True:
    # Link que puso el usuario
    url = input("Ingresa el enlace del video de YouTube que deseas descargar y convertir a MP3 (o 'salir' para terminar):\n>> ")

    if url.lower() == 'salir':
        break

    try:
        yt = YouTube(url)
    except Exception as e:
        print(f"Error: No se pudo obtener el video desde el enlace proporcionado. Error: {str(e)}")
        continue

    # Preguntamos la ruta de guardado del archivo
    destination = input("Ingresa la ruta de destino (Dejar en blanco para el directorio actual):\n") or '.'

    # Descargamos el archivo
    try:
        out_file = yt.streams.filter(only_audio=True, file_extension='mp4', abr='128kbps').first().download(output_path=destination)
    except Exception as e:
        print(f"Error al descargar el archivo. Error: {str(e)}")
        continue

    # Obtenemos el nombre del archivo formateado
    video_title = format_video_title(yt.title)

    # Creamos el nuevo nombre
    new_filename = f'{video_title}.mp3'

    # Construimos el path final del archivo
    new_file_path = os.path.join(destination, new_filename)

    # Convertimos el archivo a formato MP3
    try:
        audio = AudioFileClip(out_file)
        audio.write_audiofile(new_file_path)
    except Exception as e:
        print(f"Error al convertir a MP3. Error: {str(e)}")
        continue

    # Eliminamos el archivo descargado en formato mp4
    os.remove(out_file)

    # Imprimimos un resultado de completado
    print(yt.title + " se ha descargado y convertido a MP3 correctamente como " + new_filename)

    # Preguntamos si quiere seguir descargando más archivos MP3
    choice = input("¿Deseas continuar descargando más videos? (s/n):\n")
    if choice.lower() != 's':
        break
