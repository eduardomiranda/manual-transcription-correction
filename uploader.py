import sys
  
# append the path of the parent directory
sys.path.append(".")


import streamlit as st
from datetime import datetime
import pytz
import os
import logging
import time
from pathlib import Path

from PyUtilityKit import file_utils
from PyUtilityKit import gcp_utils
from PyUtilityKit import email_utils
from PyUtilityKit import mongo_utils
from PyUtilityKit import logging_utils

import newrelic.agent
# newrelic.agent.initialize('newrelic.ini', env.lower(),  ignore_errors=False)


timezone = st.secrets['system'].get("timezone", '')

mongodb_uri        = st.secrets['mongodb'].get('mongodb_uri', '')
mongodb_db         = st.secrets['mongodb'].get('mongodb_db', '')
mongodb_collection = st.secrets['mongodb'].get('mongodb_collection', '')

bucket_name = st.secrets['gcp'].get('bucket_name', '')
service_account_json_string = st.secrets['gcp'].get('service_account_json_string', '')

sender        = st.secrets['email'].get('sender', '')
password      = st.secrets['email'].get('password', '')
destinatarios = st.secrets['email'].get('destinatarios', '')


logging_utils.iniciaLogging('logs/uploader.log', logging.INFO, '' )
logger = logging.getLogger('')


def estao_todos_campos_preenchidos(**kwargs):

	for arg in kwargs.values():
	    if len( arg.strip() ) == 0:
		    return False
	return True



def validate_email(email):
	import re

	# Define a regex pattern for email validation
	pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

	# Use the match function to search for a match between the pattern and the email
	if re.match(pattern, email):
	    return True
	else:
	    return False


def __adicona_div_container_content(div_container_content):

	# Create HTML version
	html_body = f"""<!DOCTYPE html>
					<html lang="pt-BR">
					<head>
					<meta charset="UTF-8">
					<meta name="viewport" content="width=device-width, initial-scale=1.0">
					<style>
						body {{
							font-family: Arial, sans-serif;
						}}
						.container {{
							max-width: 600px;
							margin: 0 auto;
							padding: 20px;
							border: 1px solid #ccc;
						}}
						.heading {{
							text-align: center;
							margin-bottom: 20px;
						}}
						.details {{
							margin-bottom: 20px;
						}}
						.footer {{
							text-align: center;
							margin-top: 20px;
						}}
					</style>
				</head>
				<body>
					<div>{div_container_content}</div>
				</body>
				</html>
				"""
					# <div class="container">{div_container_content}</div>

	return html_body


def criar_html_de_confirmacao_de_recebimento(nome_terapeuta, nome_paciente, data_hora_sessao):

	div_container_content = f"""<p>Olá {nome_terapeuta},<br><br>Informamos que o arquivo de áudio enviado foi recebido com sucesso e encontra-se em processamento para geração da transcrição.</p> 
								<div class="details">

								<h4>Informações fornecidas:</h4>
								<ul>
									<li><p><strong>Nome do terapeuta:</strong> {nome_terapeuta}</p></li>
									<li><p><strong>Nome do paciente:</strong> {nome_paciente}</p></li>
									<li><p><strong>Data e hora da sessão:</strong> {data_hora_sessao}</p></li>
								</ul>
								</div>
								
								<p>Após a conclusão, a transcrição poderá ser utilizada como <strong>material de apoio à organização do conteúdo clínico e à reflexão técnica</strong>, respeitando a autonomia profissional e a responsabilidade ética do(a) psicólogo(a).</p>
								<p>Reforçamos que a Brainn Care atua exclusivamente como <strong>ferramenta de suporte</strong>, não realizando diagnósticos, não emitindo conclusões clínicas finais e não substituindo a escuta, o julgamento técnico ou a responsabilidade profissional.</p>
								<p>Caso o conteúdo contenha informações sensíveis, recomendamos atenção contínua aos princípios de sigilo profissional, conforme o Código de Ética do Psicólogo.</p>

								<p>Você será notificado(a) assim que a transcrição estiver disponível na plataforma.</p>

								<p><br>Atenciosamente,<br><strong>Equipe Brainn Care</strong><br>Plataforma de apoio ético e técnico à prática psicológica</p>"""

	return __adicona_div_container_content(div_container_content)




