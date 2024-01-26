<<<<<<< Updated upstream
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

=======
from flask import Flask, render_template, request, send_from_directory
from dotenv import load_dotenv
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
@app.route('/upload', methods=['POST'])
def upload_files():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']

        if file1.filename and file2.filename:
            filename1 = secure_filename(file1.filename)
            filename2 = secure_filename(file2.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            return 'Files uploaded successfully'
        else:
            return 'Please select two files before uploading.'
    return 'Failed to upload files'

=======
    return render_template('index.html', fuentes=fuentes_data)
>>>>>>> Stashed changes

if __name__ == '__main__':
    app.run(debug=True)
