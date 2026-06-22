import cv2
import matplotlib.pyplot as plt
import numpy as np

# === 1. Cargar imagen ===
ruta = "/home/kali/Descargas/Plank.webp"  # Cambia por la ruta de tu imagen
imagen = cv2.imread(ruta)

if imagen is None:
    print("No se pudo cargar la imagen. Verifica la ruta.")
    exit()

# === 2. Convertir a escala de grises ===
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# === 3. Aplicar Sobel en X y Y ===
sobel_x = cv2.Sobel(gris, cv2.CV_64F, 1, 0, ksize=3)  # Derivada en X
sobel_y = cv2.Sobel(gris, cv2.CV_64F, 0, 1, ksize=3)  # Derivada en Y

# === 4. Calcular magnitud del gradiente ===
magnitud = cv2.magnitude(sobel_x, sobel_y)

# Convertimos la magnitud a rango 0–255 para mostrarla correctamente
magnitud = cv2.convertScaleAbs(magnitud)

# === 5. Mostrar resultados ===
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
plt.title("Original")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(gris, cmap='gray')
plt.title("Escala de grises")
plt.axis("off")

plt.subplot(2, 2, 3)
plt.imshow(sobel_x, cmap='gray')
plt.title("Sobel X (bordes verticales)")
plt.axis("off")

plt.subplot(2, 2, 4)
plt.imshow(sobel_y, cmap='gray')
plt.title("Sobel Y (bordes horizontales)")
plt.axis("off")

plt.tight_layout()
plt.show()
