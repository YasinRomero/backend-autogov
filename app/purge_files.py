import sys
try:
    from google import genai
except ImportError:
    print("Error: Sin librería google-genai")
    sys.exit(1)

def purge_google_files():
    api_key = input("Pega API Key: ").strip()
    
    if not api_key:
        print("Falta el API Key.")
        return

    try:
        client = genai.Client(api_key=api_key)
        
        files = list(client.files.list())
        
        if not files:
            print("No hay archivos para borrar en esta cuenta.")
            return

        print(f"Se encontraron {len(files)} archivos. Iniciando eliminación...")
        
        deleted_count = 0
        for file in files:
            try:
                client.files.delete(name=file.name)
                print(f"Eliminado: {file.display_name} ({file.name})")
                deleted_count += 1
            except Exception as e:
                print(f"No se pudo borrar {file.display_name}: {e}")

        print(f"\n Limpieza completada! Se borraron {deleted_count} archivos.")

    except Exception as e:
        print(f"Error de conexión/Auth: {e}")

if __name__ == "__main__":
    purge_google_files()