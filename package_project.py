# Script para empaquetar el proyecto en un archivo ZIP limpio (EvaluacionModular10.zip)

import zipfile
import os

def empaquetar(nombre_zip="EvaluacionModular10.zip"):
    excluir = ["__pycache__", ".git", ".venv", "mlops-env", nombre_zip]

    with zipfile.ZipFile(nombre_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("."):
            # Filtrar carpetas excluidas
            dirs[:] = [d for d in dirs if d not in excluir]

            for file in files:
                if file in excluir or file == nombre_zip:
                    continue
                ruta_completa = os.path.join(root, file)
                ruta_relativa = os.path.relpath(ruta_completa, ".")
                zipf.write(ruta_completa, ruta_relativa)
                print(f"✅ Añadido: {ruta_relativa}")

    print(f"\n📦 Proyecto empaquetado en {nombre_zip} (limpio)")

if __name__ == "__main__":
    empaquetar()