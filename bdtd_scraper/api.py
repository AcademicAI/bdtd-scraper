r"""Módulo com funções para acessar a API da BDTD.

A API da BDTD é uma API RESTful que retorna os resultados em JSON.

Exemplo de uso:

    >>> from bdtd_scraper import api
    >>> api.get_search_results(page=1, limit=1, lookfor="covid")
    {'resultCount': 4153,
    'records': [{'id': 'P_RS_18810defd4deaf1d666c9c497b91d65f',
    'title': 'Viol?ncia contra as mulheres no contexto da pandemia : rompendo o sil?ncio',
    'authors': {'primary': {'Concatto, Cristina Schimitt': {'profile': [['NA']]}}},
    'subjectsPOR': [['Viol?ncia de G?nero'],
        ['Viol?ncia Dom?stica e Intrafamiliar'],
        ['Servi?o Social'],
        ['G?nero'],
        ['Gramado/RS'],
        ['Gender Violence'],
        ['Domestic and Intrafamilial Violence'],
        ['Social Work'],
        ['Gender'],
        ['CIENCIAS SOCIAIS APLICADAS::SERVICO SOCIAL']],
    'institutions': ['PUC_RS'],
    'types': ['masterThesis'],
    'accesslevel': 'openAccess',
    'publicationDates': ['2023'],
    'urls': ['https://tede2.pucrs.br/tede2/handle/tede/10604'],
    'formats': ['masterThesis'],
    'languages': ['por']}],
    'status': 'OK'}

    >>> api.get_record("P_RS_18810defd4deaf1d666c9c497b91d65f")
    {'resultCount': 1,
    'records': [{'id': 'P_RS_18810defd4deaf1d666c9c497b91d65f',
    'title': 'Viol?ncia contra as mulheres no contexto da pandemia : rompendo o sil?ncio',
    'authors': {'primary': {'Concatto, Cristina Schimitt': {'profile': [['NA']]}}},
    'subjectsPOR': [['Viol?ncia de G?nero'],
        ['Viol?ncia Dom?stica e Intrafamiliar'],
        ['Servi?o Social'],
        ['G?nero'],
        ['Gramado/RS'],
        ['Gender Violence'],
        ['Domestic and Intrafamilial Violence'],
        ['Social Work'],
        ['Gender'],
        ['CIENCIAS SOCIAIS APLICADAS::SERVICO SOCIAL']],
    'institutions': ['PUC_RS'],
    'types': ['masterThesis'],
    'accesslevel': 'openAccess',
    'publicationDates': ['2023'],
    'urls': ['https://tede2.pucrs.br/tede2/handle/tede/10604'],
    'formats': ['masterThesis'],
    'languages': ['por']}],
    'status': 'OK'}
"""
import functools
import urllib.parse
from typing import Generator

import requests

from bdtd_scraper.constants import ENDPOINTS


@functools.lru_cache(maxsize=128)
def requests_get(url):
    """Wrapper para requests.get que faz cache dos resultados."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_search_results(
    page: int = 1,
    **kwargs,
) -> dict:
    """Retorna os resultados da busca na BDTD.

    Args:
        page (int, optional): Número da página de resultados. Defaults to 1.

    Returns:
        dict: Dicionário com os resultados da busca.
    """

    default_params = ENDPOINTS["search"]["params"]
    params: dict = {
        "page": page,
        **default_params,  # type: ignore
    }

    for key, value in kwargs.items():
        if isinstance(value, list):
            params[key + "[]"] = value
        else:
            params[key] = value

    url = f"{ENDPOINTS['search']['url']}?{urllib.parse.urlencode(params, doseq=True)}"
    return requests_get(url)


def get_record(id: str, **kwargs) -> dict:
    """Retorna os metadados de um registro da BDTD.

    Args:
        id (str): ID do registro na BDTD.

    Returns:
        dict: Dicionário com os metadados do registro.
    """
    default_params = ENDPOINTS["record"]["params"]
    params = {
        "id": id,
        **default_params,  # type: ignore
    }

    for key, value in kwargs.items():
        if isinstance(value, list):
            params[key + "[]"] = str(value)
        else:
            params[key] = value
    url = f"{ENDPOINTS['record']['url']}?{urllib.parse.urlencode(params, doseq=True)}"
    return requests_get(url)


def get_all_results(**kwargs) -> Generator:
    """Retorna todos os resultados da busca na BDTD.

    Args:
        page (int, optional): Número da página de resultados. Defaults to 1.

    Returns:
        dict: Dicionário com os resultados da busca.
    """
    page = 1
    response = get_search_results(page=page, **kwargs)
    limit = kwargs.get("limit", ENDPOINTS["search"]["params"]["limit"])  # type: ignore
    n_pages = -(response["resultCount"] // -limit)
    while page <= n_pages:
        yield response["records"]
        page += 1
        response = get_search_results(page=page, **kwargs)
