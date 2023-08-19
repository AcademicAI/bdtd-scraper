# bdtd-scraper
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Ferramenta para obter informações da Biblioteca Digital Brasileira de Teses e Dissertações

## Instalação

```sh
pip install git+https://github.com/AcademicAI/bdtd-scraper.git
```

## Biblioteca Python

### Busca simples
```python
import bdtd_scraper.api

# Retornar 1000 registros da base
result = bdtd_scraper.api.get_search_results()
print(result)

# Retornar informações sobre um trabalho específico
info = bdtd.api.get_record("P_RS_18810defd4deaf1d666c9c497b91d65f")
```

### Parâmetros adicionais (**kwargs)

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

### Obter resultados de várias páginas
```python
import bdtd_scraper.api

results = []
for records in bdtd_scraper.api.get_all_results(lookfor="bumba meu boi", limit=100):
    results.extend(records)

print(len(results))
```
