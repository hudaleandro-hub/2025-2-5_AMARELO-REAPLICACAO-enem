"""
Propósito: Dividir as questões por padrão. Observa-se que ao início de cada questão tem uma faixa de alguma cor, que é o padrão de início de cada questão
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026

OBS1: puxe a imagem "colunas_concatenadas_verticalmente.png" do passo 6 para essa pasta do passo 7

OBS2: puxe a pasta "inteiras" do passo 5 para essa pasta do passo 7

OBS3: este código foi originalmente preparado para percorrer cada pixel de cima para baixo, analizando o penúltimo pixel da direita (linha 55), procurando por um padrão visual vertical de 10 pixels RGB 0-255 (64, 193, 243), seguido de 7 pixels RGB 0-255 (179, 230, 250), 4 px RGB 0-255 (64, 193, 243) e 8 px RGB 0-255 (179, 230, 250). Quando encontrava esse padrão, cortava-se 13 pixels acima de começar o padrão (linha 71).

OBS4: tendo isso em mente, use o GIMP para identificar qual é o padrão visual da sua prova (que indica o início de cada questão), quantos pixels acima do padrão visual você precisa cortar, e também qual pixel é melhor percorrer para procurar por essa faixa. SEJA CRÍTICO(A)!

OBS5: em algumas situações, o pixel procurado é a mesma cor de uma imagem ou letra. Nesses casos, você pode pedir para percorrer uma faixa de determinada altura e largura e determinada cor, e não apenas um pixel. Isso vai depender do padrão visual da sua prova.

OBS6: além disso, em algumas situações, o padrão visual varia um pixel ou outro. Por isso, é interessante considerar uma margem de erro de 3 pixels para mais e 3 pixels para menos em cada uma das faixas do seu padrão visual.

OBS6: use IA para mudar minimamente o código a fim de cortar sua imagem seguindo o padrão visual vertical da sua prova, qual pixel percorrer, qual cor RGB 0-255 procurar, quantos pixels acima do padrão visual cortar, e se necessário, percorrer uma faixa de determinada altura e largura e determinada cor, e não apenas um pixel.

OBS7: rode esse código para cada imagem que você precisa cortar. Atualize as linhas 138 e 139 para identificar a imagem e atualize o nome da pasta de saída também

OBS8: execute o código, e abra as imagens para conferir se as questões foram divididas corretamente. Se não, ajuste os valores de corte e execute novamente.
"""
from PIL import Image
import os

def converter_cor_gimp_para_rgb(gimp_r, gimp_g, gimp_b):
    """
    Converte valores do GIMP (0-100) para RGB (0-255)
    """
    r = int((gimp_r / 100) * 255)
    g = int((gimp_g / 100) * 255)
    b = int((gimp_b / 100) * 255)
    return (r, g, b)

