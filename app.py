import io
from xml.etree.ElementTree import tostring
from flask import Flask, request
from flask import jsonify
from flask import Flask, render_template, request, redirect, session, jsonify

from config import SUPABASE_API_URL, SUPABASE_PROJECT_URL
from supabase.client import create_client, Client
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import csv


app = Flask(__name__)
app.secret_key = 'secret-key'

supabase: Client = create_client(SUPABASE_PROJECT_URL, SUPABASE_API_URL)

@app.route('/')
def test_connection():
    try:
        # Realizar una consulta simple a la base de datos
        response = supabase.table('Users').select("*").execute()

        print(response)


        # Comprobar si la consulta fue exitosa
        if response is not None and response.data is not None:
            return 'La conexión con Supabase es exitosa.'
        else:
            return 'Hubo un problema al conectar con Supabase.'
    except Exception as e:
        return f'Hubo un error al conectar con Supabase: {str(e)}'

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.json

        # Verificar que todos los campos necesarios estén presentes en la solicitud
        required_fields = ['name', 'email', 'password', 'user_type']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Faltan campos obligatorios'}), 400

        nombre = data['name']
        correo = data['email']
        password = data['password']
        tipo_usuario = data['user_type']

        try:
            # Insertar usuario en la base de datos de Supabase
            response = supabase.auth.sign_up({
                "email": correo,
                "password": password,
                "options": {
                    "data": {
                        "name": nombre,
                        "user_type": tipo_usuario,
                    }
                }
            })

            return jsonify({'message': 'Usuario registrado exitosamente'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')

        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})

            res = supabase.auth.get_session()
            print(res)
            print("AAAAAAAAAAAWWWWOOOOOOOOOOOO")
            if response:
                session['access_token'] = res.access_token
                session['user'] = res.user.id
                session['role'] = res.user.user_metadata['user_type']

                return jsonify({'message': 'Inicio de sesión exitoso'})

            else:
                return 'Credenciales incorrectas. Inténtalo de nuevo.'
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return render_template('login.html')


@app.route('/logout')
def logout():
    if 'access_token' in session:
        del session['access_token']
    return redirect('/')

@app.route('/upload/<database>', methods=['POST'])
def upload(database):
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    if file:
        inserted_ids = parse_and_insert(file, database)

        return jsonify(inserted_ids)

def parse_and_insert(file, database):
    inserted_ids = []
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_reader = csv.DictReader(stream)


    if database == "ieeexplore":
        target_columns = ['document title', 'authors', 'author affiliations', 'publication title', 'date added to xplore', 'publication year', 'volume', 'issue', 'start page', 'end page', 'abstract', 'issn', 'isbns', 'doi', 'funding information', 'pdf link', 'author keywords', 'ieee terms', 'inspec controlled terms', 'inspec non-controlled terms', 'mesh_terms', 'article citation count', 'patent citation count', 'reference count', 'license', 'online data', 'issue date', 'meeting date', 'publisher', 'document identifier']
    elif database == "eric":
        target_columns = ['own', 'ti', 'au', 'ot', 'jt', 'so', 'oid', 'vi', 'ip', 'pg', 'dp', 'lid', 'ab', 'issn', 'la', 'pt']
    elif database == "historial":
        target_columns = ['document title', 'authors', 'author affiliations', 'publication title', 'date added to xplore', 'publication year', 'volume', 'issue', 'start page', 'end page', 'abstract', 'issn', 'isbns', 'doi', 'funding information', 'pdf link', 'author keywords', 'ieee terms', 'inspec controlled terms', 'inspec non-controlled terms', 'mesh_terms', 'article citation count', 'patent citation count', 'reference count', 'license', 'online data', 'issue date', 'meeting date', 'publisher', 'document identifier']
    elif database == "jstor":
        target_columns = ['document identifier', 'document identifier', 'document identifier', 'url', 'abstract', 'author', 'journal', 'number', 'pages', 'publisher', 'title', 'urldate', 'volume', 'year']
    elif database == "pubmed":
        target_columns = ['pmid', 'authors', 'citation', 'first author', 'journal/book', 'publication year', 'create date', 'pmcid', 'nihms id', 'doi']
    elif database == "sciencedirect":
        target_columns = ['campo 1', 'campo 2', 'campo 3', 'campo 4', 'campo 5', 'campo 6', 'campo 7', 'campo 8', 'campo 9', 'campo 10']
    elif database == "scopus":
        target_columns = [
        'authors',
        'author full names',
        'author(s) id',
        'title',
        'year',
        'source title',
        'volume',
        'issue',
        'art. No.',
        'page start',
        'page end',
        'page count',
        'cited by',
        'doi',
        'link',
        'affiliations',
        'authors with affiliations',
        'abstract',
        'author keywords',
        'index keywords',
        'molecular sequence numbers',
        'chemicals/cas',
        'tradenames',
        'manufacturers',
        'funding details',
        'funding texts',
        'references',
        'correspondence address',
        'editors',
        'publisher',
        'sponsors',
        'conference name',
        'conference date',
        'conference location',
        'conference code',
        'issn',
        'isbn',
        'coden',
        'pubmed id',
        'language of original document',
        'abbreviated source title',
        'document type',
        'publication stage',
        'open access',
        'source',
        'eid'
        ]

    elif database == "wos":
        target_columns = [
        'authors',
        'author full names',
        'author(s) id',
        'title',
        'year',
        'source title',
        'volume',
        'issue',
        'art. no.',
        'page start',
        'page end',
        'page count',
        'cited by',
        'doi',
        'link',
        'affiliations',
        'authors with affiliations',
        'abstract',
        'author keywords',
        'index keywords',
        'molecular sequence numbers',
        'chemicals/cas',
        'tradenames',
        'manufacturers',
        'funding details',
        'funding texts',
        'references',
        'correspondence address',
        'editors',
        'publisher',
        'sponsors',
        'conference name',
        'conference date',
        'conference location',
        'conference code',
        'issn',
        'isbn',
        'coden',
        'pubmed id',
        'language of original document',
        'abbreviated source title',
        'document type',
        'publication stage',
        'open access',
        'source',
        'eid'
        ]

    for row in csv_reader:
        # Filter the row to include only the columns present in your target list
        filtered_data = {}

        # Ensure all values are strings; handle any special cases as needed
        for col in target_columns:
            # Convert CSV column names to lowercase to match the database column names
            normalized_col = col.lower()
            # Check if the normalized column name exists in the row (with case normalization)
            if normalized_col in (key.lower() for key in row):
                # Find the original column name in the row that matches the normalized column name
                original_col_name = next((key for key in row if key.lower() == normalized_col), None)
                if original_col_name:
                    # Use the original column name to get the value from the row
                    filtered_data[col] = row[original_col_name] if row[original_col_name] not in (None, "") else ""
            else:
                # Optionally handle missing columns in the CSV, if needed
                filtered_data[col] = ""


        # Insert filtered data into the table
        response = supabase.table("IEEE Xplore").insert(filtered_data).execute()

        # Process the response as before
        if response.data:
            inserted_id = response.data[0]['id']  # Adjust based on your table's ID column name
            inserted_ids.append(inserted_id)
        elif response.error:
            print(f"Error inserting data: {response.error.message}")
            continue  # Handle errors appropriately
    return inserted_ids


if __name__ == '__main__':
    app.run(debug=True, port=8000)
