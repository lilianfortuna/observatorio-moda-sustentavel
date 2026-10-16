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


## Versão 6.0 — página inicial
Nova apresentação visual e científica, indicadores contextualizados, explicação de base única e orientação de navegação. As demais seções, bases agregadas e figuras estão preservadas da v5.


## Atualização 6.1 — Equipe e publicações
Inclui retrato fornecido e autorizado pela pesquisadora, minicurrículo, identificação dos coautores, DOI da publicação de 2025 e situação editorial de 2026.


## Versão 6.2 — desempenho
- Leitura dos arquivos agregados com cache do Streamlit (`st.cache_data`).
- Cache para geração dos gráficos Plotly utilizados repetidamente.
- Importação de Plotly apenas nas páginas que utilizam gráficos.
- Redução de tamanho da fotografia para carregamento mais rápido, preservando sua aparência e enquadramento.
- Dados e resultados científicos inalterados.

**Limitação:** a primeira abertura após repouso (cold start) do Streamlit Community Cloud depende da infraestrutura de hospedagem e pode continuar demorando. Teste o tempo na primeira abertura separadamente do tempo entre seleções de gráficos.

**Reversão:** em caso de problema, use o histórico de commits do GitHub para reverter a alteração para a versão anterior.
