import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
from fastapi import FastAPI
from pydantic import BaseModel

# Carregando o CSV
@st.cache_data
def load_data():
    data = pd.read_csv('lixo.csv')
    data_dom = pd.read_csv('C:\\Users\\User\\Documents\\CDD\\PB\\PB\\dados_mesclados_dom.csv')
    data_pub = pd.read_csv('C:\\Users\\User\\Documents\\CDD\\PB\\PB\\dados_mesclados_pub.csv')
    data_comp = pd.read_csv('C:\\Users\\User\\Documents\\CDD\\PB\\TP5\\data_comp.csv')
    return data, data_dom, data_pub, data_comp

# Gerando a nuvem de palavras com cache
@st.cache_data
def generate_wordcloud(text):
    stopwords = set(STOPWORDS)
    stopwords.update([
         "para", "como", "outro", "outra", "podem", "também", "cada", "este"
    ])
    wordcloud = WordCloud(width=800, height=400, background_color='white', 
                          max_words=200, colormap='viridis',
                          stopwords=stopwords, regexp=r'\b\w{4,}\b').generate(text)
    
    return wordcloud

# Carregando o conteúdo do arquivo .txt
@st.cache_data
def load_txt_file():
    with open('C:\\Users\\User\\Documents\\CDD\\PB\\conteudo_reciclagem.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    return content

# Configurando o estado de sessão para armazenar variáveis ao longo da interação
if 'data' not in st.session_state:
    st.session_state['data'] = None
if 'data_dom' not in st.session_state:
    st.session_state['data_dom'] = None
if 'data_pub' not in st.session_state:
    st.session_state['data_pub'] = None
if 'data_comp' not in st.session_state:
    st.session_state['data_comp'] = None
if 'wordcloud' not in st.session_state:
    st.session_state['wordcloud'] = None

# Raspando o conteúdo de uma notícia a partir da URL
def scrape_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Identificando os parágrafos principais da notícia
    paragraphs = soup.find_all('p')
    
    # Extraindo o texto dos parágrafos
    news_text = ' '.join([p.get_text() for p in paragraphs if len(p.get_text()) > 20])
    
    return news_text

# Função para converter DataFrame em CSV para download
def convert_to_csv(df):
    output = io.StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()

# Upload de novos dados CSV
def upload_file():
    uploaded_file = st.file_uploader("Escolha um arquivo CSV para upload", type=["csv"])
    if uploaded_file:
        try:
            data = pd.read_csv(uploaded_file)
            st.success("Arquivo carregado com sucesso!")
            return data
        except Exception as e:
            st.error(f"Erro ao carregar o arquivo: {e}")
            return pd.DataFrame()
    return None

# Download dos dados modificados
def download_file(data):
    buffer = io.BytesIO()
    data.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer

menu = st.sidebar.selectbox('Selecione um item:',
                            (
                                    'Página inicial',
                                    'Links úteis',
                                    'Notícias recentes',
                                    'Tabela de dados',
                                    'Wikipedia',
                                    'Serviço de download/upload',
                                    'Recursos de IA via LLM'
                            ))

if menu == 'Página inicial':
        st.title("Projeto Reciclagem")
        image_url = "https://blog.larplasticos.com.br/s/img/wp-content/uploads/2020/08/O-que-significa-o-simbolo-da-reciclagem.jpg"
        st.image(image_url, use_column_width=True)
        st.write("""
        A gestão inadequada de resíduos sólidos urbanos representa um dos grandes desafios ambientais e sociais das cidades modernas. Muitos resíduos recicláveis ainda acabam em aterros sanitários, contribuindo para a degradação ambiental, aumento das emissões de gases de efeito estufa e desperdício de recursos valiosos. Além disso, a falta de incentivo para a população adotar práticas de reciclagem e a dificuldade em conectar pessoas e empresas que podem reutilizar materiais recicláveis intensificam o problema.

        A proposta para diminuir este problema é o futuro desenvolvimento de uma aplicação cujos dois principais objetivos são:

        - Facilitar a troca de materiais recicláveis: Criar uma plataforma que conecta indivíduos e empresas que têm materiais recicláveis com aqueles que podem reutilizá-los, promovendo uma economia circular.
        - Incentivar a reciclagem: Através de um sistema de pontuação que recompensa os usuários por reciclar corretamente, promovendo a participação ativa da comunidade.
                 
        Nesta fase beta da aplicação, podem ser encontradas algumas notícias úteis que dão a dimensão do problema na cidade do RJ, além de algumas análises feitas sobre os dados produzidos pelo portal Data.Rio
                 
        Por fim, foi desenvolvido um chatbot do modelo Gemini (gemini-1.5-flash) treinado especificamente para responder dúvidas sobre reciclagem e tratamento de resíduos.
                 
        Com isso, espera-se conscientizar a população para a relevância deste assunto e servir como um repositório de tópicos pertinentes ao tema.

        """)

        st.markdown("---")

        st.write('Aplicação desenvolvida por Ciro Ferreira, para o Projeto de Bloco: Ciência de Dados Aplicada')

elif menu == 'Links úteis':
        st.subheader("Links úteis:\n")
        st.write('Empresas e ONGs de destaque no universo da conscientização ambiental sobre reciclagem.')

        st.markdown("""
                - [Reciclaê](https://institutolegado.org/blog/reciclae-o-aplicativo-que-conecta-catadores-a-materiais-reciclaveis/?gad_source=1&gclid=Cj0KCQjwrKu2BhDkARIsAD7GBoslHXWS7usjo0ZVHRyI4sS05_EZePli0gYdD2bhWSjTsY9qwVVMqFoaArkcEALw_wcB)\n
                    Aplicativo que conecta catadores a materiais recicláveis
                    
                - [Cataki](https://www.cataki.org/)\n
                    Ferramenta que aproxima os profissionais da reciclagem dos geradores de resíduos
                    
                - [Pimp my carroça](https://pimpmycarroca.com/)\n
                    ONG que desenvolve iniciativas pelas catadoras e catadores de todo o Brasil através do artivismo, mobilização, visibilidade e tecnologias sociais colaborativas e inovadoras.
        """)

        st.markdown('---')
        
        st.subheader('Filmes sobre o tema:')
        st.markdown('\n')
        
        movies = [
    {
        "title": "Lixo Extraordinário",
        "description": """O documentário relata o trabalho do artista plástico brasileiro Vik Muniz com catadores de material reciclável em um dos maiores aterros controlados do mundo, localizado no Jardim Gramacho, bairro periférico de Duque de Caxias.""",
        "link": "https://youtu.be/61eudaWpWb8?si=DyBU4dc5K7JhP0ih",
        "image": "https://cinegarimpo.com.br/wp/content/uploads/2011/02/cinegarimpo.com.br-lixo-extraordinario-waste-land-lixo-extraordinario-vik-muniz-d-nq-np-730423-mlb26976463112-032018-f.jpg"
    },
    {
        "title": "Estamira",
        "description": """Documentário sobre a vida de Estamira, uma mulher que trabalha em um lixão no Rio de Janeiro e reflete sobre sociedade, lixo e vida.""",
        "link": "https://youtu.be/-wHISEEXMh4?si=bqRD-NSZpu03wJR2",
        "image": "https://wikifavelas.com.br/images/2/27/Estamira_filme.jpg"
    },
    {
        "title": "Ilha das Flores",
        "description": """Um tomate é plantado, colhido, transportado e vendido num supermercado, mas apodrece e acaba no lixo. O filme segue-o até seu verdadeiro final, tudo para deixar clara a diferença que existe entre tomates, porcos e seres humanos.""",
        "link": "https://youtu.be/h30BO_6kFNM?si=l7_8GJayVNqPOo7I",
        "image": "https://s1.static.brasilescola.uol.com.br/be/conteudo/images/vencedor-na-categoria-festival-gramado-1989-curta-metragem-ilha-das-flores-apresenta-interessantes-recursos-linguagem-539763e628fce.jpg"
    }
]

        for movie in movies:
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(movie["image"], width=150, caption=movie["title"])
            with cols[1]:
                st.markdown(
                    f"""
                    ### [{movie['title']}]({movie['link']})
                    {movie['description']}
                    """
                )
            st.divider()


elif menu == 'Notícias recentes':
     st.subheader('Notícias recentes')
     st.write('Notícias publicadas recentemente que dão a dimensão do problema do recolhimento e tratamento de resíduos no RJ')

     st.markdown("---")
     
     noticias = {
        'Menos de 1% do lixo produzido no Rio passa por coleta seletiva': 'https://vejario.abril.com.br/cidade/menos-de-1-do-lixo-produzido-no-rio-de-janeiro-passa-por-coleta-seletiva',
        'O Rio de Janeiro tem um dos piores índices de recuperação de resíduos': 'https://www.ecodebate.com.br/2023/04/14/o-rio-de-janeiro-tem-um-dos-piores-indices-de-recuperacao-de-residuos/',
        'Produção diária de lixo no Rio de Janeiro chega a 17 mil toneladas': 'https://orlario.com.vc/esg/sustentabilidade/producao-diaria-de-lixo-no-rio-de-janeiro-chega-a-17-mil-toneladas/',
        'Falta de reciclagem faz Rio de Janeiro desperdiçar R$ 2 bi': 'https://saneamentobasico.com.br/acervo-tecnico/falta-de-reciclagem-rio-de-janeiro/',
        'Rio enterra R$ 1 bilhão em resíduos recicláveis por ano': 'https://www.firjan.com.br/noticias/rio-enterra-r-1-bilhao-de-residuos-reciclaveis-por-ano-revela-estudo-da-firjan.htm',
    }
     
     noticia_selecionada = st.sidebar.radio("Selecione uma notícia:", list(noticias.keys()))
     
     url_selecionada = noticias[noticia_selecionada]
     noticia_conteudo = scrape_news(url_selecionada)

     st.subheader(noticia_selecionada)
     st.write(noticia_conteudo)
     st.markdown(f"[Leia mais]({url_selecionada})")

     st.markdown("---")


elif menu == 'Tabela de dados':
        
        opcoes = {'Total do lixo recolhido (2002-2022)': 'data',
                  'Lixo domiciliar (1990-2023)': 'data_dom',
                  'Lixo público (1990-2023)': 'data_pub',
                  'Análise de lixo domiciliar por bairro': 'data_dom',
                  'Análise de lixo público por bairro': 'data_pub',
                  'Comparações': 'data_comp'}
        
        descricoes = {
    'Total do lixo recolhido (2002-2022)': {
        'fonte': "Fonte: [Data.Rio - Total do lixo recolhido através de coleta seletiva e total recuperado](https://www.data.rio/documents/4b74be782816403f9fda15df584d01f2/about)",
        'periodo': 'Período: 2002-2022'
    },
    'Lixo domiciliar (1990-2023)': {
        'fonte': "Fonte: [Data.Rio - Lixo domiciliar coletado por ano](https://www.data.rio/documents/PCRJ::-total-do-lixo-domiciliar-e-p%C3%BAblico-coletados-por-ano-segundo-%C3%A1reas-de-planejamento-ap-regi%C3%B5es-de-planejamento-rp-e-regi%C3%B5es-administrativas-ra-no-munic%C3%ADpio-do-rio-de-janeiro-entre-1990-2023/about)",
        'periodo': 'Período: 1990-2023'
    },
    'Lixo público (1990-2023)': {
        'fonte': "Fonte: [Data.Rio - Lixo público coletado por ano](https://www.data.rio/documents/PCRJ::-total-do-lixo-domiciliar-e-p%C3%BAblico-coletados-por-ano-segundo-%C3%A1reas-de-planejamento-ap-regi%C3%B5es-de-planejamento-rp-e-regi%C3%B5es-administrativas-ra-no-munic%C3%ADpio-do-rio-de-janeiro-entre-1990-2023/about)",
        'periodo': 'Período: 1990-2023'
    },
    'Análise de lixo domiciliar por bairro': {
        'fonte': "Fonte: [Data.Rio - Lixo domiciliar coletado por ano](https://www.data.rio/documents/PCRJ::-total-do-lixo-domiciliar-e-p%C3%BAblico-coletados-por-ano-segundo-%C3%A1reas-de-planejamento-ap-regi%C3%B5es-de-planejamento-rp-e-regi%C3%B5es-administrativas-ra-no-munic%C3%ADpio-do-rio-de-janeiro-entre-1990-2023/about)",
        'periodo': 'Período: 1990-2023'
    },
    'Análise de lixo público por bairro': {
        'fonte': "Fonte: [Data.Rio - Lixo público coletado por ano](https://www.data.rio/documents/PCRJ::-total-do-lixo-domiciliar-e-p%C3%BAblico-coletados-por-ano-segundo-%C3%A1reas-de-planejamento-ap-regi%C3%B5es-de-planejamento-rp-e-regi%C3%B5es-administrativas-ra-no-munic%C3%ADpio-do-rio-de-janeiro-entre-1990-2023/about)",
        'periodo': 'Período: 1990-2023'
    },
    'Comparações': {
        'fonte': "Fonte: [Data.Rio - Total anual de lixo municipal disposto nos aterros](https://www.data.rio/documents/24cf719960024b8aa2987009700f7479/about)",
        'periodo': 'Período: 1995-2023'
    }
}
        
        if st.session_state['data'] is None:
                (st.session_state['data'], st.session_state['data_dom'], 
                 st.session_state['data_pub'], st.session_state['data_comp']) = load_data()
        
        dados_selecionados = st.sidebar.radio("Selecione a tabela de dados:", list(opcoes.keys()))
        
        st.subheader(f"Tabela: {dados_selecionados}")
        st.write(descricoes[dados_selecionados]['fonte'])
        st.write(descricoes[dados_selecionados]['periodo'])
        st.markdown("---")
        
        chave_dados = opcoes[dados_selecionados]
        df = st.session_state[chave_dados]
        st.dataframe(df)

        st.title("Visualizações e análises")

        if dados_selecionados == 'Total do lixo recolhido (2002-2022)':

            st.markdown("""
            - Lixo recolhido por coleta seletiva: Total inicial de resíduos coletados de forma organizada (por agentes parceiros da prefeitura), sem garantia de que todo o material será reciclado.
            - Lixo recuperado total: Resíduos que foram efetivamente separados e enviados para reciclagem, representando o resultado final do tratamento dos resíduos.
            """)
            
            colunas_para_plot = ['Lixo recolhido por coleta seletiva (t) (CS026)', 'Lixo Recuperado Total (t)']
            cores = ['green', 'blue']
            marcadores = ['o', 's']
    
            fig, ax = plt.subplots(figsize=(10, 6))

            df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce')
            df = df.sort_values(by='Ano')

            for coluna, cor, marcador in zip(colunas_para_plot, cores, marcadores):
                df.plot(
                    x='Ano', 
                    y=coluna, 
                    kind='line', 
                    ax=ax, 
                    marker=marcador, 
                    color=cor, 
                    label=coluna
        )
            
            ax.set_title("Total de lixo recolhido por ano (2002-2022)", fontsize=16)
            ax.set_xlabel("Ano", fontsize=12)
            ax.set_ylabel("Toneladas", fontsize=12)
            ax.set_xticks(df['Ano'])
            ax.set_xticklabels(df['Ano'], rotation=45, ha='right')
            ax.grid(True)
            st.pyplot(fig)

            st.write("""
                    1. O que explica a queda repentina no volume de lixo recolhido entre 2017 e 2018?
                    2. O crescimento de lixo entre 2019 e 2020 é reflexo da pandemia, maior registro de dados ou implementação de alguma política em específico?
                    3. Quais os incentivos ou ações tomadas que possibilitaram o aumento no recolhimento de lixo via coleta seletiva?
                     """)
            
            st.markdown("---")

            colunas_materiais = [
                'Papel e papelão (CS010)', 
                'Plásticos (CS011)', 
                'Metais (CS012)', 
                'Vidro (CS013)', 
                'Outros (CS014)'
                ]
            cores = ['brown', 'orange', 'gray', 'purple', 'pink']
            marcadores = ['o', 's', 'd', '^', 'x']

            fig, ax = plt.subplots(figsize=(12, 7))

            df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce')
            df = df.sort_values(by='Ano')

            for coluna, cor, marcador in zip(colunas_materiais, cores, marcadores):
                df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
                df.plot(
                    x='Ano', 
                    y=coluna, 
                    kind='line', 
                    ax=ax, 
                    marker=marcador, 
                    color=cor, 
                    label=coluna
                )

            ax.set_title("Distribuição dos materiais recolhidos por ano (2002-2022)", fontsize=16)
            ax.set_xlabel("Ano", fontsize=12)
            ax.set_ylabel("Toneladas", fontsize=12)
            ax.set_xticks(df['Ano'])
            ax.set_xticklabels(df['Ano'].astype(str), rotation=45, ha='right')
            ax.legend(title="Materiais", fontsize=10, title_fontsize=12)
            ax.grid(True)
            st.pyplot(fig)

            st.write("""
                    1. O que explica a grande oscilação no volume de recolhimento de alguns materiais?
                    2. Quais externalidades impactam no volume de lixo recolhido? Megaeventos como olimpíadas? Flutuações do próprio mercado de resíduos?
                     """)
            
            st.markdown("---")

        elif dados_selecionados == 'Lixo domiciliar (1990-2023)':

            colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns
            colunas_categoricas = df.select_dtypes(exclude=['float64', 'int64']).columns
            df[colunas_numericas] = df[colunas_numericas].apply(pd.to_numeric, errors="coerce").fillna(0)

            total_domiciliar = df[colunas_numericas].sum().sum()
            total_domiciliar_str = f"{total_domiciliar:,.2f}"
            st.metric(label="Total de lixo público (Toneladas)", value=total_domiciliar_str)
            
            colunas_anos = df.columns[2:]
            df_total_por_ano = df[colunas_anos].sum()
            
            st.write("Volume total de resíduos por ano:", df_total_por_ano)

            fig, ax = plt.subplots(figsize=(14, 8))
            df_total_por_ano.plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title("Evolução total de resíduos (t) por ano (1990-2023)", fontsize=16)
            ax.set_xlabel("Ano", fontsize=12)
            ax.set_ylabel("Toneladas de lixo por milhão", fontsize=12)
            ax.grid(axis='y')
            st.pyplot(fig)
            
            st.markdown("---")

            st.subheader('Mapa de calor por bairro e ano')
    
            heatmap_data = df.set_index('Bairro').iloc[:, 1:]
            
            fig, ax = plt.subplots(figsize=(14, 8))
            sns.heatmap(heatmap_data, cmap='YlGnBu', cbar_kws={'label': 'Toneladas de Lixo'}, ax=ax)
            ax.set_title('Intensidade de lixo por bairro e ano (1990-2023)', fontsize=14)
            ax.set_xlabel('Ano')
            ax.set_ylabel('Bairro')
            st.pyplot(fig)


        elif dados_selecionados == 'Lixo público (1990-2023)':
           
            colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns
            colunas_categoricas = df.select_dtypes(exclude=['float64', 'int64']).columns
            df[colunas_numericas] = df[colunas_numericas].apply(pd.to_numeric, errors="coerce").fillna(0)

            total_publico = df[colunas_numericas].sum().sum()
            total_publico_str = f"{total_publico:,.2f}"
            st.metric(label="Total de lixo público (Toneladas)", value=total_publico_str)

            
            colunas_anos = df.columns[2:]

            df_total_por_ano = df[colunas_anos].sum()
            
            st.write("Volume total de resíduos por ano:", df_total_por_ano)

            fig, ax = plt.subplots(figsize=(14, 8))
            df_total_por_ano.plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title("Evolução total de resíduos (t) por ano (1990-2023)", fontsize=16)
            ax.set_xlabel("Ano", fontsize=12)
            ax.set_ylabel("Toneladas de lixo por milhão", fontsize=12)
            ax.grid(axis='y')
            st.pyplot(fig)

            st.markdown("---")

            st.subheader('Mapa de calor por bairro e ano')
    
            heatmap_data = df.set_index('Bairro').iloc[:, 1:]
            
            fig, ax = plt.subplots(figsize=(14, 8))
            sns.heatmap(heatmap_data, cmap='YlGnBu', cbar_kws={'label': 'Toneladas de Lixo'}, ax=ax)
            ax.set_title('Intensidade de lixo por bairro e ano (1990-2023)', fontsize=14)
            ax.set_xlabel('Ano')
            ax.set_ylabel('Bairro')
            st.pyplot(fig)

        
        elif dados_selecionados == 'Análise de lixo domiciliar por bairro':

            st.title('Análise detalhada por bairro')

            bairros = df['Bairro'].unique()
            bairro_selecionado = st.selectbox('Selecione um bairro:', bairros)

            if bairro_selecionado:
                df_bairro = df[df['Bairro'] == bairro_selecionado].set_index('Bairro')
                volumes_por_ano = df_bairro.loc[bairro_selecionado, '1990':'2023']
                
                st.write(f"Volumes de resíduos por ano no bairro {bairro_selecionado}:")
                st.dataframe(volumes_por_ano)

            tipo_grafico = st.selectbox(
                "Escolha o tipo de gráfico para exibir",
                ["Gráfico de Barras", "Gráfico de Linha", "Gráfico de Área", "Heatmap"]
            )

            if tipo_grafico == "Gráfico de Barras":
                st.subheader(f"Gráfico de Barras - Volume de Resíduos no Bairro {bairro_selecionado}")
                
                fig, ax = plt.subplots(figsize=(14, 8))
                volumes_por_ano.plot(kind='bar', ax=ax, color='orange', alpha=0.7)
                ax.set_title(f"Volume de resíduos no bairro {bairro_selecionado} por ano", fontsize=16)
                ax.set_xlabel("Ano", fontsize=12)
                ax.set_ylabel("Toneladas de lixo", fontsize=12)
                ax.grid(axis='y', linestyle='--', alpha=0.7)
                st.pyplot(fig)

                st.markdown('---')
            
            elif tipo_grafico == "Gráfico de Linha":
                st.subheader(f"Gráfico de Linha - Volume de Resíduos no Bairro {bairro_selecionado}")
                
                fig, ax = plt.subplots(figsize=(14, 8))
                volumes_por_ano.T.plot(kind='line', ax=ax, marker='o', color='green')
                ax.set_title(f"Evolução do volume de resíduos no bairro {bairro_selecionado}", fontsize=16)
                ax.set_xlabel("Ano", fontsize=12)
                ax.set_ylabel("Toneladas de lixo", fontsize=12)
                ax.grid(axis='y')
                st.pyplot(fig)

                st.markdown('---')

            elif tipo_grafico == "Gráfico de Área":
                st.subheader(f"Gráfico de Área - Volume de Resíduos no Bairro {bairro_selecionado}")
                
                fig, ax = plt.subplots(figsize=(14, 8))
                volumes_por_ano.T.plot(kind='area', ax=ax, color='lightgreen', alpha=0.6)
                ax.set_title(f"Evolução acumulativa do volume de resíduos no bairro {bairro_selecionado}", fontsize=16)
                ax.set_xlabel("Ano", fontsize=12)
                ax.set_ylabel("Toneladas de lixo", fontsize=12)
                ax.grid(axis='y')
                st.pyplot(fig)

                st.markdown('---')

            elif tipo_grafico == "Heatmap":
                st.subheader(f"Heatmap - Volume de Resíduos no Bairro {bairro_selecionado}")
                
                volumes_por_ano_numeric = volumes_por_ano.astype(float)

                fig, ax = plt.subplots(figsize=(14, 8))
                sns.heatmap(
                    volumes_por_ano_numeric.values.reshape(1, -1),
                    cmap='YlGnBu',
                    annot=False,
                    fmt='.0f',
                    cbar_kws={'label': 'Toneladas'},
                    xticklabels=volumes_por_ano.index
                )

                ax.set_title(f"Intensidade do volume de resíduos no bairro {bairro_selecionado} por ano", fontsize=16)
                ax.set_xlabel("Ano", fontsize=12)
                ax.set_yticks([])
                plt.xticks(rotation=45, ha='right')

                st.pyplot(fig)

                st.markdown('---')


        elif dados_selecionados == 'Análise de lixo público por bairro':
            st.title('Análise detalhada por bairro')

            bairros = df['Bairro'].unique()
            bairro_selecionado = st.selectbox('Selecione um bairro:', bairros)

            if bairro_selecionado:
                df_bairro = df[df['Bairro'] == bairro_selecionado].set_index('Bairro')
                volumes_por_ano = df_bairro.loc[bairro_selecionado, '1990':'2023']
                
                st.write(f"Volumes de resíduos por ano no bairro {bairro_selecionado}:")
                st.dataframe(volumes_por_ano)
                
                fig, ax = plt.subplots(figsize=(14, 8))
                volumes_por_ano.T.plot(kind='line', ax=ax, marker='o', color='green')
                ax.set_title(f"Evolução do volume de resíduos no bairro {bairro_selecionado}", fontsize=16)
                ax.set_xlabel("Ano", fontsize=12)
                ax.set_ylabel("Toneladas de lixo", fontsize=12)
                ax.grid(axis='y')
                st.pyplot(fig)

                st.markdown('---')

                fig, ax = plt.subplots(figsize=(14, 8))
                volumes_por_ano.T.plot(kind='area', ax=ax, color='lightgreen', alpha=0.6)
                ax.set_title(f"Evolução acumulativa do volume de resíduos no bairro {bairro_selecionado}", fontsize=16)
                ax.set_xlabel("Ano", fontsize=12)
                ax.set_ylabel("Toneladas de lixo", fontsize=12)
                ax.grid(axis='y')
                st.pyplot(fig)

                st.markdown('---')

                volumes_por_ano_numeric = volumes_por_ano.astype(float)

                fig, ax = plt.subplots(figsize=(14, 8))
                sns.heatmap(
                    volumes_por_ano_numeric.values.reshape(1, -1),
                    cmap='YlGnBu',
                    annot=False,
                    fmt='.0f',
                    cbar_kws={'label': 'Toneladas'},
                    xticklabels=volumes_por_ano.index
                )

                ax.set_title(f"Intensidade do volume de resíduos no bairro {bairro_selecionado} por ano", fontsize=16)
                ax.set_xlabel("Ano", fontsize=12)
                ax.set_yticks([])
                plt.xticks(rotation=45, ha='right')

                st.pyplot(fig)


        elif dados_selecionados == 'Comparações':         
            st.subheader("Análise Comparativa: Lixo Público, Domiciliar e Reciclado")

            total_publico = df["Limpeza Pública"].sum()
            total_domiciliar = df["Domiciliar"].sum()
            total_reciclado = df["Lixo Recuperado Total"].sum()
            total_desperdicio = (df["Limpeza Pública"] + df["Domiciliar"] - df["Lixo Recuperado Total"]).sum()

            col1, col2 = st.columns(2)
            col1.metric(label="Total de Lixo Público (Ton)", value=f"{total_publico:,.2f}")
            col2.metric(label="Total de Lixo Domiciliar (Ton)", value=f"{total_domiciliar:,.2f}")
            col3, col4 = st.columns(2)
            col3.metric(label="Total de Lixo Reciclado (Ton)", value=f"{total_reciclado:,.2f}")
            col4.metric(label="Total Desperdiçado (Ton)", value=f"{total_desperdicio:,.2f}")
            
            st.markdown("---")

            st.subheader("Evolução Temporal: Lixo Público, Domiciliar, Reciclado e Desperdiçado")
            fig, ax = plt.subplots(figsize=(14, 8))
            
            ax.plot(df["Ano"], df["Limpeza Pública"], label="Lixo Público", marker="o")
            ax.plot(df["Ano"], df["Domiciliar"], label="Lixo Domiciliar", marker="s")
            ax.plot(df["Ano"], df["Lixo Recuperado Total"], label="Lixo Reciclado", marker="^")
            ax.plot(df["Ano"], 
                    df["Limpeza Pública"] + df["Domiciliar"] - df["Lixo Recuperado Total"], 
                    label="Lixo Desperdiçado", linestyle="--")
            
            ax.set_title("Comportamento dos dados ao longo do tempo", fontsize=16)
            ax.set_xlabel("Ano", fontsize=12)
            ax.set_ylabel("Toneladas de Lixo em milhão", fontsize=12)
            ax.legend()
            ax.grid(axis="y")
            st.pyplot(fig)
            
            st.markdown("---")

            st.subheader("Distribuição Acumulada de Lixo por Categoria")
            fig, ax = plt.subplots(figsize=(14, 8))
            
            df_totais = {
                "Lixo Público": total_publico,
                "Lixo Domiciliar": total_domiciliar,
                "Lixo Reciclado": total_reciclado,
                "Lixo Desperdiçado": total_desperdicio
            }
            categorias = list(df_totais.keys())
            valores = list(df_totais.values())
            
            ax.bar(categorias, valores, color=["#4CAF50", "#2196F3", "#FFC107", "#F44336"])
            ax.set_title("Distribuição Total de Lixo (1990-2023)", fontsize=16)
            ax.set_ylabel("Toneladas de Lixo", fontsize=12)
            ax.set_xlabel("Categoria", fontsize=12)
            for i, v in enumerate(valores):
                ax.text(i, v + 0.02 * max(valores), f"{v:,.2f}", ha="center", fontsize=10, color="black")
            st.pyplot(fig)
            
            st.markdown("---")    


    
elif menu == 'Wikipedia':
    with open('C:\\Users\\User\\Documents\\CDD\\PB\\conteudo_reciclagem.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    st.subheader("Conteúdo extraído da página sobre Reciclagem")
    if st.session_state['wordcloud'] is None:
        content = load_txt_file()
        st.session_state['wordcloud'] = generate_wordcloud(content)
        st.write(content[:500] + "...")
    st.write(content[:482] + "...")

    # Gerando e exibindo a nuvem de palavras
    wordcloud = generate_wordcloud(content)
    st.subheader("Nuvem de Palavras")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

elif menu == 'Serviço de download/upload':
    st.title('Serviço de Download/Upload')
    
    if 'data' not in st.session_state or st.session_state['data'] is None:
        st.session_state['data'] = load_data()

    st.subheader('Tabela de Dados Existente')
    if not st.session_state['data'].empty:
        st.dataframe(st.session_state['data'])
    else:
        st.warning("Nenhum dado disponível.")

    st.subheader("Upload de Novos Dados")
    uploaded_data = upload_file()

    # Processa os dados carregados
    if uploaded_data is not None:
        if list(uploaded_data.columns) == list(st.session_state['data'].columns):
            st.success("Colunas coincidem. Dados adicionados com sucesso!")
            st.session_state['data'] = pd.concat([st.session_state['data'], uploaded_data], ignore_index=True)

            st.subheader("Dados Atualizados")
            st.dataframe(st.session_state['data'])
        else:
            st.error("As colunas do arquivo carregado não coincidem com as colunas existentes!")

    st.subheader("Download dos Dados Atualizados")
    if not st.session_state['data'].empty:
        st.download_button(
            label="Baixar CSV",
            data=convert_to_csv(st.session_state['data']),
            file_name="dados_atualizados.csv",
            mime="text/csv"
        )
    else:
        st.warning("Nenhum dado para download.")
      
elif menu == 'Recursos de IA via LLM':
    st.title('Recursos de IA via LLM')

    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    if prompt := st.chat_input("Tire aqui sua dúvida sobre reciclagem:"):
        # Adiciona a mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Estou pensando"):
                try:
                    # Preparando o payload corretamente
                    payload = {
                        "messages": [
                            {
                                "role": msg["role"],
                                "content": msg["content"]
                            } for msg in st.session_state.messages
                        ]
                    }
                    
                    response = requests.post(
                    "http://localhost:8000/chat/",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                    
                    if response.status_code == 200:
                        response = response.json()
                        if "response" in response:
                            st.markdown(response["response"])
                            st.session_state.messages.append({"role": "assistant", "content": response["response"]})
                        else:
                            st.error("Formato de resposta inválido do servidor.")
                    else:
                        st.error(f"Erro na API: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    st.error(f"Erro ao comunicar com a API: {str(e)}")

    # Limita o número de mensagens armazenadas
    max_messages = 10
    if len(st.session_state.messages) > max_messages:
        st.session_state.messages = st.session_state.messages[-max_messages:]