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
    data90 = pd.read_csv('C:/Users/User/Documents/CDD/PB/1481.xlsx - Dom-1990-1999.csv')
    data00 = pd.read_csv('C:/Users/User/Documents/CDD/PB/1481.xlsx - Dom-2000-2009.csv')
    data10 = pd.read_csv('C:/Users/User/Documents/CDD/PB/1481.xlsx - Dom-2010-2019.csv')
    data20 = pd.read_csv('C:/Users/User/Documents/CDD/PB/1481.xlsx - Dom-2020-2023.csv')
    return data, data90, data00, data10, data20

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
if 'data90' not in st.session_state:
    st.session_state['data90'] = None
if 'data00' not in st.session_state:
    st.session_state['data00'] = None
if 'data10' not in st.session_state:
    st.session_state['data10'] = None
if 'data20' not in st.session_state:
    st.session_state['data20'] = None
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

# Upload de novos dados CSV
def upload_file():
    uploaded_file = st.file_uploader("Escolha um arquivo CSV para upload", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data
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
                 
        Nesta fase beta da aplicação, pode ser encontrada algumas notícias úteis que dão a dimensão do problema na cidade do RJ, além de algumas análises feitas sob os dados produzidos pelo portal Data.Rio
                 
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


        st.markdown("---")

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
                  'Lixo domiciliar (1990-1999)': 'data90',
                  'Lixo domiciliar (2000-2009)': 'data00',
                  'Lixo domiciliar (2010-2019)': 'data10',
                  'Lixo domiciliar (2020-2023)': 'data20'}
        
        descricoes = {
    'Total do lixo recolhido (2002-2022)': {
        'fonte': "Fonte: [Data.Rio - Total do lixo recolhido através de coleta seletiva e total recuperado](https://www.data.rio/documents/4b74be782816403f9fda15df584d01f2/about)",
        'periodo': 'Período: 2002-2022'
    },
    'Lixo domiciliar (1990-1999)': {
        'fonte': "Fonte: [Data.Rio - Lixo domiciliar coletado por ano](https://www.data.rio/documents/PCRJ::-total-do-lixo-domiciliar-e-p%C3%BAblico-coletados-por-ano-segundo-%C3%A1reas-de-planejamento-ap-regi%C3%B5es-de-planejamento-rp-e-regi%C3%B5es-administrativas-ra-no-munic%C3%ADpio-do-rio-de-janeiro-entre-1990-2023/about)",
        'periodo': 'Período: 1990-1999'
    },
    'Lixo domiciliar (2000-2009)': {
        'fonte': "Fonte: [Data.Rio - Lixo domiciliar coletado por ano](https://www.data.rio/documents/PCRJ::-total-do-lixo-domiciliar-e-p%C3%BAblico-coletados-por-ano-segundo-%C3%A1reas-de-planejamento-ap-regi%C3%B5es-de-planejamento-rp-e-regi%C3%B5es-administrativas-ra-no-munic%C3%ADpio-do-rio-de-janeiro-entre-1990-2023/about)",
        'periodo': 'Período: 2000-2009'
    },
    'Lixo domiciliar (2010-2019)': {
        'fonte': "Fonte: [Data.Rio - Lixo domiciliar coletado por ano](https://www.data.rio/documents/PCRJ::-total-do-lixo-domiciliar-e-p%C3%BAblico-coletados-por-ano-segundo-%C3%A1reas-de-planejamento-ap-regi%C3%B5es-de-planejamento-rp-e-regi%C3%B5es-administrativas-ra-no-munic%C3%ADpio-do-rio-de-janeiro-entre-1990-2023/about)",
        'periodo': 'Período: 2010-2019'
    },
    'Lixo domiciliar (2020-2023)': {
        'fonte': "Fonte: [Data.Rio - Lixo domiciliar coletado por ano](https://www.data.rio/documents/PCRJ::-total-do-lixo-domiciliar-e-p%C3%BAblico-coletados-por-ano-segundo-%C3%A1reas-de-planejamento-ap-regi%C3%B5es-de-planejamento-rp-e-regi%C3%B5es-administrativas-ra-no-munic%C3%ADpio-do-rio-de-janeiro-entre-1990-2023/about)",
        'periodo': 'Período: 2020-2023'
    }
}
        
        if st.session_state['data'] is None:
                (st.session_state['data'], st.session_state['data90'], 
                 st.session_state['data00'], st.session_state['data10'], 
                 st.session_state['data20']) = load_data()
        
        dados_selecionados = st.sidebar.radio("Selecione a tabela de dados:", list(opcoes.keys()))
        
        st.subheader(f"Tabela: {dados_selecionados}")
        st.write(descricoes[dados_selecionados]['fonte'])
        st.write(descricoes[dados_selecionados]['periodo'])
        st.markdown("---")
        
        chave_dados = opcoes[dados_selecionados]
        df = st.session_state[chave_dados]
        st.dataframe(df)

        st.subheader("Visualizações e análises")

        if dados_selecionados == 'Total do lixo recolhido (2002-2022)':

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
            
            ax.set_title("Total de Lixo Recolhido por Ano (2002-2022)", fontsize=16)
            ax.set_xlabel("Ano", fontsize=12)
            ax.set_ylabel("Toneladas", fontsize=12)
            ax.set_xticks(df['Ano'])
            ax.set_xticklabels(df['Ano'], rotation=45, ha='right')
            ax.grid(True)
            st.pyplot(fig)

            st.write("""
                    1. O que explica a queda repentina no volume de lixo recolhido entre 2017 e 2018?
                    2. O crescimento de lixo entre 2019 e 2020 é reflexo da pandemia, maior registro de dados ou implementação de alguma política em específico?
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

        elif dados_selecionados == 'Lixo domiciliar (1990-1999)':

            df.replace("...", np.nan, inplace=True)
            df.iloc[:, 2:] = df.iloc[:, 2:].apply(lambda x: x.str.replace(" ", "").astype(float))
            df = df.fillna(0)
            for col in df.columns[2:]:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(int)

            
            colunas_anos = df.columns[2:]
            for coluna in colunas_anos:
                df[coluna] = df[coluna].replace(['...', '-'], 0)
                df[coluna] = pd.to_numeric(df[coluna], errors='coerce').fillna(0)

            df_total_por_ano = df[colunas_anos].sum()
            
            st.write("Volume total de resíduos por ano:", df_total_por_ano)

            fig, ax = plt.subplots(figsize=(10, 6))
            df_total_por_ano.plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title("Evolução total de resíduos (t) por ano (1990-1999)", fontsize=16)
            ax.set_xlabel("Ano", fontsize=12)
            ax.set_ylabel("Quantidade total de resíduos (t)", fontsize=12)
            ax.grid(axis='y')
            st.pyplot(fig)

            st.write("""
                    1. O que explica a queda no volume de lixo em 1995?
                     """)
            
            st.markdown("---")


        elif dados_selecionados == 'Lixo domiciliar (2000-2009)':
            df.replace("...", np.nan, inplace=True)
            df.iloc[:, 2:] = df.iloc[:, 2:].apply(lambda x: x.str.replace(" ", "").astype(float))
            df = df.fillna(0)
            for col in df.columns[2:]:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(int)

            
            colunas_anos = df.columns[2:]
            for coluna in colunas_anos:
                df[coluna] = df[coluna].replace(['...', '-'], 0)
                df[coluna] = pd.to_numeric(df[coluna], errors='coerce').fillna(0)

            df_total_por_ano = df[colunas_anos].sum()
            
            st.write("Volume total de resíduos por ano:", df_total_por_ano)

            fig, ax = plt.subplots(figsize=(10, 6))
            df_total_por_ano.plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title("Evolução total de resíduos (t) por ano (2000-2009)", fontsize=16)
            ax.set_xlabel("Ano", fontsize=12)
            ax.set_ylabel("Quantidade total de resíduos (t)", fontsize=12)
            ax.grid(axis='y')
            st.pyplot(fig)

        
        elif dados_selecionados == 'Lixo domiciliar (2010-2019)':
            df.replace("...", np.nan, inplace=True)
            df.iloc[:, 2:] = df.iloc[:, 2:].apply(lambda x: x.str.replace(" ", "").astype(float))
            df = df.fillna(0)
            for col in df.columns[2:]:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(int)

            
            colunas_anos = df.columns[2:]
            for coluna in colunas_anos:
                df[coluna] = df[coluna].replace(['...', '-'], 0)
                df[coluna] = pd.to_numeric(df[coluna], errors='coerce').fillna(0)

            df_total_por_ano = df[colunas_anos].sum()
            
            st.write("Volume total de resíduos por ano:", df_total_por_ano)

            fig, ax = plt.subplots(figsize=(10, 6))
            df_total_por_ano.plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title("Evolução total de resíduos (t) por ano (2010-2019)", fontsize=16)
            ax.set_xlabel("Ano", fontsize=12)
            ax.set_ylabel("Quantidade total de resíduos (t)", fontsize=12)
            ax.grid(axis='y')
            st.pyplot(fig)


        elif dados_selecionados == 'Lixo domiciliar (2020-2023)':
            df.replace("...", np.nan, inplace=True)
            df.iloc[:, 2:] = df.iloc[:, 2:].apply(lambda x: x.str.replace(" ", "").astype(float))
            df = df.fillna(0)
            for col in df.columns[2:]:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(int)

            
            colunas_anos = df.columns[2:]
            for coluna in colunas_anos:
                df[coluna] = df[coluna].replace(['...', '-'], 0)
                df[coluna] = pd.to_numeric(df[coluna], errors='coerce').fillna(0)

            df_total_por_ano = df[colunas_anos].sum()
            
            st.write("Volume total de resíduos por ano:", df_total_por_ano)

            fig, ax = plt.subplots(figsize=(10, 6))
            df_total_por_ano.plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title("Evolução total de resíduos (t) por ano (2020-2023)", fontsize=16)
            ax.set_xlabel("Ano", fontsize=12)
            ax.set_ylabel("Quantidade total de resíduos (t)", fontsize=12)
            ax.grid(axis='y')
            st.pyplot(fig)


    
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
      st.title('Serviço de download/upload')
      st.subheader('Tabela de dados')
      if st.session_state['data'] is None:
           st.session_state['data'] = load_data()
      st.dataframe(st.session_state['data'])

      data = load_data()

    # Serviço de upload de arquivos CSV
      st.subheader("Upload de Novos Dados")
      uploaded_data = upload_file()

    # Se o usuário fez upload de novos dados, concatenar com os dados existentes
      if uploaded_data is not None:
        st.write("Novos dados adicionados:")
        st.dataframe(uploaded_data)

        # Concatenar os dados existentes com os dados enviados pelo usuário
        data = pd.concat([data, uploaded_data], ignore_index=True)

    # Exibindo os dados atualizados
      st.subheader("Dados Atualizados")
      st.dataframe(data)

    # Serviço de download dos dados atualizados
      st.subheader("Download dos Dados Atualizados")
      st.download_button(
           label="Baixar CSV",
           data=download_file(data),
           file_name="dados_atualizados.csv",
           mime="text/csv"
           )
      
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