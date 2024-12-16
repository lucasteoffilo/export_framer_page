import os
import requests
from bs4 import BeautifulSoup

def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return None

def save_page_content(path, content, base_url):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Corrigir links relativos no conteúdo HTML
    soup = BeautifulSoup(content, "html.parser")
    for tag in soup.find_all(["a", "link", "script", "img"]):
        attr = "href" if tag.name in ["a", "link"] else "src"
        if tag.has_attr(attr):
            original_link = tag[attr]
            if original_link.startswith("/") and not original_link.startswith("//"):
                tag[attr] = f"{base_url}{original_link}"
    
    fixed_content = str(soup)

    with open(path, 'w', encoding='utf-8') as file:
        file.write(fixed_content)
    print(f"Página salva em: {path}")


def main():
    base_url = "https://tedious-software-931425.framer.app"

    # Lista das rotas a serem exportadas
    routes = [
        "",
        "main",
        "architecture",
        "brands",
        "color",
        "design",
        "fashion",
        "fonts",
        "icons",
        "learning",
        "images",
        "stock",
        "studio",
        "ui_ux",
        "advertising",
        "ai",
        "entrepreneurship",
        "inovation",
        "marketing",
        "technology",
        "magazines",
        "news",
        "newsletter",
        "movies",
        "music",
        "photograph",
        "organization",
        "tool",
    ]

    # Diretório para salvar os arquivos exportados
    output_dir = "exported_pages"

    for route in routes:
        route_path = f"/{route}" if route else ""
        full_url = f"{base_url}{route_path}"
        print(f"Acessando: {full_url}")

        content = fetch_page_content(full_url)
        if content:
            # Gerar o caminho do arquivo de saída
            sanitized_route = route.replace("/", "_") or "home"
            output_path = os.path.join(output_dir, f"{sanitized_route}.html")

            # Salvar o conteúdo da página
            save_page_content(output_path, content, base_url)

if __name__ == "__main__":
    main()
