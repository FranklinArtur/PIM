# Arquivo: app.py (Modificado para calcular a média)

from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)
NOME_ARQUIVO = 'dados_alunos.csv'

# --- Funções de Manipulação de Arquivo e Cálculo ---

def ler_dados():
    alunos_com_media = []
    # Incluindo a coluna 'Media' no cabecalho padrao
    cabecalho = ["Nome", "Matricula", "Nota1", "Nota2", "Media"] 

    if not os.path.exists(NOME_ARQUIVO):
        return cabecalho, [["ERRO:", "Arquivo de dados nao encontrado!", "", "", ""]]

    try:
        with open(NOME_ARQUIVO, 'r', newline='', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo)
            
            # Tenta ler o cabecalho, mas garante que o cabecalho de retorno inclui 'Media'
            try:
                next(leitor) # Pula a linha do cabecalho original (sem 'Media')
            except StopIteration:
                pass 

            # Le as linhas de dados
            for linha in leitor:
                if len(linha) >= 4 and any(field.strip() for field in linha):
                    
                    # 1. Tenta extrair as notas
                    try:
                        nota1 = float(linha[2])
                        nota2 = float(linha[3])
                        
                        # 2. CALCULA A MÉDIA (Requisito da atividade)
                        media = (nota1 + nota2) / 2
                        
                        # 3. Cria a linha de dados final (incluindo a media formatada)
                        linha_final = linha + [f"{media:.2f}"]
                        alunos_com_media.append(linha_final)
                        
                    except ValueError:
                        # Se as notas nao forem numeros
                        alunos_com_media.append(linha + ["ERRO NOTA"])
                        
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return cabecalho, [["ERRO:", "Problema na leitura do arquivo CSV.", "", "", ""]]

    return cabecalho, alunos_com_media


def adicionar_aluno_csv(dados):
    # Função inalterada: apenas anexa a nova linha ao CSV
    try:
        with open(NOME_ARQUIVO, 'a', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(dados)
        return True
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")
        return False


# --- Rotas da Aplicação ---

@app.route('/')
def index():
    # Rota principal: Exibe a tabela com os dados e a média
    cabecalho, dados_alunos = ler_dados()
    # Usando o nome do arquivo que voce tem: 'tabela_aluno.html'
    return render_template('tabela_aluno.html', 
                           cabecalho=cabecalho, 
                           alunos=dados_alunos)

@app.route('/adicionar')
def formulario_adicionar():
    # Rota: Exibe o formulario para adicionar um novo aluno
    # Usando o nome do arquivo que voce tem: 'formulario_aluno.html'
    return render_template('formulario_aluno.html')

@app.route('/salvar', methods=['POST'])
def salvar_aluno():
    # Rota: Processa o envio do formulario
    nome = request.form['nome']
    matricula = request.form['matricula']
    nota1 = request.form['nota1']
    nota2 = request.form['nota2']
    
    dados_aluno = [nome, matricula, nota1, nota2]
    
    if adicionar_aluno_csv(dados_aluno):
        return redirect(url_for('index'))
    else:
        return "Erro ao salvar o aluno!", 500


if __name__ == '__main__':
    print(f"Flask rodando. Acesse: http://127.0.0.1:5000/")
    app.run(debug=True)