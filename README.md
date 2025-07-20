# HERMES - Cifrado/Descifrado de Archivos

**HERMES** es una herramienta sencilla para cifrar y descifrar archivos usando el algoritmo **Fernet** de la librería `cryptography`. Esta aplicación permite cifrar archivos con una clave generada o proporcionada por el usuario, y también puede descifrar archivos previamente cifrados si se conoce la clave correcta.

## 🚀 Características

- **Cifrado**: Convierte archivos en un formato seguro utilizando una clave de cifrado.
- **Descifrado**: Restaura archivos cifrados a su estado original utilizando la clave adecuada.
- **Opciones**:
  - **Sobrescribir archivo original**: Permite reemplazar el archivo original con el archivo cifrado/descifrado.
  - **Interfaz gráfica**: Sencilla y fácil de usar, con selección de archivos y claves.
  
## 🛠️ Requisitos

Este programa requiere Python 3.7 o superior y las siguientes librerías:

- `flet` para la interfaz gráfica.
- `cryptography` para el cifrado y descifrado de archivos.

Para instalar las dependencias, simplemente ejecuta:

```bash
pip install flet cryptography
