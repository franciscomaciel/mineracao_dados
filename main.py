import csv

def corrigir_tempo_resolucao(arquivo_entrada, arquivo_saida):
    with open(arquivo_entrada, 'r', newline='', encoding='utf-8') as entrada, \
            open(arquivo_saida, 'w', newline='', encoding='utf-8') as saida:

        leitor = csv.reader(entrada, delimiter=',', quotechar='"')
        escritor = csv.writer(saida, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        cabecalho = next(leitor)
        escritor.writerow(cabecalho)

        for linha in leitor:
            if len(linha) >= 11:
                # Corrige o campo TEMPO_RESOLUCAO (índices 9 e 10)
                tempo_resolucao = f'{linha[9]}.{linha[10]}'.replace(',', '.')
                linha[9] = tempo_resolucao
                linha.pop(10)

                # Escreve a linha manualmente para remover aspas apenas do campo 9
                linha_escrita = []
                for i, campo in enumerate(linha):
                    if i == 9:  # Campo TEMPO_RESOLUCAO - sem aspas
                        linha_escrita.append(campo)
                    else:
                        linha_escrita.append(f'"{campo}"')  # Demais campos com aspas

                saida.write(','.join(linha_escrita) + '\n')
            else:
                escritor.writerow(linha)  # Linhas com menos de 11 campos são escritas normalmente


def concatenar_texto_acao(arquivo_entrada, arquivo_saida):
    with open(arquivo_entrada, 'r', newline='', encoding='utf-8') as entrada, \
            open(arquivo_saida, 'w', newline='', encoding='utf-8') as saida:

        leitor = csv.reader(entrada, delimiter=',', quotechar='"')

        # Configuração especial do escritor para controlar aspas seletivamente
        escritor = csv.writer(saida, delimiter=',', quotechar='"',
                              quoting=csv.QUOTE_MINIMAL, escapechar='\\')

        cabecalho = next(leitor)
        escritor.writerow(cabecalho)

        for linha in leitor:
            if len(linha) > 10:
                # Mantém TEMPO_RESOLUCAO (campo 9) como número sem aspas
                tempo_resolucao = linha[9]

                # Concatena TEXTO_ACAO (campos 10+)
                texto_acao = ' '.join(linha[10:]).replace('"', "'").strip()

                # Reconstrói a linha com formatação seletiva
                nova_linha = linha[:9] + [tempo_resolucao, texto_acao]

                # Escreve manualmente para controle preciso das aspas
                linha_formatada = []
                for i, campo in enumerate(nova_linha):
                    if i == 9:  # TEMPO_RESOLUCAO - sem aspas
                        linha_formatada.append(str(campo))
                    else:  # Demais campos - com aspas
                        linha_formatada.append(f'"{campo}"')

                saida.write(','.join(linha_formatada) + '\n')
            else:
                escritor.writerow(linha)
# Uso
# concatenar_texto_acao('chamados_2024_corrigido.csv', 'chamados_2024_final.csv')

"""
arquivo_origem = 'chamados_2024.csv'
arquivo_destino = 'chamados_2024_tempo_resolucao_corrigido.csv'
corrigir_tempo_resolucao(arquivo_origem, arquivo_destino)

"""
arquivo_origem = 'chamados_2024_tempo_resolucao_corrigido.csv'
arquivo_destino = 'chamados_2024_final.csv'
concatenar_texto_acao(arquivo_origem,arquivo_destino)
