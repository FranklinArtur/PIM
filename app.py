# Arquivo: app.py (COMPLETO E FINAL)

from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)
NOME_ARQUIVO_ALUNOS = 'dados_alunos.csv'
NOME_ARQUIVO_TURMAS = 'turmas.csv'

# --- Funções de Manipulação de Arquivo e Cálculo ---

def ler_turmas():
    """Lê o arquivo turmas.csv e retorna um dicionario {ID_Turma: Nome_Turma}."""
    turmas = {}
    if not os.path.exists(NOME_ARQUIVO_TURMAS):
        return turmas
        
    try:
        with open(NOME_ARQUIVO_TURMAS, 'r', newline='', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo)
            next(leitor) # Pula o cabecalho
            for linha in leitor:
                if len(linha) >= 2 and linha[0].strip():
                    turmas[linha[0]] = linha[1] 
    except Exception as e:
        print(f"Erro ao ler turmas: {e}")
    return turmas


def ler_dados():
    """Lê o arquivo de alunos, calcula a media e associa o Nome da Turma."""
    turmas = ler_turmas()
    alunos_com_media = []
    # O cabecalho para EXIBICAO
    cabecalho = ["Turma", "Nome", "Matricula", "Nota1", "Nota2", "Media"] 

    if not os.path.exists(NOME_ARQUIVO_ALUNOS):
        return cabecalho, [["ERRO:", "Arquivo de alunos nao encontrado!", "", "", "", ""]]

    try:
        with open(NOME_ARQUIVO_ALUNOS, 'r', newline='', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo)
            next(leitor) # Pula o cabecalho original do CSV

            for linha in leitor:
                if len(linha) >= 5 and any(field.strip() for field in linha): 
                    
                    id_turma = linha[0]
                    nome_turma = turmas.get(id_turma, "Turma Não Encontrada") 

                    # Dados do aluno no CSV: [ID_Turma, Nome, Matricula, N1, N2]
                    dados_aluno_csv = linha[1:] 
                    
                    try:
                        # As notas sao o 3o e 4o elemento da lista dados_aluno_csv (Indices 2 e 3)
                        nota1 = float(dados_aluno_csv[2])
                        nota2 = float(dados_aluno_csv[3])
                        
                        media = (nota1 + nota2) / 2
                        media_str = f"{media:.2f}"
                        
                    except (ValueError, IndexError):
                        media_str = "ERRO"
                        
                    # Linha final para exibicao: [Nome_Turma, Nome, Matricula, N1, N2, Media]
                    linha_final = [nome_turma] + dados_aluno_csv + [media_str]
                    alunos_com_media.append(linha_final)
                        
    except Exception as e:
        print(f"Erro ao ler alunos: {e}")
        return cabecalho, [["ERRO:", "Problema na leitura do arquivo CSV.", "", "", "", ""]]

    return cabecalho, alunos_com_media


