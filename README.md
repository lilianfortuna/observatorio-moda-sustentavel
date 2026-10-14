# Observatório da Moda Sustentável no Interior Paulista

Protótipo público em Streamlit, concebido para integrar resultados descritivos da investigação apresentada em 2025 e associações estatísticas do artigo de 2026. As duas análises usam a **mesma base com 336 respostas**.

## Executar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicar no Streamlit Community Cloud

1. Crie uma conta no GitHub.
2. Crie um repositório e carregue somente os arquivos desta pasta.
3. Na página do Streamlit Community Cloud, escolha **Create app** e conecte o repositório.
4. Defina `app.py` como arquivo principal e escolha um subdomínio disponível.
5. Confira a interface publicada em computador e celular, valide as informações e gere um QR Code do link definitivo.

## Proteção de dados

- Este repositório contém exclusivamente **contagens agregadas** e percentuais; a planilha original de respostas **não é incluída**.
- Os indicadores de 2025 foram obtidos de contagens simples dos campos do formulário; as categorias com menos de dez menções individuais foram reunidas sob 'Outras respostas (agrupadas)'.
- Alguns campos originais têm respostas abertas ou grafias divergentes, por isso não são usados para análise inferencial automática.
- Não compartilhar arquivos individuais, dados de cidade, carimbos de data/hora, profissões livres, marcas ou justificativas abertas sem avaliação específica de risco, consentimento e critérios éticos.
- Os quatro gráficos de 2026 são destaques percentuais extraídos do artigo revisado e **não reproduzem integralmente** as tabelas de contingência originais. Para reproduzir a análise completa, inserir tabelas de todas as categorias e respectivos denominadores depois de validação.
- Os dados devem ser interpretados como uma **amostra não probabilística por conveniência**, sem inferência para toda a população regional.

## Próximos aprimoramentos

- Incorporar imagem da nuvem de marcas do artigo após validação da figura.
- Incluir links permanentes dos artigos e DOI quando disponível.
- Rever a categorização para padronização das respostas de formulário.
- Confirmar condições de consentimento/CEP e política de privacidade antes da publicação.
- Personalizar a identidade visual com logos e retratos com autorização.
