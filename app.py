import flet as ft
from cryptography.fernet import Fernet

def main(page: ft.Page):
    page.title = "HERMES - Cifrado/Descifrado de Archivos"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 20
    modo = ft.Text(value="Selecciona una opción para continuar", size=18)
    archivo_seleccionado = ft.Text(value="", size=16, color=ft.Colors.BLUE)

    # Campo de clave oculto inicialmente
    clave_campo = ft.TextField(label="Clave de cifrado", visible=False)
    hidden_ruta = ft.TextField(value="", visible=False)
    mensaje_funcion = ft.TextField(value="", visible=False)
    
    sobrescribir_checkbox = ft.Checkbox(label="Sobrescribir archivo original", value=False)
    # Explorador de archivos
    file_picker = ft.FilePicker()

    def on_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            # Ocultar el campo de clave antes de comprobar
            clave_campo.visible = False

            if len(e.files) > 1:
                archivo_seleccionado.value = "Por favor, selecciona un solo archivo."
            else:
                archivo_seleccionado.value = f"Archivo seleccionado: {e.files[0].name}"
                #print(e.files)
                hidden_ruta.value = e.files[0].path
                if modo.value.startswith("🛡️"):
                    # Generar nueva clave
                    clave = Fernet.generate_key().decode()
                    clave_campo.value = clave
                    clave_campo.visible = True
                    boton_funcion.text = "Cifrar"
                    boton_funcion.visible = True
                    
                elif modo.value.startswith("🔓"):
                    # Mostrar campo de clave para descifrado
                    clave_campo.visible = True
                    clave_campo.label = "Clave de cifrado (para descifrar)"
                    clave_campo.helper_text = "Introduce la clave utilizada para cifrar el archivo."
                    boton_funcion.text = "Descifrar"
                    boton_funcion.visible = True

        else:
            archivo_seleccionado.value = "No se seleccionó ningún archivo"

        page.update()

    file_picker.on_result = on_file_result
    page.overlay.append(file_picker)

    def lanzar_funcion(e):
        if not hidden_ruta.value:
            page.snack_bar = ft.SnackBar(content=ft.Text("Por favor, selecciona un archivo primero."))
            page.snack_bar.open = True
            page.update()
            return

        try:
            clave = clave_campo.value.encode()
            fernet = Fernet(clave)

            with open(hidden_ruta.value, "rb") as file:
                data = file.read()

            if modo.value.startswith("🛡️"):
                if sobrescribir_checkbox.value:
                    output_path = hidden_ruta.value
                else:
                    output_path = hidden_ruta.value + ".penc"
                encrypted_data = fernet.encrypt(data)
                with open(output_path, "wb") as file:
                    file.write(encrypted_data)
                mensaje_funcion.value = f"✅ Archivo cifrado exitosamente: {hidden_ruta.value}"

            elif modo.value.startswith("🔓"):
                decrypted_data = fernet.decrypt(data)
                if hidden_ruta.value.endswith(".penc"):
                    if sobrescribir_checkbox.value:
                        output_path = hidden_ruta.value
                    else:
                        output_path = hidden_ruta.value[:-5]
                with open(output_path, "wb") as file:
                    file.write(decrypted_data)
                mensaje_funcion.value = f"✅ Archivo descifrado exitosamente: {hidden_ruta.value}"

            mensaje_funcion.visible = True
            page.snack_bar = ft.SnackBar(content=ft.Text(mensaje_funcion.value))
            page.snack_bar.open = True

        except Exception as err:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"❌ Error: {str(err)}"))
            page.snack_bar.open = True

        page.update()
    
    def seleccionar_cifrar(e):
        modo.value = "🛡️ Modo: CIFRAR archivo"
        file_picker.pick_files()
        page.update()

    def seleccionar_descifrar(e):
        modo.value = "🔓 Modo: DESCIFRAR archivo"
        file_picker.pick_files()
        page.update()

    # Interfaz
    
    boton_funcion = ft.ElevatedButton("Lanzar", visible=False, on_click=lanzar_funcion)
    page.add(
        ft.Text("🔐 HERMES - Cifrado/Descifrado de Archivos", size=24, weight=ft.FontWeight.BOLD),
        ft.Row([
            ft.ElevatedButton("Cifrar", on_click=seleccionar_cifrar),
            ft.ElevatedButton("Descifrar", on_click=seleccionar_descifrar)
        ]),
        modo,
        archivo_seleccionado,
        clave_campo ,
        sobrescribir_checkbox,
        boton_funcion,
        mensaje_funcion
    )

ft.app(target=main)
