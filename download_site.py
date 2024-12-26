import os
import requests
from bs4 import BeautifulSoup

# Lista de rotas do site
rotas = [
    "architecture", "brands", "color", "design", "fashion", "fonts", "icons",
    "learning", "images", "stock", "studio", "ui_ux", "advertising", "ia-options",
    "entrepreneurship", "inovation", "marketing", "technology", "magazines",
    "news", "newsletter", "movies", "music", "photograph", "organization",
    "tool", "main", ""
]

# URL base do site
base_url = "https://tedious-software-931425.framer.app/"  # Substitua pelo site real

# Pasta para salvar os arquivos baixados
output_folder = os.getcwd()
os.makedirs(output_folder, exist_ok=True)

def save_file(content, path):
    """Salva o conteúdo no arquivo especificado."""
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

def download_html_and_css(route):
    """Baixa HTML e CSS de uma rota específica."""
    url = base_url + route
    print(f"Baixando: {url}")
    
    try:
        # Faz a requisição para a rota
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        # Salva o HTML com ajustes de nome
        if not route:  # Página inicial
            html_file = os.path.join(output_folder, "home.html")
        else:
            html_file = os.path.join(output_folder, route)

        save_file(html_content, html_file)

        # Analisa o HTML para encontrar CSS
        soup = BeautifulSoup(html_content, "html.parser")
        for link in soup.find_all("link", {"rel": "stylesheet"}):
            css_url = link.get("href")
            if css_url:
                # Resolve URLs relativas
                if not css_url.startswith("http"):
                    css_url = base_url + css_url.lstrip("/")
                print(f"  Baixando CSS: {css_url}")
                try:
                    css_response = requests.get(css_url)
                    css_response.raise_for_status()
                    css_file = os.path.join(output_folder, os.path.basename(css_url))
                    save_file(css_response.text, css_file)
                except requests.RequestException as e:
                    print(f"  Erro ao baixar CSS: {css_url} -> {e}")

    except requests.RequestException as e:
        print(f"Erro ao baixar {url}: {e}")

def update_main_html_links():
    """Atualiza os links dos botões em main.html para o padrão desejado."""
    main_html_path = os.path.join(output_folder, "main")
    
    with open(main_html_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Usando BeautifulSoup para modificar os links
    soup = BeautifulSoup(content, "html.parser")
    
    # Remove a linha <div id="__framer-badge-container"></div>
    badge_container = soup.find("div", {"id": "__framer-badge-container"})
    if badge_container:
        badge_container.decompose()  # Remove o elemento do DOM

    for button in soup.find_all("a", {"data-framer-name": "Button"}):
        href = button.get("href")
        if href:
            # Adiciona o prefixo "./" se necessário
            new_href = f"./{href}" if not href.startswith("./") else href
            
            # Remove a extensão .html se estiver presente
            if new_href.endswith(".html"):
                new_href = new_href[:-5]
            
            button["href"] = new_href
            print(f'Alterando botão: {button} para href: {new_href}')  # Exibe a alteração

    # Salva as alterações de volta no arquivo
    with open(main_html_path, "w", encoding="utf-8") as file:
        file.write(str(soup))

    # Adiciona a inclusão do script.js antes do fechamento da tag </body>
    with open(main_html_path, "a", encoding="utf-8") as file:
        file.write('\n<script src="script.js"></script>\n')

# Baixa todas as rotas
for rota in rotas:
    download_html_and_css(rota)

# Atualiza os links no main.html após baixar tudo
update_main_html_links()
