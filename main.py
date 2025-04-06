import csv

def corrigir_tempo_resolucao(arquivo_entrada, arquivo_saida):
    with open(arquivo_entrada, 'r', newline='', encoding='utf-8') as entrada, \
         open(arquivo_saida, 'w', newline='', encoding='utf-8') as saida:

        leitor = csv.reader(entrada, delimiter=',', quotechar='"')
        escritor = csv.writer(saida, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        cabecalho = next(leitor)
        escritor.writerow(cabecalho)

        for linha in leitor:
            # Verifica se a linha tem pelo menos 11 campos
            if len(linha) >= 11:
                # Corrige o campo TEMPO_RESOLUCAO (índices 9 e 10)
                # Combina os valores dos índices 9 e 10, substitui a vírgula por ponto e armazena em tempo_resolucao
                tempo_resolucao = f'{linha[9]}.{linha[10]}'.replace(',', '.')
                # Atualiza o índice 9 com o valor corrigido
                linha[9] = tempo_resolucao
                # Remove o índice 10
                linha.pop(10)
            escritor.writerow(linha)

# Nomes dos arquivos
arquivo_original = 'chamados_2024.csv'
arquivo_corrigido = 'chamados_2024_corrigido.csv'

# Executar a correção
corrigir_tempo_resolucao(arquivo_original, arquivo_corrigido)