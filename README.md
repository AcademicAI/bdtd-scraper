# bdtd-scraper
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Ferramenta para obter informações da Biblioteca Digital Brasileira de Teses e Dissertações.

## Instalação

```sh
pip install git+https://github.com/AcademicAI/bdtd-scraper.git
```

## Biblioteca Python

### Biblioteca Digital de Teses e Dissertações
#### Busca simples
```python
import bdtd_scraper.api

# Retornar 1000 registros da base
result = bdtd_scraper.api.get_search_results()
print(result)

# Retornar informações sobre um trabalho específico
info = bdtd_scraper.api.get_record("PUC_RIO-1_116b1dc174d74d0cdc7d451060e9129a")
print(info)
```

#### Parâmetros adicionais (**kwargs)

Essa ferramenta permite passar demais parâmetros usados na chamada da API da BDTD.

```python
result = bdtd_scraper.api.get_search_results(
    lookfor="covid",
    page=2,
    limit=5,
    type="AllFields",
    field=["id", "title", "authors"]
)
print(result)
```

#### Obter resultados de várias páginas
```python
results = []
for records in bdtd_scraper.api.get_all_results(lookfor="bumba meu boi", limit=100):
    results.extend(records)

print(len(results))
```

### Acessando trabalhos nos repositórios
#### Obter links de um trabalho

Buscar prováveis links de um trabalho em um repositório de uma universidade. Recebe como argumento a URL do trabalho e retorna uma lista com os links encontrados. Pode ser informado uma das URLs retornadas pelo `bdtd_scraper.api.get_search_results`.

```python
from bdtd_scraper import theses_downloader

url = 'https://doi.org/10.17771/PUCRio.acad.55901'
links = theses_downloader.get_most_probable_thesis_links(url)
for link in links:
    print(link)

# https://www.maxwell.vrac.puc-rio.br/55901/55901.PDF
```
#### Fazer download de um arquivo

Realiza o download do arquivo com o nome informado.

```python
theses_downloader.download_pdf(links[0], "example.pdf")
```
