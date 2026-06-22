import hashlib

def codificar_sha256(texto):
    # Convertir el texto a bytes
    texto_bytes = texto.encode('utf-8')
    # Crear el hash SHA-256
    hash_obj = hashlib.sha256(texto_bytes)
    # Obtener el hash en formato hexadecimal
    hash_hex = hash_obj.hexdigest()
    return hash_hex

# Programa principal
if __name__ == "__main__":
    texto = input("Introduce el texto a codificar: ")
    resultado = codificar_sha256(texto)
    print("\nHash SHA-256 generado:")
    print(resultado)
    input("\nPresiona Enter para salir...")
