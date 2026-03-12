"""
SCRIPT: init_db.py
OBJETIVO:
    Crear e inicializar la base de datos SQLite del proyecto
    "Breast Cancer Clinical Data Analysis Platform".

FUNCIONALIDAD:
    1. Crea la carpeta database si no existe.
    2. Crea el archivo de base de datos SQLite.
    3. Ejecuta el esquema definido en schema.sql.
    4. Inserta datos artificiales desde seed_data.sql.
"""

from pathlib import Path
import sqlite3


def get_project_paths() -> dict:
    """
    Retorna las rutas base del proyecto.
    """
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent

    database_dir = project_root / "database"
    db_path = database_dir / "breast_cancer_clinical.db"
    schema_path = database_dir / "schema.sql"
    seed_path = database_dir / "seed_data.sql"

    return {
        "project_root": project_root,
        "database_dir": database_dir,
        "db_path": db_path,
        "schema_path": schema_path,
        "seed_path": seed_path,
    }


def ensure_database_directory(database_dir: Path) -> None:
    """
    Crea la carpeta database si no existe.
    """
    database_dir.mkdir(parents=True, exist_ok=True)


def create_connection(db_path: Path) -> sqlite3.Connection:
    """
    Crea y retorna una conexión a SQLite.
    """
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


def execute_sql_file(connection: sqlite3.Connection, file_path: Path) -> None:
    """
    Ejecuta el contenido de un archivo SQL.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

    sql_script = file_path.read_text(encoding="utf-8")
    connection.executescript(sql_script)


def initialize_database() -> None:
    """
    Inicializa completamente la base de datos:
    - crea carpeta
    - crea DB
    - ejecuta schema
    - inserta seed data
    """
    paths = get_project_paths()

    ensure_database_directory(paths["database_dir"])

    if paths["db_path"].exists():
        paths["db_path"].unlink()

    connection = create_connection(paths["db_path"])

    try:
        print("Creando estructura de base de datos...")
        execute_sql_file(connection, paths["schema_path"])

        print("Insertando datos de prueba...")
        execute_sql_file(connection, paths["seed_path"])

        connection.commit()
        print(f"Base de datos creada correctamente en: {paths['db_path']}")
    except Exception as error:
        connection.rollback()
        print(f"Error al inicializar la base de datos: {error}")
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()