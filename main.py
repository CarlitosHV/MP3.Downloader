from pytube import YouTube
import os
import re


def format_video_title(title):
    # Reemplazamos guiones bajos y quitamos el símbolo | por si lo tiene
    words = title.split("_")
    formatted_title = " ".join(word.capitalize() for word in words)

    formatted_title = re.sub(r'[\\/:"*?<>|]', '', formatted_title)
    return formatted_title


while True:
    # Link que puso el usuario
    url = input(
        "Ingresa el enlace del video de YouTube que deseas descargar y convertir a MP3 (o 'salir' para terminar):\n>> ")

    if url.lower() == 'salir':
        break

    try:
        yt = YouTube(url)
    except:
        print("Error: No se pudo obtener el video desde el enlace proporcionado.")
        continue

    # Extraemos solo el audio del video
    video = yt.streams.filter(only_audio=True).first()

    # Preguntamos la ruta de guardado del archivo
    destination = input("Ingresa la ruta de destino (Dejar en blanco para el directorio actual):\n") or '.'

    # Descargamos el archivo
    out_file = video.download(output_path=destination)

    # Obtenemos el nombre del archivo formateado
    video_title = format_video_title(yt.title)

    # Creamos el nuevo nombre con el siguiente formato: NombreArtista - NombreCancion.mp3
    # No olvides reemplazar NombreArtista por el que estás descargando o puedes personalizar el título
    new_filename = f'Artista - {video_title}.mp3'

    # Construimos el path final del archivo
    new_file_path = os.path.join(destination, new_filename)

    # Renombramos y movemos el archivo final
    os.rename(out_file, new_file_path)

    # Imprimimos un resultado de completado
    print(yt.title + " se ha descargado completamente como " + new_filename)

    # Preguntamos si quiere seguir descargando más archivos MP3
    choice = input("¿Deseas continuar descargando más videos? (s/n):\n")
    if choice.lower() != 's':
        break