def adicionar_aluno_csv(dados):
    """Anexa os novos dados ao dados_alunos.csv."""
    try:
        # Linha salva: ID_Turma, Nome, Matricula, Nota1, Nota2
        with open(NOME_ARQUIVO_ALUNOS, 'a', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(dados)
        return True
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")
        return False


def adicionar_turma_csv(nome_turma):
    """Gera um ID sequencial e anexa a nova turma ao turmas.csv."""
    try:
        turmas_existentes = ler_turmas()
        
        # Gera o proximo ID (T001, T002, etc.)
        novo_num = 1
        if turmas_existentes:
            # Encontra o maior numero de ID existente
            ids_numericos = [int(k[1:]) for k in turmas_existentes.keys() if k.startswith('T') and k[1:].isdigit()]
            if ids_numericos:
                 ultimo_num = max(ids_numericos)
                 novo_num = ultimo_num + 1

        novo_id = f"T{novo_num:03d}" 

        # Salva a nova linha no CSV
        with open(NOME_ARQUIVO_TURMAS, 'a', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow([novo_id, nome_turma])
        
        return True
    except Exception as e:
        print(f"Erro ao salvar a nova turma: {e}")
        return False


def excluir_aluno_csv(matricula_aluno):
    """Reescreve o CSV sem o aluno que corresponde a matricula informada."""
    alunos_mantidos = []
    
    # 1. Leitura de todos os alunos, exceto o que será excluído
    try:
        with open(NOME_ARQUIVO_ALUNOS, 'r', newline='', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo)
            cabecalho = next(leitor)
            
            for linha in leitor:
                # O campo Matricula esta no indice 2 do CSV original
                # CSV: [ID_Turma, Nome, Matricula, Nota1, Nota2]
                if len(linha) > 2 and linha[2] != matricula_aluno:
                    alunos_mantidos.append(linha)
    except Exception as e:
        print(f"Erro ao ler alunos para exclusao: {e}")
        return False

    # 2. Reescreve o arquivo com os alunos restantes (mantidos)
    try:
        with open(NOME_ARQUIVO_ALUNOS, 'w', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(cabecalho)
            escritor.writerows(alunos_mantidos)
        return True
    except Exception as e:
        print(f"Erro ao reescrever CSV apos exclusao: {e}")
        return False


# --- Rotas da Aplicação ---

@app.route('/')
def index():
    # Rota principal com BUSCA
    termo_busca = request.args.get('q', '').lower()
    
    cabecalho, todos_alunos = ler_dados()
    
    alunos_filtrados = []
    
    # FILTRA os alunos (Corrigido para usar o indice 1, que é o Nome)
    if termo_busca:
        for aluno in todos_alunos:
            # O NOME do aluno na lista de EXIBIÇÃO está no índice 1
            if len(aluno) > 1:
                nome_aluno = aluno[1].lower()
                
                if termo_busca in nome_aluno:
                    alunos_filtrados.append(aluno)
    else:
        alunos_filtrados = todos_alunos
        
    return render_template('tabela_aluno.html', 
                           cabecalho=cabecalho, 
                           alunos=alunos_filtrados,
                           termo_busca_atual=termo_busca)

@app.route('/adicionar')
def formulario_adicionar():
    # Rota para exibir o formulario de aluno. Envia as turmas para o template.
    turmas = ler_turmas()
    return render_template('formulario_aluno.html', turmas=turmas)

@app.route('/salvar', methods=['POST'])
def salvar_aluno():
    # Rota que processa o envio do formulario de aluno
    id_turma = request.form['id_turma']
    nome = request.form['nome']
    matricula = request.form['matricula']
    nota1 = request.form['nota1']
    nota2 = request.form['nota2']
    
    # Dados que serao gravados no CSV: [ID_Turma, Nome, Matricula, Nota1, Nota2]
    dados_aluno_para_csv = [id_turma, nome, matricula, nota1, nota2]
    
    if adicionar_aluno_csv(dados_aluno_para_csv):
        return redirect(url_for('index'))
    else:
        return "Erro ao salvar o aluno!", 500

@app.route('/cadastrar_turma')
def formulario_cadastrar_turma():
    """Exibe o formulario simples para cadastrar uma nova turma."""
    return render_template('formulario_turma.html')

@app.route('/salvar_turma', methods=['POST'])
def salvar_turma():
    """Processa o envio do formulario de cadastro de turma."""
    nome_turma = request.form['nome_turma']
    
    if adicionar_turma_csv(nome_turma):
        # Redireciona de volta para a tela de adicionar aluno (com a nova turma disponivel)
        return redirect(url_for('formulario_adicionar'))
    else:
        return "Erro ao salvar a nova turma!", 500

@app.route('/apagar/<matricula>')
def apagar_aluno(matricula):
    """Processa a exclusao do aluno pela matricula recebida na URL."""
    if excluir_aluno_csv(matricula):
        # Redireciona de volta para a tabela principal
        return redirect(url_for('index'))
    else:
        return "Erro ao excluir o aluno.", 500


if __name__ == '__main__':
    # Roda o servidor acessivel em sua LAN ou Radmin VPN
    print("Servidor Flask inicializado. Acesse pela URL de rede local ou Radmin VPN.")
    app.run(debug=True, host='0.0.0.0')