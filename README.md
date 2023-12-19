# rn_newsletter
Newsletter feita em python.

Tem como objetivo capturar as principais noticias diariamente dos sites:
    -https://g1.globo.com/
    -https://www.uol.com.br/
    -https://www.cnnbrasil.com.br/
    -https://www.terra.com.br/noticias/

    pegando 3 noticias de cada site, ou seja 12 noticias por dia.

-Etapas:
    ->Acessar os sites com o request.get e obter o conteudo do site. Caso não funcione utilizar o selenium e depois pegar o conteudo da pagina.
    ->Tratar o conteudo de cada site com o beautifulSoup e extrair as noticias.

