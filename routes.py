from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
import requests
from app import app, db, login_manager
from models import Usuario, Planta

API_KEY = 'sk-CZuC67c9cf191fa4b8981'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def home_():
    return render_template('inicio-login.html')

@app.route('/home')
@login_required
def home():
    return render_template('inicio-perfil.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já registrado!', 'danger')
            return redirect(url_for('register'))

        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.senha == senha:
            login_user(usuario)
            return redirect(url_for('home'))
        else:
            flash('E-mail ou senha incorretos.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))

@app.route('/atualizar-usuario/<int:id>', methods=['GET', 'POST'])
@login_required
def atualizar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']

        nova_senha = request.form['senha']
        if nova_senha:
            usuario.senha = nova_senha

        db.session.commit()
        flash('Dados atualizados com sucesso!', 'success')
        return redirect(url_for('home'))

    return render_template('dados-user.html', usuario=usuario)

@app.route('/deletar-usuario/<int:id>', methods=['POST'])
@login_required
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if usuario.id != current_user.id:
        flash('Você não tem permissão para deletar esta conta.', 'danger')
        return redirect(url_for('home'))

    plantas = Planta.query.filter_by(usuario_id=usuario.id).all()
    for planta in plantas:
        db.session.delete(planta)
    db.session.delete(usuario)
    db.session.commit()

    flash('Conta e plantas associadas deletadas com sucesso!', 'success')
    return redirect(url_for('home'))

@app.route('/jardim')
@login_required
def jardim():
    plantas = Planta.query.filter_by(usuario_id=current_user.id).all()
    return render_template('user.html', plantas=plantas)

@app.route('/visualizar-planta/<int:id>')
@login_required
def visualizar_planta(id):
    planta = Planta.query.get_or_404(id)
    if planta.usuario_id != current_user.id:
        return redirect(url_for('jardim'))
    return render_template('visualizar-planta.html', planta=planta)

@app.route('/adicionar-planta', methods=['GET'])
@login_required
def mostrar_formulario_adicionar_planta():
    url = 'https://perenual.com/api/species-list'
    params = {
        'key': API_KEY,
        'page': 1,
        'q': ''
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        plantas = response.json()['data']
    else:
        plantas = []
        flash('Erro ao buscar plantas da API.', 'danger')

    return render_template('adicionar-planta.html', plantas=plantas)

@app.route('/adicionar-planta', methods=['POST'])
@login_required
def adicionar_planta():
    planta_id = request.form.get('plantaSelecionada')

    if not planta_id:
        flash('Selecione uma planta válida.', 'danger')
        return redirect(url_for('mostrar_formulario_adicionar_planta'))

    url = f'https://perenual.com/api/species/details/{planta_id}'
    params = {'key': API_KEY}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        planta_info = response.json()

        # Converter listas em strings
        nome_cientifico = ', '.join(planta_info.get('scientific_name', ['N/A']))
        luz_solar = ', '.join(planta_info.get('sunlight', ['N/A']))
        tipo_solo = ', '.join(planta_info.get('soil', ['N/A']))

        nivel_cuidado = planta_info.get('care_level', 'N/A')
        if nivel_cuidado is None:
            nivel_cuidado = 'N/A'

        nova_planta = Planta(
            nome=planta_info.get('common_name', 'N/A'),
            nome_cientifico=nome_cientifico,
            agua=planta_info.get('watering', 'N/A'),
            luz_solar=luz_solar,
            nivel_cuidado=nivel_cuidado,
            tipo_solo=tipo_solo,
            imagem_url=planta_info.get('default_image', {}).get('original_url', 'N/A'),
            descricao=planta_info.get('description', ''),
            ciclo_vida=planta_info.get('cycle', ''),
            tamanho_medio=planta_info.get('dimensions', {}).get('type', ''),
            toxicidade=planta_info.get('poisonous_to_pets', ''),
            temperatura_ideal=planta_info.get('temperature', ''),
            dicas_cultivo=planta_info.get('care_guides', ''),
            usuario_id=current_user.id
        )
        db.session.add(nova_planta)
        db.session.commit()
    else:
        flash('Erro ao buscar detalhes da planta.', 'danger')

    return redirect(url_for('jardim'))

def get_plant_info(api_key, plant_name):
    search_url = 'https://perenual.com/api/species-list'
    search_params = {
        'key': api_key,
        'q': plant_name
    }

    search_response = requests.get(search_url, params=search_params)

    if search_response.status_code == 200:
        search_data = search_response.json()
        if search_data['data']:
            plant_id = search_data['data'][0]['id']

            details_url = f'https://perenual.com/api/species/details/{plant_id}'
            details_params = {
                'key': api_key
            }

            details_response = requests.get(details_url, params=details_params)

            if details_response.status_code == 200:
                details_data = details_response.json()

                # Converta listas em strings
                nome_cientifico = ', '.join(details_data.get('scientific_name', ['N/A']))
                luz_solar = ', '.join(details_data.get('sunlight', ['N/A']))
                tipo_solo = ', '.join(details_data.get('soil', ['N/A']))

                return {
                    'name': details_data.get('common_name', 'N/A'),
                    'scientific_name': nome_cientifico,
                    'watering': details_data.get('watering', 'N/A'),
                    'sunlight': luz_solar,
                    'care_level': details_data.get('care_level', 'N/A'),
                    'soil_type': tipo_solo,
                    'image_url': details_data.get('default_image', {}).get('original_url', 'N/A')
                }
    return None