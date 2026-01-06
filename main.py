# Importa o módulo necessário do moviepy para manipulação de áudio e vídeo
from moviepy.editor import AudioFileClip

# Importa o módulo uuid para gerar identificadores únicos
import uuid


# Certifique-se de que o pacote `assemblyai` esteja instalado. 
# Você pode instalá-lo facilmente com o comando `pip install -U assemblyai`.
#
# Nota para usuários macOS: use `pip3` se `pip` estiver associado a outra versão do Python.

import assemblyai as aai

import streamlit as st



# Define uma função chamada 'mp4_to_mp3' que converte um arquivo MP4 em formato MP3
def mp4_to_mp3(mp4, mp3):
    try:
        # Cria um objeto de áudio a partir do arquivo MP4 utilizando a classe AudioFileClip
        filetoconvert = AudioFileClip(mp4)

        # Grava o áudio extraído do arquivo MP4 em formato MP3
        filetoconvert.write_audiofile(mp3)

        # Fecha o objeto de áudio para liberar recursos do sistema
        filetoconvert.close()

    except FileNotFoundError:
        # Esta exceção é capturada caso o arquivo MP4 não seja encontrado
        print(f"Erro: O arquivo MP4 '{mp4}' não foi encontrado.")

    except Exception as e:
        # Captura qualquer outra exceção e imprime a mensagem de erro
        print(f"Ocorreu um erro durante a conversão: {e}")




# Função para converter um arquivo de áudio MP3 em texto usando o serviço AssemblyAI.
def mp3_to_text(aai, filename, s_labels, s_expected, l_code):
    try:
        # Configura as opções de transcrição, incluindo rótulos de falantes,
        # o número esperado de falantes e o código de idioma do áudio.
        config = aai.TranscriptionConfig(
            speaker_labels=s_labels,  # Define se os rótulos dos falantes devem ser incluídos.
            speakers_expected=s_expected,  # Número esperado de falantes no áudio.
            language_code=l_code  # Define o código de idioma, como 'pt' para português.
        )

        # Cria uma instância do Transcriber, que será usada para realizar a transcrição.
        transcriber = aai.Transcriber()

        # Transcreve o arquivo MP3 usando as configurações especificadas.
        transcript = transcriber.transcribe(
            filename,
            config=config
        )

        # Retorna a transcrição gerada pela API.
        return transcript

    except FileNotFoundError:
        # Captura o erro se o arquivo de áudio não for encontrado.
        print("Erro: o arquivo especificado não foi encontrado.")
    except Exception as e:
        # Captura quaisquer outras exceções ocorridas durante a execução.
        print(f"Ocorreu um erro: {e}")



# Function that takes parameters
def update_message(text_id):
    st.session_state.messages[text_id].text = st.session_state[f"textarea_{text_id}"]




def gerar_transcricao(mp3_local_filename):

        # Define o caminho do arquivo MP4 local que será convertido
        mp4_local_filename = "YTDown.com_YouTube_Media_7L9A6KhIpDA_006_144p.mp4"

        # Chama a função para converter o arquivo MP4 em MP3
        mp4_to_mp3(mp4_local_filename, mp3_local_filename)


        # Defina sua chave de API fornecida pelo AssemblyAI. Isso é essencial para autenticação.
        aai.settings.api_key = "617454231d6f40d7b1ab95fb818b5d3c"

        # Chama a função de transcrição com as configurações desejadas.
        transcript = mp3_to_text(
            aai, 
            filename=mp3_local_filename, 
            s_labels=True,  # Habilita os rótulos dos falantes no resultado da transcrição.
            s_expected=2,   # Espera que o áudio contenha 2 falantes.
            l_code='pt'     # Define o idioma do áudio como português.
        )

        if transcript:
            st.session_state.messages = {}
            # Itera sobre as fala transcritas e imprime cada fala com o número do falante.
            for utterance in transcript.utterances:
                text_id = f"{uuid.uuid4().hex}"
                st.session_state.messages[text_id] = utterance




def preencher_pagina(mp3_local_filename):

    # Se a transcrição foi bem-sucedida, exibe as falas dos falantes.
    if st.session_state.messages:
        # Itera sobre as fala transcritas e imprime cada fala com o número do falante.
        for text_id, utterance in st.session_state.messages.items():

            # Exibe o número do falante e o texto correspondente.
            st.write(f"Speaker {utterance.speaker}: {utterance.text}")

            col11, col12 = st.columns(2)
            with col11:
                st.audio(mp3_local_filename, format="audio/mpeg", start_time=utterance.start/1000)
            with col12:
                with st.popover("Atualizar texto"):
                    st.markdown("Insira o texto correto")
                    st.text_area("Novo texto", value=utterance.text, key=f"textarea_{text_id}")
                    st.button('📨 Atualizar', key=f"btn_{uuid.uuid4().hex}", on_click=update_message, kwargs={"text_id": text_id})

    



# Verifica se o script está sendo executado como o programa principal
if __name__ == "__main__":

    # Gera um nome de arquivo único para o arquivo MP3 usando uuid para evitar colisões de nome
    if "mp3_local_filename" not in st.session_state:
        st.session_state.mp3_local_filename = f"{uuid.uuid4().hex}.mp3"

    if "messages" not in st.session_state:
        gerar_transcricao(st.session_state.mp3_local_filename)
        preencher_pagina(st.session_state.mp3_local_filename)

    else:
        preencher_pagina(st.session_state.mp3_local_filename)
        pass

    # st.write(st.session_state["messages"])

