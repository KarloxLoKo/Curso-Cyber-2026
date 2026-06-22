import requests
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
import os
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
import schedule
import time

RSS_URL = "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"
CSV_FILE = "titulares_elpais.csv"

stopwords_es = set(STOPWORDS)
stopwords_es.update([
    "el", "la", "los", "las", "de", "del", "a", "y", "en", "que", "un",
    "una", "por", "con", "su", "se", "al", "lo", "para", "como", "más", "es", "que",
    "despues", "si", "sin", "da", "és", "cada", "sí", "ha", "hace", "o", "cada", "qué", "pero",
    "tras", "sobre", "dos", "uno", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
    "diez", "después", "cero", "año", "abren", "hablar", "viene", "wrapped", "veo", "puertas",
    "años", "parte", "crear", "otras", "esta", "casa"
    ])

def recolectar_titulares():
    response = requests.get(RSS_URL)
    root = ET.fromstring(response.content)

    titulares = []
    for item in root.findall(".//item"):
        title = item.find('title').text
        link = item.find('link').text
        categories = [cat.text for cat in item.findall('category')]
        pubDate = item.find('pubDate').text

        titulares.append({
            "fecha_recolecta": datetime.now(),
            "fecha_publicacion": pubDate,
            "titular": title,
            "link": link,
            "categorias": ", ".join(categories)
            })

    df = pd.DataFrame(titulares)

    if os.path.exists(CSV_FILE):
        df_old = pd.read_csv(CSV_FILE)
        df = pd.concat([df_old, df], ignore_index=True)

    df.to_csv(CSV_FILE, index=False)
    print(f"Se han guardado {len(titulares)} titulares. Total historico: {len(df)}")

    generar_nube(df)

def generar_nube(df):
    text = " ".join(df['titular'].dropna().tolist())
    if not text.strip():
        print("No hay titulares para generar la nube de palabras.")
        return

    wordcloud = WordCloud(
        width=800,
        height=600,
        background_color='white',
        stopwords=stopwords_es
        ).generate(text)

    plt.figure(figsize=(15, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("Nube de palabras de titulares", fontsize=16)
    plt.show()

def job():
    recolectar_titulares()

schedule.every(1).hours.do(job)

print("Iniciando el seguimiento de titulares de El Pais...")
job()

while True:
    schedule.run_pending()
    time.sleep(60)