def encontrar_faixa_cinza(imagem, cor_alvo, tolerancia=15, altura_busca=28, margem_erro=3):
    """
    Encontra posições onde há uma faixa horizontal cinza nos últimos 2 pixels da direita.
    A altura da faixa pode variar de (altura_busca - margem_erro) até (altura_busca + margem_erro).
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    
    # Colunas a serem verificadas (último e penúltimo pixel da direita)
    colunas_verificacao = [largura - 1, largura - 2]
    
    # Percorre a imagem de cima para baixo
    y = 0
    while y < altura - (altura_busca - margem_erro):
        
        # Tenta encontrar a faixa cinza em uma das duas colunas da borda direita
        faixa_encontrada = False
        altura_real_faixa = 0
        
        for coluna in colunas_verificacao:
            # Verifica o início de uma possível faixa
            pixel_inicio = pixels[coluna, y]
            if len(pixel_inicio) == 4:  # RGBA
                r, g, b, a = pixel_inicio
            else:  # RGB
                r, g, b = pixel_inicio[:3]
                
            # Se a cor do pixel inicial não bater com a cor alvo, vai para a próxima coluna
            if (abs(r - cor_alvo[0]) > tolerancia or 
                abs(g - cor_alvo[1]) > tolerancia or 
                abs(b - cor_alvo[2]) > tolerancia):
                continue

            # Verifica a continuidade da faixa com margem de erro
            # A faixa deve ter entre 25 e 31 pixels (28 +/- 3)
            for dy in range(1, altura_busca + margem_erro + 1):
                if y + dy >= altura:
                    break
                    
                pixel_atual = pixels[coluna, y + dy]
                if len(pixel_atual) == 4:
                    r, g, b, a = pixel_atual
                else:
                    r, g, b = pixel_atual[:3]
                
                if (abs(r - cor_alvo[0]) <= tolerancia and 
                    abs(g - cor_alvo[1]) <= tolerancia and 
                    abs(b - cor_alvo[2]) <= tolerancia):
                    altura_real_faixa += 1
                else:
                    break # A cor mudou, encerra a contagem dessa faixa
            
            # Verifica se a altura real encontrada está dentro da margem de erro permitida (25 a 31 pixels)
            if altura_busca - margem_erro <= altura_real_faixa <= altura_busca + margem_erro:
                faixa_encontrada = True
                break # Encontrou uma faixa válida em uma das colunas, pode parar de verificar
        
        if faixa_encontrada:
            # Corta 8 pixels ACIMA do padrão visual
            posicao_corte = y - 8
            if posicao_corte < 0:
                posicao_corte = 0
                
            posicoes_corte.append(posicao_corte)
            print(f"Faixa cinza encontrada começando em y={y} (altura={altura_real_faixa}px), cortando em y={posicao_corte}")
            
            # Pula a faixa inteira e mais um pouco para evitar detecções duplicadas
            y += altura_real_faixa + 5
        else:
            y += 1
    
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_alvo):
    """
    Divide a imagem verticalmente cortando ANTES das faixas
    """
    # Abre a imagem
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    print(f"Buscando faixa cinza RGB {cor_alvo} com altura de 28px (+/- 3px)")
    
    # Encontra as posições das faixas cinzas
    posicoes_corte = encontrar_faixa_cinza(imagem, cor_alvo)
    
    if not posicoes_corte:
        print("Nenhuma faixa cinza encontrada na imagem!")
        return
    
    print(f"Encontradas {len(posicoes_corte)} faixas cinzas para corte")
    
    # Cria a pasta de saída se não existir
    os.makedirs(pasta_saida, exist_ok=True)
    
    # Corta as seções da imagem
    posicao_anterior = 0
    
    for i, posicao_corte in enumerate(posicoes_corte):
        # Garantir que a posição de corte é válida e maior que a anterior
        if posicao_corte <= posicao_anterior:
            continue
            
        # Corta a seção ANTES da faixa cinza (do início anterior até o início da faixa)
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        # Salva a imagem cortada
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        # A próxima seção começa logo após a faixa cinza (que tem no mínimo 25px, mas usamos o padrão 28 + margem superior)
        # Para garantir que não pegue resquícios da faixa, pulamos 32 pixels (28+3 + 1 de segurança)
        posicao_anterior = posicao_corte + 8 + (28 + 3) 
    
    # Corta a seção final (após a última faixa cinza)
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    # --- ATUALIZE AQUI OS CAMINHOS ---
    caminho_imagem = "colunas_concatenadas_verticalmente.png"   # Substitua pelo caminho da sua imagem
    pasta_saida = "colunas"            # Substitua pelo nome da pasta de saída desejada
    # ----------------------------------

    # Cor do GIMP convertida para RGB (0-255): Cinza claro da faixa (GIMP: 82, 82.4, 83.1)
    cor_do_padrao = converter_cor_gimp_para_rgb(82.0, 82.4, 83.1) 
    print(f"Cor alvo convertida: RGB{cor_do_padrao}")
    
    # Executa a divisão
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_do_padrao)
    
    print("Divisão concluída!")