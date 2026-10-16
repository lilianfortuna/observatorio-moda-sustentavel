"""Observatório da Moda Sustentável no Interior Paulista — protótipo científico público.
Somente dados agregados integram esta distribuição.
"""
import json
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
</style>''',unsafe_allow_html=True)
COLORS=['#347D70','#356A80','#C77255','#D2A34E','#8F7393','#88958C','#BD7F79','#737C92']
with open(ROOT/'data/indicadores_2025.json',encoding='utf8') as f: distributions=json.load(f)
with open(ROOT/'data/associacoes_2026.json',encoding='utf8') as f: associations=json.load(f)

section=st.sidebar.radio('Navegação',['Início','Perfil e hábitos','Associações estatísticas','Marcas e motivações','Sobre a pesquisa','Equipe e publicações'])
st.sidebar.caption('Pesquisa com 336 respondentes · Interior paulista · Base original compartilhada entre as análises de 2025 e 2026')


def bar_chart(labels,values,title,xlabel='Percentual (%)'):
    df=pd.DataFrame({'Categoria':labels,'Percentual':values})
    fig=px.bar(df, x='Percentual',y='Categoria',orientation='h',text='Percentual',color='Categoria',color_discrete_map={category: COLORS[i%len(COLORS)] for i,category in enumerate(labels)})
    fig.update_traces(showlegend=False, texttemplate='%{text:.1f}%', textposition='outside',cliponaxis=False)
    fig.update_layout(height=max(310,len(df)*47+120),margin=dict(t=15,b=35,l=10,r=85),plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',xaxis_title=xlabel,yaxis_title='',yaxis={'categoryorder':'total ascending'},xaxis_range=[0, max(values+[1])*1.22])
    fig.update_xaxes(showgrid=True,gridcolor='#EDEAE4',zeroline=False)
    fig.update_yaxes(tickfont=dict(size=13,color='#3A4844'))
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
def full_distribution_chart(detail):
    fig=go.Figure()
    for key,values in detail['series'].items():
        fig.add_bar(name=key,y=detail['groups'],x=values,orientation='h',marker_color=STACK_COLORS[key],
                    text=[f'{v:.1f}%' if v>=8 else '' for v in values],textposition='inside',
                    textfont=dict(size=14,color='white'),hovertemplate='%{y}<br>'+key+': %{x:.1f}%<extra></extra>')
    fig.update_layout(barmode='stack',height=250 if len(detail['groups'])==1 else 360,
        margin=dict(t=30,b=30,l=10,r=12),legend=dict(orientation='h',y=1.20,x=0),
        xaxis=dict(title='Percentual dentro de cada grupo (%)',range=[0,105],gridcolor='#EDEAE4'),
        yaxis=dict(title='',autorange='reversed'),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    return fig

# Nuvem calculada offline sobre respostas de marcas; SVG embutido e dados agregados somente.
BRAND_COUNTS={'Hering': 43, 'Nike': 25, 'Adidas': 20, 'Renner': 17, 'Malwee': 15, 'Clariá': 12, 'Shein': 11, 'Zara': 9, 'Levi’s': 9, 'Riachuelo': 7, 'Farm': 7, 'Colcci': 7, 'C&A': 5, 'Lunender': 3, 'Ogochi': 3, 'Marisa': 2, 'Cóz Jeans': 2, 'Pernambucanas': 1}
WORDCLOUD_SVG='<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="480">\n<style>text{font-family:\'Droid Sans Mono\';font-weight:normal;font-style:normal;}</style>\n<rect width="100%" height="100%" style="fill:white"></rect>\n<text transform="translate(142,268)" font-size="267" style="fill:#347D70">Hering</text>\n<text transform="translate(301,446)" font-size="211" style="fill:#356A80">Nike</text>\n<text transform="translate(722,111)" font-size="131" style="fill:#C77255">Adidas</text>\n<text transform="translate(124,457) rotate(-90)" font-size="121" style="fill:#D2A34E">Renner</text>\n<text transform="translate(290,102)" font-size="110" style="fill:#D2A34E">Malwee</text>\n<text transform="translate(823,466)" font-size="99" style="fill:#356A80">Clariá</text>\n<text transform="translate(666,325)" font-size="73" style="fill:#D2A34E">Shein</text>\n<text transform="translate(131,61)" font-size="66" style="fill:#D2A34E">Zara</text>\n<text transform="translate(929,384)" font-size="66" style="fill:#C77255">Levi’s</text>\n<text transform="translate(50,366) rotate(-90)" font-size="59" style="fill:#8F7393">Riachuelo</text>\n<text transform="translate(242,410) rotate(-90)" font-size="59" style="fill:#347D70">Farm</text>\n<text transform="translate(1143,330) rotate(-90)" font-size="59" style="fill:#8F7393">Colcci</text>\n<text transform="translate(195,474)" font-size="51" style="fill:#347D70">C&amp;A</text>\n<text transform="translate(515,36)" font-size="41" style="fill:#8F7393">Lunender</text>\n<text transform="translate(528,217)" font-size="41" style="fill:#356A80">Ogochi</text>\n<text transform="translate(540,474)" font-size="34" style="fill:#347D70">Marisa</text>\n<text transform="translate(4,475)" font-size="34" style="fill:#356A80">Cóz Jeans</text>\n<text transform="translate(294,474)" font-size="26" style="fill:#8F7393">Pernambucanas</text>\n</svg>'

if section=='Início':
    st.markdown('<div class="section-kicker">Ciência aberta · Consumo e circularidade</div>',unsafe_allow_html=True)
    st.title('Observatório da Moda Sustentável no Interior Paulista')
    st.markdown('**Conhecimento, práticas e barreiras no consumo de moda.** Um ambiente aberto para explorar resultados de pesquisa e compreender escolhas de consumo responsável.')
    a,b,c=st.columns(3)
    a.metric('Participantes','336');b.metric('Análises associativas','4');c.metric('Figuras no estudo de 2026','5')
    st.subheader('O que o estudo revelou?')
    st.markdown('<div class="note">Maior percepção ambiental e conhecimento sobre circularidade apresentaram associações com intenções ou práticas de consumo mais sustentáveis. Entretanto, as associações foram de magnitude limitada: conhecimento não explica sozinho o comportamento.</div>',unsafe_allow_html=True)
    st.markdown('### Explore o Observatório')
    st.markdown('**Perfil e hábitos** apresenta as distribuições dos participantes. **Associações estatísticas** aprofunda relações entre conhecimento, percepções e comportamento. **Marcas e motivações** reúne duas nuvens distintas: marcas lembradas e motivações de compra. Os dois estudos utilizam a mesma base de respostas.')
    st.markdown('### Como explorar')
    st.write('**Perfil e hábitos:** frequências descritivas obtidas da pesquisa original.  **Associações estatísticas:** resultados do aprofundamento analítico de 2026.  **Sobre a pesquisa:** método e limites de interpretação.')
    st.info('Os artigos de 2025 e 2026 analisam a **mesma base de 336 respostas** em abordagens complementares. Não são duas coletas em momentos diferentes, nem uma amostra de 672 pessoas.')

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
    st.caption('Distribuição percentual das respostas. Passe o cursor sobre as barras para consultar os valores.')
    df=pd.DataFrame(distributions[indicador])
    st.plotly_chart(bar_chart(df.categoria.tolist(),df.percentual.tolist(),indicador),use_container_width=True)
    if len(df):
        top=df.sort_values('percentual',ascending=False).iloc[0]
        st.markdown(f"**Leitura do gráfico:** a categoria mais frequente foi **{top['categoria']}** ({top['percentual']:.1f}%).".replace('.',','))
    if st.toggle('Mostrar tabela e quantidades absolutas',value=False):
        st.dataframe(df.rename(columns={'categoria':'Resposta','quantidade':'Participantes','percentual':'Percentual (%)'}),hide_index=True,use_container_width=True)
    st.download_button('Baixar tabela agregada (CSV)',df.to_csv(index=False).encode('utf-8-sig'),file_name='indicador_agregado.csv',mime='text/csv')
    st.caption('Percentuais calculados sobre N=336. Respostas pouco frequentes foram agrupadas como “Outras respostas (agrupadas)”. Alguns campos tiveram padronizações limitadas; verifique as categorias originais antes de usar em novas análises.')

elif section=='Associações estatísticas':
    st.title('Associações entre conhecimento e consumo')
    st.caption('Resultados do estudo de 2026 · Teste qui-quadrado · V de Cramér · nível de 5%.')
    nome=st.selectbox('Selecione o cruzamento',list(associations))
    a=associations[nome]
    st.subheader(nome)
    if nome in FULL_2026:
        st.markdown('#### Distribuição detalhada das respostas')
        detail=FULL_2026[nome]
        st.plotly_chart(full_distribution_chart(detail),use_container_width=True)
        st.caption(detail['caption'])
        df_detail=pd.DataFrame({'Grupo':detail['groups'],**detail['series']})
        with st.expander('Consultar e exportar a tabela detalhada'):
            st.dataframe(df_detail,hide_index=True,use_container_width=True)
            st.download_button('Baixar CSV detalhado',df_detail.to_csv(index=False).encode('utf-8-sig'),file_name='distribuicao_detalhada.csv',mime='text/csv')
    else:
        st.markdown('#### Comparação entre grupos')
        st.plotly_chart(bar_chart(a['categorias'],a['percentuais'],a['variavel']),use_container_width=True)
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
            st.plotly_chart(fig,use_container_width=True)
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
    st.subheader('Pesquisadores')
    st.markdown('**Lilian Fortuna** · Doutoranda em Agronegócio e Desenvolvimento, Unesp/Tupã  \n**Maurício de Campos Araújo** · EACH/USP  \n**Andréa Rossi Scalco** · Unesp/Tupã')
    st.subheader('Sobre Lilian Fortuna')
    st.write('Pesquisadora e doutoranda em Agronegócio e Desenvolvimento pela Unesp, campus de Tupã, mestra em Educação pela UFRJ, com formação interdisciplinar em Matemática, Pedagogia, Administração e Design de Moda. Possui mais de 17 anos de experiência em educação, atua no ensino superior e pesquisa economia circular, inovação e aproveitamento de resíduos agroindustriais para materiais têxteis.')
    st.markdown('**Contato acadêmico:** [lilian.fortuna@unesp.br](mailto:lilian.fortuna@unesp.br)')
    st.subheader('Publicações relacionadas')
    st.markdown('**2026:** *Moda sustentável no interior paulista: conhecimento, práticas e barreiras* — Lilian Fortuna, Maurício de Campos Araújo e Andréa Rossi Scalco.  \n**2025:** *Moda circular em foco: início de uma jornada consciente sob a perspectiva dos ODS* — investigação descritiva anterior.')
    st.caption('Painel precursor (2025): contribuição técnica de Ronnie Marinho. A reprodução da nuvem histórica no Observatório deve manter atribuição e respeitar direitos aplicáveis. Acrescentar links dos artigos completos quando disponíveis.')
    st.caption('Pesquisa com apoio CAPES — Código de Financiamento 001 (conforme artigo de 2026).')

st.divider()
st.caption('Observatório da Moda Sustentável no Interior Paulista · Versão 5.0 · Dados agregados · 2026')
