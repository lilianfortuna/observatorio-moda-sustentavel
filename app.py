"""Observatório da Moda Sustentável no Interior Paulista — protótipo científico público.
Somente dados agregados integram esta distribuição.
"""
import json
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).parent
st.set_page_config(page_title='Observatório da Moda Sustentável', page_icon='🌿', layout='wide', initial_sidebar_state='expanded')
st.markdown('''<style>
:root {--verde:#347D70;--terracota:#C77255;--azul:#356A80;--mostarda:#D2A34E;--ameixa:#8F7393}
.block-container{padding-top:2rem;max-width:1180px}
h1,h2,h3{color:#285D51 !important}
h1{letter-spacing:-.025em}
div[data-testid="stMetric"]{background:#FAF8F4;border:1px solid #EAE4DA;border-radius:15px;padding:1rem}
[data-testid="stSidebar"]{background:#F7F5F0}
.note{background:#F7F5F0;padding:18px 20px;border-left:5px solid #347D70;border-radius:9px;line-height:1.65}
.subtitle{color:#61736D;font-size:1.08rem}
.section-kicker{color:#C77255;font-size:.79rem;letter-spacing:.12em;font-weight:750;text-transform:uppercase}
@media (max-width: 640px) {
  .block-container{padding:1.0rem .85rem 2rem;max-width:100%}
  h1{font-size:1.75rem!important;line-height:1.18!important}
  h2{font-size:1.4rem!important}
  h3{font-size:1.15rem!important}
  .note{padding:12px 14px;font-size:.94rem}
  .subtitle{font-size:.96rem}
  [data-testid='stMetric']{padding:.65rem!important}
  [data-testid='stMetricValue']{font-size:1.45rem!important}
  [data-testid='stPlotlyChart']{max-width:100%;overflow:hidden}
  [data-testid='stPlotlyChart'] .modebar{display:none!important}
  [data-testid='stDataFrame']{max-width:100%;}
}

</style>''',unsafe_allow_html=True)
PLOT_CONFIG={'displayModeBar':False,'responsive':True,'scrollZoom':False}

def brief_label(label):
    # Exibir nomes curtos nos eixos; o nome integral permanece na tabela e no tooltip.
    replacements={
       'Ensino Superior completo':'Superior completo',
       'Ensino Superior incompleto':'Superior incompleto',
       'Ensino Médio completo':'Médio completo',
       'Especialização (lato sensu)':'Especialização',
       'Outras respostas (agrupadas)':'Outras respostas',
       'Não tem certeza':'Não tem certeza',
       'Conhece/comprou':'Conhece/comprou',
       'Relaciona escolhas aos ODS':'Relaciona aos ODS',
    }
    label=str(label)
    if label in replacements: return replacements[label]
    if len(label)<=22: return label
    import textwrap
    parts=textwrap.wrap(label,width=20,break_long_words=False,break_on_hyphens=False)
    return '<br>'.join(parts[:3])

COLORS=['#347D70','#356A80','#C77255','#D2A34E','#8F7393','#88958C','#BD7F79','#737C92']
@st.cache_data(show_spinner=False)
def load_aggregates():
    with open(ROOT/'data/indicadores_2025.json', encoding='utf8') as f:
        distributions = json.load(f)
    with open(ROOT/'data/associacoes_2026.json', encoding='utf8') as f:
        associations = json.load(f)
    return distributions, associations

distributions, associations = load_aggregates()

section=st.sidebar.radio('Navegação',['Início','Perfil e hábitos','Associações estatísticas','Marcas e motivações','Sobre a pesquisa','Equipe e publicações'])
if section in ('Perfil e hábitos','Associações estatísticas'):
    import plotly.express as px
    import plotly.graph_objects as go

st.sidebar.caption('Pesquisa com 336 respondentes · Interior paulista · Base original compartilhada entre as análises de 2025 e 2026')


