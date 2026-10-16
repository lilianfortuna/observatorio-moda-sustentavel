# Observatório da Moda Sustentável no Interior Paulista — versão 5.0

Site Streamlit público com dados **exclusivamente agregados** de uma base de 336 respostas e análises científicas descritivas (2025) e associativas (2026).

## O que foi integrado
- 18 indicadores descritivos e quatro associações estatísticas, preservados da versão 4.0;
- duas visualizações separadas: marcas mencionadas (extração exploratória) e motivações de consumo (imagem do painel de 2025);
- contextualização da continuidade dos estudos e crédito ao projeto de 2025.

**Não foram incorporados** dados individuais (`moda.xlsx`, `moda_lilian.csv`), o mapa granular por cidade, nem o antigo índice experimental de circularidade (a codificação original utiliza indevidamente a variável renda).

## Instalação / publicação
Arquivos na raiz do repositório: `app.py`, `requirements.txt`, `README.md`, pasta `data/` com dois JSON agregados e pasta `assets/` com `motivacoes_2025.jpg`. No Streamlit Community Cloud, apontar para `app.py` na branch `main`.

## Créditos e uso
A nuvem histórica de motivações foi obtida do repositório do painel de 2025, com contribuição de Ronnie Marinho. Confirmar autorização e condições de reutilização da imagem antes de divulgação definitiva. Resultados e figuras estatísticas pertencem aos autores dos estudos citados no Observatório. O aplicativo não dispõe ainda de licença aberta explícita.

## Validação
A compilação sintática foi verificada. Antes da publicação definitiva, revisar os rótulos originais, o algoritmo de identificação de marcas e verificar as seções no aplicativo em execução. A amostra por conveniência não permite generalização populacional nem inferência causal.
