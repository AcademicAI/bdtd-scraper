import urllib.parse
from functools import lru_cache

import Levenshtein
import requests
from bs4 import BeautifulSoup

from .constants import HEADERS


requests.packages.urllib3.disable_warnings()  # type: ignore


def _is_downloadable(url: str) -> bool:
    """Verifica se o link é para um arquivo baixável.

    Args:
        url (str): URL do link.

    Returns:
        bool: True se o link é para um arquivo baixável, False caso contrário.
    """
    try:
        h = requests.head(
            url,
            allow_redirects=True,
            verify=False,
            timeout=5,
            headers={**HEADERS, "Referer": url, "Accept": "*/*;q=0.8"},
        )
    except requests.exceptions.RequestException:
        return False

    header = h.headers
    content_type = header.get("content-type")
    if not content_type:
        return False
    if "text" in content_type.lower():
        return False
    if "html" in content_type.lower():
        return False
    return True


@lru_cache(maxsize=100)
def _get_links(url: str) -> list[tuple[str, str]]:
    """Obtém os links de um repositório de teses e dissertações.

    São obtidos links do tipo:
        - ref: link para a página do repositório.
        - default: outros links encontrados na página.
        - embedded: link para o arquivo PDF embutido na página.

    Args:
        url (str): URL do repositório.

    Returns:
        list[tuple[str, str]]: Lista de tuplas com o tipo de link e o link.
    """
    response = requests.get(
        url,
        allow_redirects=True,
        verify=False,
        timeout=5,
        headers={"Referer": url, **HEADERS},
    )
    soup = BeautifulSoup(response.text, "html.parser")
    base_url = urllib.parse.urlparse(response.url).netloc

    # Obtém os links da página.
    links = [("ref", response.url)]
    for link in soup.find_all("a", href=True):
        current_link = urllib.parse.urljoin(response.url, link["href"])
        if base_url in current_link and current_link != response.url:
            links.append(("default", current_link))

    # Obtém o link para o arquivo PDF embutido na página. Geralmente é um elemento do tipo
    # <object> com o atributo type="application/pdf". O link para o arquivo PDF é o valor do
    # atributo data.
    if embedded := soup.find("object", {"type": "application/pdf"}):
        embedded_link = urllib.parse.urljoin(
            response.url,
            embedded["data"],
        )
        if embedded_link not in links:
            links.append(("embedded", embedded_link))

    return links


def _get_files_links(links: list[tuple[str, str]]) -> list[str]:
    """Obtém os links para os arquivos PDF.

    Geralmente, os links para os arquivos PDF são encontrados em links que contém
    "jspui", "handle" ou "bitstream" na URL.

    Args:
        links (list[tuple[str, str]]): Lista de tuplas com o tipo de link e o link.

    Returns:
        list[str]: Lista de links para os arquivos PDF.
    """
    pdf_links = set()
    for link_type, link in links:
        lower_link = link.lower()
        if link in pdf_links:
            continue
        if link_type == "embedded":
            pdf_links.add(link)
        elif (
            lower_link.endswith(".pdf")
            or "/jspui" in lower_link
            or "/handle" in lower_link
            or "/bitstream" in lower_link
        ):
            if _is_downloadable(link):
                pdf_links.add(link)
    return list(pdf_links)


def get_most_probable_thesis_links(
    url: str,
) -> list[str]:
    """Obtém os links mais prováveis para os arquivos PDF.

    Dado um repositório, obtém os links para os arquivos PDF que possuem maior similaridade
    com a URL do repositório. A similaridade é calculada utilizando a distância de Levenshtein.

    Args:
        url (str): URL do repositório.

    Returns:
        list[str]: Lista de links para os arquivos PDF.
    """

    # Obtém os links do repositório. O primeiro link é o link para a página do repositório. Os
    # demais links são links encontrados na página.
    links = _get_links(url)
    (_, repo_url), links = links[0], links[1:]

    if repo_url.lower().endswith(".pdf"):
        return [repo_url]

    # Obtém os links para os arquivos PDF. Os links para os arquivos PDF são links que terminam
    # com ".pdf" ou que contém "jspui", "handle" ou "bitstream" na URL.
    pdf_links = _get_files_links(links)

    if len(pdf_links) == 0:
        return []

    # Calcula a distância de Levenshtein entre a URL do repositório e os links para os arquivos PDF.
    # O link com maior similaridade é o mais provável para o arquivo PDF.
    levenshtein_ratios = []
    for link in pdf_links:
        base_url, _ = link.rsplit("/", 1)
        levenshtein_ratios.append(
            (Levenshtein.ratio(repo_url, base_url), link),
        )

    max_ratio = max(levenshtein_ratios, key=lambda x: x[0])
    max_ratio_links = [
        link for ratio, link in levenshtein_ratios if ratio == max_ratio[0]
    ]
    return max_ratio_links


def download_pdf(url: str, filename: str) -> None:
    """Faz o download de um arquivo PDF.

    Args:
        url (str): URL do arquivo PDF.
        filename (str): Nome do arquivo PDF.
    """
    response = requests.get(
        url,
        allow_redirects=True,
        verify=False,
        timeout=5,
        headers={"Referer": url, **HEADERS},
    )

    with open(filename, "wb") as f:
        f.write(response.content)
