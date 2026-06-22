import cv2
import matplotlib.pyplot as plt
from skimage.feature import hog

# === 1. Cargar imagen ===
ruta = r"/home/kali/Descargas/Plank.webp"  # Cambia por tu ruta
imagen = cv2.imread(ruta)

if imagen is None:
    print("No se pudo cargar la imagen. Verifica la ruta.")
    exit()

# Convertir a escala de grises
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# === 2. Descriptores ===

# --- a) SIFT ---
sift = cv2.SIFT_create()
kp_sift, des_sift = sift.detectAndCompute(gris, None)
img_sift = cv2.drawKeypoints(imagen, kp_sift, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# --- b) ORB ---
orb = cv2.ORB_create()
kp_orb, des_orb = orb.detectAndCompute(gris, None)
img_orb = cv2.drawKeypoints(imagen, kp_orb, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# --- c) HOG (devuelve la imagen de visualización) ---
fd, hog_image = hog(gris, pixels_per_cell=(16, 16), cells_per_block=(2, 2),
                    visualize=True, block_norm='L2-Hys')
hog_image = (hog_image * 255).astype('uint8')

# === 3. Mostrar imágenes ===
plt.figure(figsize=(12, 10))

plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
plt.title("Original")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(cv2.cvtColor(img_sift, cv2.COLOR_BGR2RGB))
plt.title("SIFT")
plt.axis("off")

plt.subplot(2, 2, 3)
plt.imshow(cv2.cvtColor(img_orb, cv2.COLOR_BGR2RGB))
plt.title("ORB")
plt.axis("off")

plt.subplot(2, 2, 4)
plt.imshow(hog_image, cmap='gray')
plt.title("HOG")
plt.axis("off")

plt.tight_layout()
plt.show()
