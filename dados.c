// Arquivo: cria_dados_vazio.c

#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *arquivo;
    const char *nome_arquivo = "dados_alunos.csv"; 
    
    arquivo = fopen(nome_arquivo, "w");

    if (arquivo == NULL) {
        printf("ERRO: Nao foi possivel abrir o arquivo %s.\n", nome_arquivo);
        return 1;
    }

    // Cabecalho: Agora inclui o ID da Turma
    fprintf(arquivo, "ID_Turma,Nome,Matricula,Nota1,Nota2\n"); 

    fclose(arquivo);
    printf("Arquivo de Alunos criado: %s\n", nome_arquivo);
    
    return 0;
}