@st.cache_data(show_spinner=False,max_entries=40)
def bar_chart(labels,values,title,xlabel='Percentual (%)'):
    df=pd.DataFrame({'Categoria':labels,'Percentual':values})
    fig=px.bar(df, x='Percentual',y='Categoria',orientation='h',text='Percentual',color='Categoria',color_discrete_map={category: COLORS[i%len(COLORS)] for i,category in enumerate(labels)})
    fig.update_traces(showlegend=False, texttemplate='%{text:.1f}%', textposition='outside',cliponaxis=False)
    fig.update_layout(height=max(320,len(df)*54+110),margin=dict(t=15,b=45,l=6,r=43),plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',xaxis_title=xlabel,yaxis_title='',yaxis={'categoryorder':'total ascending'},xaxis_range=[0, max(values+[1])*1.27],autosize=True)
    fig.update_xaxes(showgrid=True,gridcolor='#EDEAE4',zeroline=False)
    fig.update_yaxes(tickfont=dict(size=11,color='#3A4844'),tickmode='array',
                      tickvals=labels,ticktext=[brief_label(label) for label in labels],automargin=True)
    fig.update_traces(customdata=df['Categoria'],hovertemplate='%{customdata}<br>%{x:.1f}%<extra></extra>',
                      textfont=dict(size=12))
    return fig

# Dados publicados com categorias completas; sem reconstruir células ausentes.
STACK_COLORS={'Sim':'#347D70','Talvez':'#D2A34E','Não':'#C77255','Sempre':'#347D70','Às vezes':'#D2A34E','Nunca':'#C77255','Raramente':'#356A80','Ocasionalmente':'#D2A34E','Frequentemente':'#8F7393'}
FULL_2026={
    'Moda circular × roupas de segunda mão':{
        'groups':['Conhece o conceito'],
        'series':{'Nunca':[32.1],'Raramente':[32.1],'Ocasionalmente':[23.5],'Frequentemente':[12.3]},
        'caption':'Distribuição entre participantes que declararam conhecer moda circular. As quatro respostas somam 100%; o artigo não fornece aqui a distribuição completa dos demais grupos.'},
    'Marcas sustentáveis × leitura de etiquetas':{
        'groups':['Conhece/comprou','Não conhece','Não tem certeza'],
        'series':{'Sempre':[44.6,19.9,18.5],'Às vezes':[38.0,44.9,39.8],'Nunca':[17.4,35.3,41.7]},
        'caption':'Frequência declarada de leitura das etiquetas por contato com marcas sustentáveis. Pequenas divergências de soma decorrem de arredondamentos.'}
}
# Fragmentos disponíveis dos demais cruzamentos: não completar categorias ausentes.
PARTIAL_2026={
 'Percepção ambiental × pagar mais':{'group':'Percepção muito alta','segments':{'Sim':33.8,'Talvez':55.4},'missing':'Não'},
 'ODS × pagar mais':{'group':'Relaciona escolhas aos ODS','segments':{'Sim':41.3,'Talvez':49.2,'Não':9.5},'missing':None}
}
@st.cache_data(show_spinner=False,max_entries=20)
def full_distribution_chart(detail):
    fig=go.Figure()
    for key,values in detail['series'].items():
        fig.add_bar(name=key,y=detail['groups'],x=values,orientation='h',marker_color=STACK_COLORS[key],
                    text=[f'{v:.1f}%' if v>=8 else '' for v in values],textposition='inside',
                    textfont=dict(size=14,color='white'),hovertemplate='%{y}<br>'+key+': %{x:.1f}%<extra></extra>')
    fig.update_layout(barmode='stack',height=250 if len(detail['groups'])==1 else 360,
        margin=dict(t=30,b=30,l=10,r=12),legend=dict(orientation='h',y=1.20,x=0),
        xaxis=dict(title='Percentual dentro de cada grupo (%)',range=[0,105],gridcolor='#EDEAE4'),
        yaxis=dict(title='',autorange='reversed',automargin=True,tickfont=dict(size=11)),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    return fig

# Nuvem calculada offline sobre respostas de marcas; SVG embutido e dados agregados somente.
BRAND_COUNTS={'Hering': 43, 'Nike': 25, 'Adidas': 20, 'Renner': 17, 'Malwee': 15, 'Clariá': 12, 'Shein': 11, 'Zara': 9, 'Levi’s': 9, 'Riachuelo': 7, 'Farm': 7, 'Colcci': 7, 'C&A': 5, 'Lunender': 3, 'Ogochi': 3, 'Marisa': 2, 'Cóz Jeans': 2, 'Pernambucanas': 1}
WORDCLOUD_SVG='<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="480">\n<style>text{font-family:\'Droid Sans Mono\';font-weight:normal;font-style:normal;}</style>\n<rect width="100%" height="100%" style="fill:white"></rect>\n<text transform="translate(142,268)" font-size="267" style="fill:#347D70">Hering</text>\n<text transform="translate(301,446)" font-size="211" style="fill:#356A80">Nike</text>\n<text transform="translate(722,111)" font-size="131" style="fill:#C77255">Adidas</text>\n<text transform="translate(124,457) rotate(-90)" font-size="121" style="fill:#D2A34E">Renner</text>\n<text transform="translate(290,102)" font-size="110" style="fill:#D2A34E">Malwee</text>\n<text transform="translate(823,466)" font-size="99" style="fill:#356A80">Clariá</text>\n<text transform="translate(666,325)" font-size="73" style="fill:#D2A34E">Shein</text>\n<text transform="translate(131,61)" font-size="66" style="fill:#D2A34E">Zara</text>\n<text transform="translate(929,384)" font-size="66" style="fill:#C77255">Levi’s</text>\n<text transform="translate(50,366) rotate(-90)" font-size="59" style="fill:#8F7393">Riachuelo</text>\n<text transform="translate(242,410) rotate(-90)" font-size="59" style="fill:#347D70">Farm</text>\n<text transform="translate(1143,330) rotate(-90)" font-size="59" style="fill:#8F7393">Colcci</text>\n<text transform="translate(195,474)" font-size="51" style="fill:#347D70">C&amp;A</text>\n<text transform="translate(515,36)" font-size="41" style="fill:#8F7393">Lunender</text>\n<text transform="translate(528,217)" font-size="41" style="fill:#356A80">Ogochi</text>\n<text transform="translate(540,474)" font-size="34" style="fill:#347D70">Marisa</text>\n<text transform="translate(4,475)" font-size="34" style="fill:#356A80">Cóz Jeans</text>\n<text transform="translate(294,474)" font-size="26" style="fill:#8F7393">Pernambucanas</text>\n</svg>'

if section=='Início':
    st.markdown('<div class="section-kicker">Observatório científico · Moda circular e sustentável</div>', unsafe_allow_html=True)
    st.title('Moda sustentável no interior paulista')
    st.markdown('<div class="subtitle">Conhecimento, práticas e barreiras no comportamento de consumo</div>',unsafe_allow_html=True)
    st.write('Uma plataforma aberta para conhecer o perfil dos participantes, explorar hábitos de consumo e consultar associações estatísticas encontradas na pesquisa.')
    st.write('')
    col1,col2,col3=st.columns(3)
    col1.metric('Respostas analisadas','336')
    col2.metric('Cruzamentos estatísticos','4')
    col3.metric('Base de dados','1 pesquisa')
    st.caption('As publicações de 2025 e 2026 analisam a mesma base. Não representam amostras independentes nem evolução temporal.')
    st.divider()
    st.subheader('O que os resultados mostram?')
    st.markdown('<div class="note"><b>Conhecimento e consciência ambiental estão associados a escolhas mais sustentáveis, mas não bastam para explicar o comportamento de consumo.</b> Todas as quatro associações testadas foram significativas, porém apresentaram magnitudes limitadas (V de Cramér entre 0,169 e 0,199).</div>',unsafe_allow_html=True)
    st.write('')
    a,b=st.columns(2)
    with a:
        st.markdown('#### Percepção ambiental e intenção de pagar mais')
        st.metric('Percepção ambiental muito alta','33,8%')
        st.caption('Nesse grupo, 33,8% declararam disposição a pagar mais por roupas sustentáveis; 55,4% responderam “Talvez”.')
    with b:
        st.markdown('#### Moda circular e compra de segunda mão')
        st.metric('Conhecem o conceito','35,8%')
        st.caption('Entre os que conheciam moda circular, 35,8% compravam peças usadas ocasional ou frequentemente.')
    st.divider()
    st.subheader('Escolha o que deseja explorar')
    nav1,nav2,nav3=st.columns(3)
    with nav1:
        st.markdown('#### 01 · Perfil e hábitos')
        st.write('Quem respondeu, como compra roupas e quais práticas de consumo declara adotar.')
        st.caption('Acesse pelo menu lateral: Perfil e hábitos')
    with nav2:
        st.markdown('#### 02 · Associações')
        st.write('Veja os cruzamentos, gráficos completos, teste qui-quadrado e V de Cramér.')
        st.caption('Acesse pelo menu lateral: Associações estatísticas')
    with nav3:
        st.markdown('#### 03 · Marcas e motivações')
        st.write('Duas nuvens de palavras distintas, com suas limitações de interpretação.')
        st.caption('Acesse pelo menu lateral: Marcas e motivações')
    st.divider()
    st.subheader('Como a pesquisa foi realizada?')
    st.write('Pesquisa exploratória e descritiva, com 336 respostas obtidas por questionário online, amostragem não probabilística por conveniência e aprofundamento estatístico com teste qui-quadrado e V de Cramér. Os resultados não permitem inferir relações causais nem generalizar a amostra a toda a população do interior paulista.')
    st.caption('Para consultar a metodologia, os créditos dos pesquisadores e as publicações, acesse “Sobre a pesquisa” e “Equipe e publicações” no menu lateral.')

elif section=='Perfil e hábitos':
    st.title('Perfil e hábitos dos participantes')
    st.caption('Frequências descritivas da base original de respostas; dados publicados apenas em formato agregado.')
    # Filtro temático de navegação: não altera os percentuais nem as bases de cálculo.
    indicators=list(distributions)
    thematic={
        'Perfil dos participantes':['idade','faixa etária','gênero','sexo','escolaridade','renda','cidade','profiss'],
        'Hábitos de consumo':['compra','frequência','gasto','loja','promoção','preço','estilo','brechó','segunda mão'],
        'Sustentabilidade e circularidade':['sustent','circular','ambient','ods','etiqueta','marca','descarte','reutil','reform']
    }
    def topic_of(name):
        lower=name.casefold()
        for group, terms in thematic.items():
            if any(term in lower for term in terms):
                return group
        return 'Outros indicadores'
    groups={group:[name for name in indicators if topic_of(name)==group] for group in [*thematic,'Outros indicadores']}
    groups={key:value for key,value in groups.items() if value}
    group=st.selectbox('Tema',list(groups))
    indicador=st.selectbox('Indicador',groups[group])
    st.subheader(indicador)
    st.caption('Distribuição percentual das respostas. Toque nas barras (celular) ou passe o cursor (computador) para consultar os valores.')
    df=pd.DataFrame(distributions[indicador])
    st.plotly_chart(bar_chart(df.categoria.tolist(),df.percentual.tolist(),indicador),use_container_width=True,config=PLOT_CONFIG)
    if len(df):
        top=df.sort_values('percentual',ascending=False).iloc[0]
        st.markdown(f"**Leitura do gráfico:** a categoria mais frequente foi **{top['categoria']}** ({top['percentual']:.1f}%).".replace('.',','))
    if st.toggle('Mostrar tabela e quantidades absolutas',value=False):
        st.dataframe(df.rename(columns={'categoria':'Resposta','quantidade':'Participantes','percentual':'Percentual (%)'}),hide_index=True,use_container_width=True)
    st.download_button('Baixar tabela agregada (CSV)',df.to_csv(index=False).encode('utf-8-sig'),file_name='indicador_agregado.csv',mime='text/csv')
    st.caption('No celular, a tabela abaixo permite conferir os nomes completos das categorias. Percentuais calculados sobre N=336. Respostas pouco frequentes foram agrupadas como “Outras respostas (agrupadas)”. Alguns campos tiveram padronizações limitadas; verifique as categorias originais antes de usar em novas análises.')

elif section=='Associações estatísticas':
    st.title('Associações entre conhecimento e consumo')
    st.caption('Resultados do estudo de 2026 · Teste qui-quadrado · V de Cramér · nível de 5%.')
    nome=st.selectbox('Selecione o cruzamento',list(associations))
    a=associations[nome]
    st.subheader(nome)
    if nome in FULL_2026:
        st.markdown('#### Distribuição detalhada das respostas')
        detail=FULL_2026[nome]
        st.plotly_chart(full_distribution_chart(detail),use_container_width=True,config=PLOT_CONFIG)
        st.caption(detail['caption'])
        df_detail=pd.DataFrame({'Grupo':detail['groups'],**detail['series']})
        with st.expander('Consultar e exportar a tabela detalhada'):
            st.dataframe(df_detail,hide_index=True,use_container_width=True)
            st.download_button('Baixar CSV detalhado',df_detail.to_csv(index=False).encode('utf-8-sig'),file_name='distribuicao_detalhada.csv',mime='text/csv')
    else:
        st.markdown('#### Comparação entre grupos')
        st.plotly_chart(bar_chart(a['categorias'],a['percentuais'],a['variavel']),use_container_width=True,config=PLOT_CONFIG)
        st.caption('Percentuais da resposta afirmativa nos grupos apresentados no artigo.')
        p=PARTIAL_2026.get(nome)
        if p:
            st.markdown('#### Respostas disponíveis para um dos grupos')
            st.write('**'+p['group']+'**')
            segments=p['segments']
            fig=go.Figure()
            for label,value in segments.items():
                fig.add_bar(x=[value],y=[p['group']],orientation='h',name=label,marker_color=STACK_COLORS[label],text=[f'{value:.1f}%'],textposition='inside',hovertemplate=label+': %{x:.1f}%<extra></extra>')
            fig.update_layout(barmode='stack',height=230,xaxis=dict(title='Percentual (%)',range=[0,105]),yaxis=dict(title=''),legend=dict(orientation='h',y=1.3),margin=dict(t=20,b=30,l=0,r=10),plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig,use_container_width=True,config=PLOT_CONFIG)
            if p['missing']:
                st.caption('Este gráfico parcial não apresenta a categoria “'+p['missing']+'”: o percentual correspondente não foi publicado explicitamente nesse trecho do artigo. Não se trata de barra 100% completa.')
            else:
                st.caption('Categorias completas publicadas para este grupo; os demais grupos são mostrados apenas na comparação de respostas afirmativas.')
    m1,m2,m3=st.columns(3)
    m1.metric('Qui-quadrado (χ²)',f"{a['chi2']:.2f}".replace('.',','))
    m2.metric('Significância','p < 0,001')
    m3.metric('V de Cramér',f"{a['v_cramer']:.3f}".replace('.',','))
    st.markdown('#### Como interpretar')
    st.write(a['interpretacao'])
    st.info('A associação é estatisticamente significativa, mas sua magnitude é limitada. Os resultados não permitem afirmar causa e efeito.')
    st.caption(a['nota'])
    with st.expander('Consultar os valores de comparação publicados'):
        df=pd.DataFrame({'Categoria':a['categorias'],'Percentual (%)':a['percentuais']})
        st.dataframe(df,hide_index=True,use_container_width=True)
        st.download_button('Baixar tabela agregada (CSV)',df.to_csv(index=False).encode('utf-8-sig'),file_name='associacao_agregada.csv',mime='text/csv')

elif section=='Marcas e motivações':
    st.title('Marcas e motivações de consumo')
    st.caption('Duas análises exploratórias diferentes sobre respostas abertas; não confundir motivos de escolha e nomes de marcas.')
    st.subheader('Marcas lembradas espontaneamente')
    st.write('Nuvem exploratória construída a partir da pergunta aberta sobre marcas de roupas. O tamanho dos nomes representa o número de participantes cujas respostas citaram cada marca identificada na padronização.')
    st.image(WORDCLOUD_SVG,caption='Nuvem de menções espontâneas a marcas — base original da pesquisa.',use_container_width=True)
    st.markdown('#### Frequências de menção identificadas')
    df_brand=pd.DataFrame([{'Marca':brand,'Respostas com menção':n} for brand,n in BRAND_COUNTS.items()])
    st.dataframe(df_brand,hide_index=True,use_container_width=True)
    st.download_button('Baixar frequências agregadas (CSV)',df_brand.to_csv(index=False).encode('utf-8-sig'),file_name='marcas_mencionadas.csv',mime='text/csv')
    st.warning('A nuvem não representa participação de mercado, volume de compras, preferência comprovada ou sustentabilidade das marcas. A identificação foi realizada por correspondência de nomes conhecidos e não abrange necessariamente todas as respostas distintas. Cada marca é contada no máximo uma vez por respondente.')

    st.divider()
    st.subheader('Motivações para as escolhas de consumo — visualização de 2025')
    st.write('A figura abaixo foi produzida no projeto de 2025 e apresenta palavras extraídas das respostas sobre motivações de consumo. Sua leitura é qualitativa e exploratória: palavras maiores indicam maior destaque no processamento original, não necessariamente número de participantes.')
    st.image(str(ROOT/'assets'/'motivacoes_2025.jpg'),caption='Nuvem original de motivações do painel de 2025 — crédito ao projeto original (Ronnie Marinho e equipe).',use_container_width=True)
    st.caption('A imagem original foi preservada. O código que a gerou deve ser auditado antes de afirmar frequências exatas, pois não substitui uma análise qualitativa das respostas.')


elif section=='Sobre a pesquisa':
    st.title('Sobre a pesquisa')
    st.write('Pesquisa exploratória e descritiva, predominantemente quantitativa, com análise complementar de respostas abertas. Foram analisadas 336 respostas de consumidores do interior paulista obtidas por questionário online, em amostragem não probabilística por conveniência.')
    st.subheader('Origem do painel')
    st.write('Este observatório consolida informações do painel inicial de 2025 e da análise associativa publicada em 2026. A visualização de motivações foi preservada do projeto original de 2025, desenvolvido com contribuição de Ronnie Marinho. O índice experimental de circularidade do painel anterior não foi incorporado, pois necessita de revisão metodológica.')
    st.subheader('Continuidade científica')
    st.write('A investigação apresentada em 2025 descreveu características, percepções e hábitos. O artigo de 2026 retomou o mesmo banco e aprofundou quatro associações específicas entre conhecimento/percepção socioambiental e práticas/intenção de consumo.')
    st.subheader('Procedimentos estatísticos')
    st.write('Frequências absolutas e relativas, tabelas de contingência, teste do qui-quadrado de independência e V de Cramér como medida de magnitude. Valores de V entre 0,169 e 0,199, indicando magnitude limitada.')
    st.subheader('Limitações')
    st.write('A amostra por conveniência não é estatisticamente representativa de toda a população do interior paulista. As respostas são autorrelatadas, coletadas em corte transversal e não permitem inferências causais. O questionário online pode favorecer pessoas com maior acesso digital.')
    st.subheader('Privacidade e transparência')
    st.write('Este protótipo publica **somente tabelas agregadas**. A base de respostas individuais, localidades específicas, carimbos de data/hora e depoimentos livres não estão incluídos nos arquivos do site. Recortes demográficos conjuntos requerem validação ética e medidas contra reidentificação antes da disponibilização.')

else:
    st.title('Equipe e publicações')
    st.caption('Pesquisadores, trajetória acadêmica e publicações que fundamentam o Observatório.')
    st.subheader('Conheça a pesquisadora')
    foto, apresentacao = st.columns([1, 2], gap='large')
    with foto:
        st.image(str(ROOT/'assets'/'lilian_fortuna.jpg'), caption='Lilian Fortuna', use_container_width=True)
    with apresentacao:
        st.markdown('### Lilian Fortuna')
        st.markdown('**Pesquisadora · Doutoranda em Agronegócio e Desenvolvimento — Unesp/Tupã**')
        st.write('Mestra em Educação pela UFRJ, com formação interdisciplinar em Matemática, Pedagogia, Administração e Design de Moda. Possui mais de 17 anos de experiência na educação, atua no ensino superior e é empreendedora, à frente do Consultório de Estilo desde 2019.')
        st.write('Desenvolve pesquisas em economia circular aplicada aos biossistemas, valorização de resíduos agroindustriais e fibras têxteis celulósicas de bagaço de cana-de-açúcar, articulando sustentabilidade, inovação e modelos de negócios.')
        st.markdown('**Contato acadêmico:** [lilian.fortuna@unesp.br](mailto:lilian.fortuna@unesp.br)')
    st.divider()
    st.subheader('Equipe de pesquisa e colaboração')
    st.markdown('**Andréa Rossi Scalco** — Professora e pesquisadora da Unesp, coautora dos estudos de 2025 e 2026.\n\n**Maurício de Campos Araújo** — Professor e pesquisador da EACH/USP, coautor do estudo de 2026.\n\n**Ronnie Shida Marinho** — Coautor do estudo de 2025 e colaborador técnico do painel digital precursor.')
    st.divider()
    st.subheader('Publicações científicas')
    with st.container(border=True):
        st.markdown('**2025 | Moda Circular em Foco: Início de uma Jornada Consciente sob a Perspectiva dos ODS**')
        st.write('Lilian Fortuna; Ronnie Shida Marinho; Andréa Rossi Scalco.')
        st.write('Anais do XX Colóquio de Moda · ISSN 1982-0941')
        st.link_button('Consultar publicação (DOI)', 'https://doi.org/10.29327/1886366.20-1')
    with st.container(border=True):
        st.markdown('**2026 | Moda Sustentável no Interior Paulista: Conhecimento, Práticas e Barreiras**')
        st.write('Lilian Fortuna; Maurício de Campos Araújo; Andréa Rossi Scalco.')
        st.write('Artigo completo aceito para apresentação no Colóquio de Moda de 2026. Link dos anais a inserir após publicação.')
    st.subheader('Apoio e créditos')
    st.write('A pesquisa informa apoio da CAPES — Código de Financiamento 001, conforme registrado no artigo de 2026.')
    st.caption('O painel precursor de 2025 contou com contribuição técnica de Ronnie Shida Marinho. Os créditos e direitos aplicáveis à imagem histórica devem ser preservados.')

st.divider()
st.caption('Observatório da Moda Sustentável no Interior Paulista · Dados agregados · 2026')
