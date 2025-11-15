// Arquivo: cria_turmas_vazio.c

#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *arquivo;
    const char *nome_arquivo = "turmas.csv"; 
    
    arquivo = fopen(nome_arquivo, "w");

    if (arquivo == NULL) {
        printf("ERRO: Nao foi possivel abrir o arquivo %s.\n", nome_arquivo);
        return 1;
    }

    // Cabecalho e exemplos iniciais
    fprintf(arquivo, "ID_Turma,Nome_Turma\n");
    fprintf(arquivo, "T001,Engenharia de Software - 3o Semestre\n");
    fprintf(arquivo, "T002,Redes de Computadores - 1o Semestre\n");

    fclose(arquivo);
    printf("Arquivo de Turmas criado: %s\n", nome_arquivo);
    
    return 0;
}