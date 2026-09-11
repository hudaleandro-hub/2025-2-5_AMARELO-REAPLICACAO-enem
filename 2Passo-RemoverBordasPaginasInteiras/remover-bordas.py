"""
Propósito: remover as bordas externas das páginas (distinguindo pares e ímpares)
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026

OBS1: puxe a pasta "imagens-convertidas" do passo 1 para essa pasta do passo 2

OBS2: abra a imagem no GIMP e conte pixels para saber quanto de borda tem que cortar.

OBS3: valores de corte ajustados para diferenciar páginas pares e ímpares.

OBS4: tenha em mente desde já que você vai usar as imagens futuramente, então corte pensando na melhor maneira para executar todos os 12 passos

OBS5: execute o código, e abra as imagens para conferir se as bordas foram removidas corretamente. Se não, ajuste os valores de corte e execute novamente.
"""

from PIL import Image
import os
import re

pasta_imagens = "imagens-convertidas"
pasta_saida = "sem-bordas-externas"

os.makedirs(pasta_saida, exist_ok=True)

for nome_arquivo in os.listdir(pasta_imagens):
    if nome_arquivo.lower().endswith(".png"):
        caminho_entrada = os.path.join(pasta_imagens, nome_arquivo)
        imagem = Image.open(caminho_entrada)

        largura, altura = imagem.size

        # Extrai os dígitos numéricos do nome do arquivo (ex: "pagina_enem_10.png" -> 10)
        numeros = re.findall(r'\d+', nome_arquivo)
        if numeros:
            numero_pagina = int(numeros[-1])
            
            # Verifica se a página é par ou ímpar
            if numero_pagina % 2 == 0:
                # Páginas pares
                caixa_corte = (272, 442, largura - 240, altura - 290)
            else:
                # Páginas ímpares
                caixa_corte = (242, 442, largura - 270, altura - 290)
        else:
            # Fallback caso não encontre número no nome do arquivo
            caixa_corte = (272, 442, largura - 240, altura - 290)

        imagem_cortada = imagem.crop(caixa_corte)

        caminho_saida = os.path.join(pasta_saida, nome_arquivo)
        imagem_cortada.save(caminho_saida)

print("Recorte das bordas concluído.")