st.image("brainncare.png")
st.markdown(":small[*Desenvolvido com foco em ética clínica, responsabilidade profissional e segurança da informação.*]")
# st.title("Brainn Care")
st.markdown(":small[Este espaço destina-se ao envio de transcrições de atendimentos psicológicos presenciais, com a finalidade de **apoio à organização do conteúdo clínico e à reflexão técnica do(a) psicólogo(a)**.]")
# st.markdown('A Brainn Care atua como uma **ferramenta de suporte ao raciocínio clínico**, sem substituir a escuta, o julgamento técnico ou a responsabilidade ética do(a) psicólogo(a).')
st.markdown(':small[A Brainn.Care atua como **ferramenta de suporte**, não substituindo a escuta clínica, o raciocínio psicológico, a autonomia profissional nem a responsabilidade técnica do(a) psicólogo(a), conforme previsto no Código de Ética Profissional do Psicólogo.]')
st.markdown(":small[Todo o conteúdo enviado é tratado com **confidencialidade**, respeitando os princípios do sigilo profissional e a legislação vigente (LGPD).]")

# st.subheader("Como funciona", divider="gray")
with st.expander("📌 Como funciona"):
	st.markdown("- :small[Você envia a gravação da sessão presencial.]")
	st.markdown("- :small[A Brainn Care trabalha na transcrição desta gravação e disponibiliza na plataforma.]")
	st.markdown("- :small[Com isso, a Brainn Care pode gerar insumos clínicos auxiliares, como resumos, observações descritivas e hipóteses não diagnósticas.]")
	st.markdown("- :small[Nenhuma decisão clínica é tomada automaticamente. Todo o material gerado deve ser avaliado criticamente pelo profissional.]")

st.divider()


uploaded_file = st.file_uploader("Selecione a gravação da sessão", type = ['.mp3', '.mp4'])


