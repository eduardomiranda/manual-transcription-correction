import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def enviar_plain_text_email(subject, body, sender, recipients, password):
	msg = MIMEText(body)
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = ', '.join(recipients)

	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
		smtp_server.login(sender, password)
		smtp_server.sendmail(sender, recipients, msg.as_string())



def enviar_html_email(subject, text_body_message, html_body_message, sender, password, recipients, file_path_attach):

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = ', '.join(recipients)

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text_body_message, 'plain')
	part2 = MIMEText(html_body_message, 'html')

	msg.attach(part1)
	msg.attach(part2)

	if file_path_attach:
		part = MIMEBase('application', "octet-stream")
		part.set_payload(open(file_path_attach, "rb").read())
		encoders.encode_base64(part)
		
		basename = os.path.basename(file_path_attach)    
		part.add_header('Content-Disposition', f'attachment; filename="{basename}"')

		msg.attach(part)


	# Send the message via local SMTP server.
	with smtplib.SMTP_SSL('smtp.zoho.com', 465) as smtp_server:
		smtp_server.ehlo()
		# smtp_server.starttls()
		smtp_server.login(sender, password)
		smtp_server.sendmail(sender, recipients, msg.as_string())




# Example usage
if __name__ == "__main__":

	subject = 'Teste'


	text_body_message = '' 

	html_body_message = """
		<html>
			<body>
				<h1>Teste</h1>
				<p>teste</p>
			</body>
		</html>
	"""


	enviar_html_email(subject, text_body_message, html_body_message, sender, password, ['eduardo.dpm@gmail.com'], '/home/eduardo/Pictures/Impacta1.jpg')
	# enviar_html_email(subject, text_body_message, html_body_message, sender, password, ['eduardo.dpm@gmail.com'], None)