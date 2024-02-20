from flask import Flask, request
from flask import jsonify
from flask import Flask, render_template, request, redirect, session, jsonify

import supabase
from supabase import create_client
from config import SUPABASE_API_URL, SUPABASE_PROJECT_URL
from supabase import create_client, Client
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user



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




if __name__ == '__main__':
    app.run(debug=True)