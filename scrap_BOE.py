import requests
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
import os
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# =========================================================
# CANALES TEMÁTICOS DEL BOE
# =========================================================

BOE_CANALES = {
    "Ayudas": "ayudas",
    "Becas": "becas",
    "Cambios de divisas": "cambios",
    "Cartas de servicios": "cartas",
    "Convenios colectivos": "ccolectivos",
    "Convenios de colaboración": "ccolaboracion",
    "Declaraciones de impacto ambiental": "imp_amb",
    "Índices de préstamos hipotecarios": "prestamoss",
    "Planes de estudio": "planes",
    "Precios de labores de tabaco": "tabaco",
    "Premios": "premios",
    "Recursos gubernativos": "notariado",
    "Registros de Fundaciones": "fundaciones",
    "Sentencias del Tribunal Constitucional": "tc"
}

# =========================================================
# STOPWORDS
# =========================================================

stopwords_es = set(STOPWORDS)
stopwords_es.update([
    "el","la","los","las","de","del","a","y","en","que","un","una",
    "por","con","su","se","al","lo","para","como","más","es","pero",
    "tras","sobre","dos","uno","años","cada","esta","este"
])

# =========================================================
# UTILIDADES
# =========================================================

def get_rss_url(tema):
    """Devuelve URL real del BOE"""
    codigo = BOE_CANALES[tema]
    return f"https://www.boe.es/rss/canal.php?c={codigo}"


def parse_rss(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, timeout=10)

    try:
        root = ET.fromstring(r.content)
    except ET.ParseError:
        print("Error: RSS no válido o bloqueado")
        return []

    items = []

    for item in root.findall(".//item"):
        title = item.findtext("title", "")
        link = item.findtext("link", "")
        pubDate = item.findtext("pubDate", "")

        items.append({
            "fecha_recolecta": datetime.now(),
            "fecha_publicacion": pubDate,
            "titular": title,
            "link": link
        })

    return items

# =========================================================
# CSV (HISTÓRICO POR CANAL)
# =========================================================

def save_csv(datos, filename):
    if not datos:
        return pd.DataFrame(columns=[
            "fecha_recolecta",
            "fecha_publicacion",
            "titular",
            "link"
        ])

    df = pd.DataFrame(datos)

    if os.path.exists(filename):
        df_old = pd.read_csv(filename)
        df = pd.concat([df_old, df], ignore_index=True)

    df.to_csv(filename, index=False)
    return df

# =========================================================
# WORDCLOUD
# =========================================================

def generar_wordcloud(df, titulo):
    if df.empty or "titular" not in df.columns:
        print("No hay datos suficientes")
        return

    texto = " ".join(df["titular"].dropna().tolist())

    if not texto.strip():
        print("Sin texto para generar nube")
        return

    wc = WordCloud(
        width=1000,
        height=500,
        background_color="white",
        stopwords=stopwords_es
    ).generate(texto)

    plt.figure(figsize=(15, 7))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"BOE - {titulo}")
    plt.show()

# =========================================================
# OPCIÓN 1: WORDCLOUD (CON HISTÓRICO CSV)
# =========================================================

def opcion_wordcloud(tema):
    url = get_rss_url(tema)
    datos = parse_rss(url)

    file = f"boe_{BOE_CANALES[tema]}.csv"

    df = save_csv(datos, file)

    generar_wordcloud(df, tema)

# =========================================================
# OPCIÓN 2: BÚSQUEDA (SIN GUARDAR)
# =========================================================

def opcion_busqueda(tema):
    palabra = input("Palabra a buscar: ").lower()

    url = get_rss_url(tema)
    datos = parse_rss(url)

    resultados = [
        i for i in datos
        if palabra in i["titular"].lower()
    ]

    if not resultados:
        print("Sin resultados")
        return

    for r in resultados:
        print("\n-------------------------")
        print(r["fecha_publicacion"])
        print(r["titular"])
        print(r["link"])

# =========================================================
# MENÚ PRINCIPAL
# =========================================================

def menu():
    print("\n============================")
    print("   ANALIZADOR RSS BOE")
    print("============================\n")

    canales = list(BOE_CANALES.keys())

    for i, c in enumerate(canales, 1):
        print(f"{i}. {c}")

    try:
        idx = int(input("\nSelecciona canal: ")) - 1
        tema = canales[idx]
    except:
        print("Opción inválida")
        return

    print(f"\nCanal seleccionado: {tema}")
    print("\n1. WordCloud (histórico)")
    print("2. Buscar palabra (en vivo)")

    op = input("Opción: ")

    if op == "1":
        opcion_wordcloud(tema)
    elif op == "2":
        opcion_busqueda(tema)
    else:
        print("Opción inválida")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    menu()
