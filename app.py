# Importação dos pacote
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

# Herdando a classe Flask
app = Flask(__name__)

# host='localhost',
# user='root',
# password='senac123456789',
# database='postomedico'

# Configurando uma chave secreta para sessão
app.secret_key = 'senac2024'

# Configuração do banco de dados Verificando a conexão

try:
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='senac123456789',
        database='postomedico'    
    )
    if conexao.is_connected():
        print('Conexão realizada com sucesso')
except OSError as error:
    print('Erro ao conectar: ', error)

# Herdando o método de execução dos scripts em SQL
cursor = conexao.cursor(dictionary=True)


# criação das rotas para o carregamento das páginas e realização das operações CRUD


# 1) Rota para acesso da página principal da aplicação
@app.route('/')
def index():
    if 'id_usuario' in session:
        return redirect(url_for('home'))

    return render_template('login.html')


# 2) Rota para criação de registros no banco
@app.route('/criar', methods = ['GET', 'POST'])
def criar():
    if 'id_usuario' in session:
        return redirect(url_for('login'))


    # Verificar qual método será usado na operação e atribuir
    # variáveis para receber os valores dos campos de texto(inputs)
    if request.method == 'POST':
        nome = request.form['nome']
        data_nascimeto = request.form['data_nascimento']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        cpf = request.form['cpf']

        # Comando em SQl para criar
        # o paciente
        comando = 'insert into paciente(nome, data_nascimento, endereco, telefone, cpf) values (%s, %s, %s, %s, %s)'

        # Variável que irá receber todos
        # os valores das variáveis anteriores
        valores = (nome, data_nascimeto, endereco, telefone, cpf)
        
        # Executar o comando em SQL
        cursor.execute(comando, valores)

        # Confirmar a execução do comando no banco de dados
        conexao.commit()


        
        # Atribuir um retorno podendo ser o redirecionamento para outra página
        return redirect(url_for('listar')) 
        # OBS: o parâmetro em 'url_for'
        # é a função criada para
        # carregar a rota desejada


    # Atribuir um retorno para o carregamento da página de de criação do paciente
    return render_template('criar.html')
    



# 3) Rota para seleção de registros no banco
@app.route('/listar')
def listar():
    # Comando em sql para selecionar paciente
    comando = 'select * from paciente'
# Executar o comando
    cursor.execute(comando)

    pacientes = cursor.fetchall()
# Retornar o resultado carregando outra pagina

# A primeira variável 'pacientes' recebe o resultado
# da execução do comando em SQL

# A segunda variável 'pacientes' é um apelido
# atribuído para ser carregado na página e
# realizar estruturas de programação
    return render_template('listar.html', pacientes = pacientes)



# 4) Rota para atualização de registros no banco

@app.route('/editar/<int:id>', methods = ['GET', 'POST'])
def editar(id):

    # Verificar qual método será
    # usado na operação e atribuir
    # variáveis para receber os valores
    # dos campos de texto(inputs)

    if request.method == 'POST':
        nome = request.form['nome']
        data_nascimeto = request.form['data_nascimento']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        cpf = request.form['cpf']

        comando = 'update paciente set nome = %s, data_nascimento = %s, endereco = %s, telefone = %s, cpf = %s where id = %s'

        valores = (nome, data_nascimeto, endereco, telefone, cpf, id)

        cursor.execute(comando, valores)

        conexao.commit()

        return redirect(url_for('listar'))
    
    # ====== PRIMEIRO PASSO ==========
    # Comando SQL para selecionar
    # somente um paciente pelo id
    comando = 'select * from paciente where id = %s'

     # Variável que irá receber todos
    # os valores das variáveis anteriores
    valor = (id,)
        
    # Executar o comando em SQL
    cursor.execute(comando, valor)

    # Atribuir um retorno para o
    # carregamento da página de
    # de criação do paciente e atribuir
    # um apelido
    paciente = cursor.fetchone()

    # Retornar o resultado carregando outra pagina
    # A segunda variável 'pacientes' é um apelido
    # atribuído para ser carregado na página e
    # realizar estruturas de programação

    return render_template('editar.html', paciente = paciente)
    
    # ====== SEGUNDO PASSO ==========
    
        
    # Comando em SQl para editar
    # o paciente
    
    # Variável que irá receber todos
    # os valores das variáveis anteriores
    
    # Executar o comando em SQL
    
    # Atribuir um retorno podendo
    # ser o redirecionamento para
    # outra página



# 5) Rota para exclusão de
# registros no banco

@app.route('/excluir/<int:id>')
def excluir(id):
    pass

    # Comando em SQl para excluir
    # o paciente
    comando = 'delete from paciente where id = %s'

    # Variável que irá receber todos
    # os valores das variáveis anteriores
    valor = (id,)
    
    # Executar o comando em SQL
    cursor.execute(comando, valor)

    # Confirmar a execução do comando no banco de dados
    conexao.commit()
    
    # Atribuir um retorno podendo ser o redirecionamento para outra página
    return redirect(url_for('listar'))



# Rota para carregar pagina de login
@app.route('/home')
def home():
    if 'id_usuario' in session:
        return render_template('index.html')
    else:
        return render_template('login.html')

# Rota de login do usuário
@app.route('/login', methods = ['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        comando = 'select id, email, senha from usuario where email = %s and senha = %s'
        valores = (email, senha)
        cursor.execute(comando, valores)
        usuario = cursor.fetchone()
        


        if usuario:
            # Criando a sessão d usuario     
            session['id_usuario'] = usuario['id']    
            return redirect(url_for('home'))
        else:
            mensagem = 'Falha no login'
            return render_template('login.html', mensagem = mensagem)
        
    return render_template('login.html')
        
    # Rota de sair do sistema e destruindo asessão
@app.route('/sair')
def sair():
    session.clear()
    return redirect(url_for('login'))


#
@app.after_request
def adicionar_cabecalho(res):
    res.cache_control.no_store = True
    return res


        # Inicialização do servidor
if __name__ == '__main__':
    app.run(debug=True)
    
