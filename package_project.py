# ===========================================================
# 📦 package_project.py — Script para comprimir el proyecto
# ===========================================================
# Este script genera un archivo ZIP con el contenido del proyecto,
# excluyendo entornos virtuales, cachés, repositorios Git, 
# archivos empaquetados previos y otros innecesarios.
# ===========================================================

import zipfile
import os

def empaquetar(nombre_zip="EvaluacionModular10.zip"):
    excluir = [
        "__pycache__",
        ".git",
        ".github",       # los workflows suelen manejarse aparte
        ".venv",
        "venv",
        "mlops-env",
        ".env",
        ".vscode",
        nombre_zip
    ]

    with zipfile.ZipFile(nombre_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("."):
            # Filtrar carpetas a excluir
            dirs[:] = [d for d in dirs if d not in excluir]

            for file in files:
                if file in excluir or file == nombre_zip:
                    continue
                ruta_completa = os.path.join(root, file)
                ruta_relativa = os.path.relpath(ruta_completa, ".")
                zipf.write(ruta_completa, ruta_relativa)
                print(f"✅ Añadido: {ruta_relativa}")

    print(f"\n📦 Proyecto empaquetado correctamente en {nombre_zip}")

if __name__ == "__main__":
    empaquetar()