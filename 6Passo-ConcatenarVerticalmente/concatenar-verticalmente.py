from PIL import Image
import os
import re

pasta_imagens = "1102-divididas-sem-bordas-do-meio"  # Altere para "." caso o script rode dentro da própria pasta das imagens
pasta_saida = "."
os.makedirs(pasta_saida, exist_ok=True)

# Função para extrair o número da página e ordenar numericamente
def get_sort_key(nome_arquivo):
    match = re.search(r'pagina_enem_(\d+)_', nome_arquivo)
    return int(match.group(1)) if match else 0

# Filtrar e ordenar apenas os arquivos que terminam com '_esquerda.png'
arquivos = [f for f in os.listdir(pasta_imagens) if f.endswith('_esquerda.png')]
arquivos.sort(key=get_sort_key)

# Abrir todas as imagens filtradas na ordem correta
imagens = []
for arquivo in arquivos:
    caminho = os.path.join(pasta_imagens, arquivo)
    imagens.append(Image.open(caminho))
    print(f"Adicionando: {arquivo}")

# Encontrar a largura máxima entre as imagens esquerdas
largura_max = max(img.width for img in imagens)

# Concatenar verticalmente
altura_total = sum(img.height for img in imagens)
imagem_final = Image.new('RGB', (largura_max, altura_total))

y = 0
for img in imagens:
    imagem_final.paste(img, (0, y))
    y += img.height

# Salvar o resultado
imagem_final.save(os.path.join(pasta_saida, '1102_esquerda_concatenadas_verticalmente.png'))
print("Imagens da esquerda concatenadas com sucesso!")
print(f"Ordem dos arquivos: {arquivos}")