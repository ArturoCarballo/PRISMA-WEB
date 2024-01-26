from flask import Flask, render_template, request, send_from_directory
from dotenv import load_dotenv
import os
from supabase.client import create_client, Client


# Cargar Variables de Entorno
load_dotenv()

# Inicializar Flask
app = Flask(__name__)

# Obtener las credenciales de Supabase
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

#Validacion si no detecta los valores
if supabase_url is None or supabase_key is None:
    raise ValueError("Las variables de entorno SUPABASE_URL y SUPABASE_KEY deben estar definidas.")

# Crear la instancia del cliente de Supabase
supabase: Client = create_client(supabase_url, supabase_key)

def get_fuentes():
    data = supabase.table("fuentes").select("*").execute()

    return data.data

@app.route('/')
def index():
    try:
        fuentes_data = get_fuentes()
    except ValueError as e:
        return str(e), 500

    return render_template('index.html', fuentes=fuentes_data)


if __name__ == '__main__':
    app.run(debug=True)
