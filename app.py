"""Observatório da Moda Sustentável no Interior Paulista — protótipo científico público.
Somente dados agregados integram esta distribuição.
"""
import json
from pathlib import Path
import pandas as pd
import plotly.express as px
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

section=st.sidebar.radio('Navegação',['Início','Perfil e hábitos','Associações estatísticas','Sobre a pesquisa','Equipe e publicações'])
st.sidebar.caption('Pesquisa com 336 respondentes · Interior paulista · Base original compartilhada entre as análises de 2025 e 2026')


def bar_chart(labels,values,title,xlabel='Percentual (%)'):
    df=pd.DataFrame({'Categoria':labels,'Percentual':values})
    fig=px.bar(df, x='Percentual',y='Categoria',orientation='h',text='Percentual',color='Categoria',color_discrete_map={category: COLORS[i%len(COLORS)] for i,category in enumerate(labels)})
    fig.update_traces(showlegend=False, texttemplate='%{text:.1f}%', textposition='outside',cliponaxis=False)
    fig.update_layout(height=max(310,len(df)*47+120),margin=dict(t=15,b=35,l=10,r=85),plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',xaxis_title=xlabel,yaxis_title='',yaxis={'categoryorder':'total ascending'},xaxis_range=[0, max(values+[1])*1.22])
    fig.update_xaxes(showgrid=True,gridcolor='#EDEAE4',zeroline=False)
    fig.update_yaxes(tickfont=dict(size=13,color='#3A4844'))
    return fig

if section=='Início':
    st.markdown('<div class="section-kicker">Ciência aberta · Consumo e circularidade</div>',unsafe_allow_html=True)
    st.title('Observatório da Moda Sustentável no Interior Paulista')
    st.markdown('**Conhecimento, práticas e barreiras no consumo de moda.** Um ambiente aberto para explorar resultados de pesquisa e compreender escolhas de consumo responsável.')
    a,b,c=st.columns(3)
    a.metric('Participantes','336');b.metric('Análises associativas','4');c.metric('Figuras no estudo de 2026','5')
    st.subheader('O que o estudo revelou?')
    st.markdown('<div class="note">Maior percepção ambiental e conhecimento sobre circularidade apresentaram associações com intenções ou práticas de consumo mais sustentáveis. Entretanto, as associações foram de magnitude limitada: conhecimento não explica sozinho o comportamento.</div>',unsafe_allow_html=True)
    st.markdown('### Explore o Observatório')
    st.markdown('**Perfil e hábitos** apresenta as distribuições dos participantes. **Associações estatísticas** aprofunda relações entre conhecimento, percepções e comportamento. Os dois estudos utilizam a mesma base de respostas.')
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
    st.caption('Análises de 2026 com teste qui-quadrado e V de Cramér, nível de significância de 5%.')
    nome=st.selectbox('Selecione o cruzamento',list(associations))
    a=associations[nome]
    st.subheader(nome)
    st.plotly_chart(bar_chart(a['categorias'],a['percentuais'],a['variavel']),use_container_width=True)
    x,y,z=st.columns(3)
    x.metric('Qui-quadrado (χ²)',f"{a['chi2']:.2f}".replace('.',','))
    y.metric('Significância','p < 0,001')
    z.metric('V de Cramér',f"{a['v_cramer']:.3f}".replace('.',','))
    st.markdown('#### Interpretação')
    st.write(a['interpretacao'])
    st.warning('As associações são estatisticamente significativas, mas têm magnitude limitada. Os resultados não demonstram causalidade.')
    st.caption(a['nota'])
    st.markdown('#### Resultados em tabela')
    df=pd.DataFrame({'Categoria':a['categorias'],'Percentual (%)':a['percentuais']})
    st.dataframe(df,hide_index=True,use_container_width=True)
    st.download_button('Baixar tabela agregada (CSV)',df.to_csv(index=False).encode('utf-8-sig'),file_name='associacao_agregada.csv',mime='text/csv')
    st.info('A quinta figura do artigo é uma nuvem de marcas citadas espontaneamente. A imagem original e suas frequências serão incorporadas após revisão: menções não equivalem a compras ou preferências confirmadas.')

elif section=='Sobre a pesquisa':
    st.title('Sobre a pesquisa')
    st.write('Pesquisa exploratória e descritiva, predominantemente quantitativa, com análise complementar de respostas abertas. Foram analisadas 336 respostas de consumidores do interior paulista obtidas por questionário online, em amostragem não probabilística por conveniência.')
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
    st.caption('Acrescentar links dos artigos completos quando disponíveis publicamente e autorizados para republicação.')
    st.caption('Pesquisa com apoio CAPES — Código de Financiamento 001 (conforme artigo de 2026).')

st.divider()
st.caption('Observatório da Moda Sustentável no Interior Paulista · Protótipo de divulgação científica · Dados agregados · 2026')
