// Arquivo: cria_dados_vazio.c

#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *arquivo;
    const char *nome_arquivo = "dados_alunos.csv"; 
    
    // Abre o arquivo no modo de escrita ("w")
    arquivo = fopen(nome_arquivo, "w");

    if (arquivo == NULL) {
        printf("ERRO: Nao foi possivel abrir o arquivo %s.\n", nome_arquivo);
        return 1;
    }

    // Escreve apenas o cabecalho
    fprintf(arquivo, "Nome,Matricula,Nota1,Nota2\n");

    fclose(arquivo);
    printf("Arquivo de dados criado: %s\n", nome_arquivo);
    
    return 0;
}