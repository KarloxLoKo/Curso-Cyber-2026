import cv2 
# pip install opencv-python
import matplotlib.pyplot as plt

# === 1. Cargar imagen ===
ruta = "/home/kali/Descargas/Plank.webp"  # Cambia por la ruta de tu imagen
imagen = cv2.imread(ruta)

# Comprobamos si se cargó correctamente
if imagen is None:
    print("No se pudo cargar la imagen. Verifica la ruta.")
    exit()

# === 2. Convertir a escala de grises ===
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# === 3. Suavizado Gaussiano para reducir ruido ===
suavizada = cv2.GaussianBlur(gris, (5, 5), 1.4)

# === 4. Aplicar detector de bordes Canny ===
bordes = cv2.Canny(suavizada, 100, 200)
# Los valores 100 y 200 son los umbrales inferior y superior

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
plt.imshow(suavizada, cmap='gray')
plt.title("Suavizada (Gaussiana)")
plt.axis("off")

plt.subplot(2, 2, 4)
plt.imshow(bordes, cmap='gray')
plt.title("Bordes Canny")
plt.axis("off")

plt.tight_layout()
plt.show()