if uploaded_file :

	with st.spinner('Processando'):
		file_name = uploaded_file.name

		# Extract the file extension (suffix)
		file_extension = Path(file_name).suffix

		st.session_state.transcricao_filename = file_utils.generate_random_filename(length=32, extension=file_extension)
		with open(st.session_state.transcricao_filename, 'wb') as file: 
			file.write(uploaded_file.read())


	with st.form(key='my_form', clear_on_submit = True):			

		col11, col12 = st.columns(2)
		col21, col22 = st.columns(2)

		with col11: nome_terapeuta    = st.text_input('Nome do terapeuta')
		with col12: email_terapeuta   = st.text_input('Email do terapeuta')
		with col21: nome_paciente     = st.text_input('Nome do paciente')
		with col22: data_hora_sessao  = st.datetime_input("Data e horário da sessão", value=None)

		st.markdown(":small[Ao enviar este conteúdo, você confirma que possui **autorização ética e legal** para utilizar a gravação e que compreende que a Brainn Care atua como apoio ao trabalho profissional, não como decisora clínica.]")
		if st.form_submit_button(label='╰┈➤ Enviar'):

			if estao_todos_campos_preenchidos( nome_terapeuta=nome_terapeuta, email_terapeuta=email_terapeuta, nome_paciente=nome_paciente, data_hora_sessao=data_hora_sessao.isoformat()):

				if validate_email(email_terapeuta):

					with st.spinner('Processando...'):

						flag_dados_enviados_mongo = False
						flag_envio_comprovante_bucket = False

						try:
							dados = {
							'nome_terapeuta' : nome_terapeuta,
							'email_terapeuta': email_terapeuta,
							'nome_paciente' : nome_paciente,
							'data_hora_sessao' : data_hora_sessao,
							"data_insercao": datetime.now(pytz.timezone(timezone)),
							"filename" : st.session_state.transcricao_filename,
							"status_processamento": False }

							mongo_utils.salva_no_mongo( mongodb_uri, mongodb_db, mongodb_collection, dados )
							flag_dados_enviados_mongo = True

						except Exception as e:
							st.error(f"Um erro ocorreu ao tentar enviar a transcrição [Código do erro: 43AF]", icon="🚨")
							logger.error("Erro ao tentar salvar os dados no MongoDB")
							logger.error(f"{e}")


						if flag_dados_enviados_mongo :
							try:
								# Envia para o bucket no GCP
								local_file_path  = st.session_state.transcricao_filename
								bucket_file_name = st.session_state.transcricao_filename

								gcp_utils.upload_file_to_gcp_bucket(service_account_json_string, bucket_name, local_file_path, bucket_file_name)
								flag_envio_comprovante_bucket = True

							except Exception as e:
								st.error('Um erro ocorreu ao tentar enviar a transcrição [Código do erro: 862C].', icon="🚨")
								logger.error(f"Um erro ocorreu na tentativa de envio das informações para o GCP.")
								logger.error(f"{e}")


						if flag_envio_comprovante_bucket:
							try:
								subject = 'Brainn Care • Gravação de sessão recebida'
								text_body_message = ''
								html_body_message = criar_html_de_confirmacao_de_recebimento(nome_terapeuta, nome_paciente, data_hora_sessao)

								email_utils.enviar_html_email(subject, text_body_message, html_body_message, sender, password, destinatarios + [email_terapeuta], None)
								st.success('Sessão recebida com sucesso!', icon="✅")
								st.markdown("Agora você pode utilizar os recursos da Brainn Care para organizar, refletir e apoiar sua análise clínica, sempre mantendo seu julgamento profissional como referência principal.")

							except Exception as e:
								st.error('Um erro ocorreu ao tentar enviar a transcrição [Código do erro: 42CB].', icon="🚨")
								logger.error(f"Um erro ocorreu na tentativa de envio da confirmação por e-mail.")
								logger.error(f"{e}")

						# Deleta localmente o arquivo utilizado
						file_utils.delete_file_if_exists(st.session_state.transcricao_filename)


				else: st.warning('e-mail incorreto!', icon="⚠️")
			else: st.warning('Foram localizados campos sem preenchimento!', icon="⚠️")



with st.expander("🤝 Finalidade e natureza do material gerado"):
	st.markdown(':small[Os materiais eventualmente produzidos a partir da transcrição possuem caráter auxiliar, descritivo e organizacional, podendo incluir sínteses do conteúdo e hipóteses clínicas não diagnósticas.]')
	st.markdown(':small[Tais materiais não configuram documentos psicológicos formais, nos termos da Resolução CFP nº 06/2019, e não substituem registros clínicos, pareceres, laudos ou relatórios elaborados pelo(a) profissional.]')
	st.markdown(':small[A Brainn.Care **não realiza diagnósticos psicológicos, não emite conclusões clínicas finais** e** não substitui processos avaliativos**, os quais são atribuições exclusivas do(a) psicólogo(a).]')
	st.markdown(':small[Qualquer hipótese apresentada deve ser compreendida como **subsídio técnico preliminar**, cabendo exclusivamente ao(a) profissional a análise crítica, validação e decisão sobre seu uso.]')


# st.subheader("Confidencialidade e proteção de dados", divider="blue")
with st.expander("🔐 Confidencialidade e proteção de dados"):
	st.markdown(":small[Sabemos que o conteúdo clínico é sensível.]")
	st.markdown("- :small[As informações enviadas são utilizadas exclusivamente para o processamento solicitado.]")
	st.markdown("- :small[Não há uso do conteúdo para treinamento público de modelos.]")
	st.markdown("- :small[O acesso é restrito ao usuário autorizado.]")
	st.markdown("- :small[Recomenda-se que o conteúdo não inclua informações pessoais identificáveis além do estritamente necessário para a finalidade clínica.]")
	st.markdown("- :small[O(a) psicólogo(a) permanece como **responsável ético pelo conteúdo enviado**, bem como pelo uso das informações e materiais gerados.]")