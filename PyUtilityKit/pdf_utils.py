from decimal import Decimal, DecimalException
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import csv
import os
import subprocess
import sys

# Encrypt the PDF and add a password
def encrypt(uncompressed, compressed, password):

	# Como usar esse método
	# uncompressed = sys.argv[1]
	# compressed   = sys.argv[2]
	# password     = sys.argv[3]

	# encrypt(uncompressed, compressed, password)

	uncompressedPDFFile = open(uncompressed, 'rb')	
	compressedPDFFile   = open(compressed  , 'wb')

	uncompressedPDFReader = PdfFileReader( uncompressedPDFFile )
	compressedPDFWriter   = PdfFileWriter()

	for pageNum in range(uncompressedPDFReader.numPages):
		compressedPDFWriter.addPage(uncompressedPDFReader.getPage(pageNum) )

	compressedPDFWriter.encrypt( password )
	compressedPDFWriter.write(compressedPDFFile)



'''
	pdfFile = open(filename_compressed, 'rb')	

	pdfReader = PdfFileReader(pdfFile)
	pdfWriter = PdfFileWriter()

	for pageNum in range(pdfReader.numPages):
		pdfWriter.addPage(pdfReader.getPage(pageNum) )


	pdfWriter.encrypt( senha )
	resultPdf = open(filename_encrypt, 'wb')
	pdfWriter.write(resultPdf)

'''




def merger(filename_watermark):

	merger = PdfFileMerger()

	merger.append(open("slides/01 - Apresentação.pdf", 'rb'),                       import_bookmarks = False) 
	merger.append(open("slides/02 - Introdução.pdf", 'rb'),                         import_bookmarks = False) 
	merger.append(open("slides/03 - Preparação do ambiente e downloads.pdf", 'rb'), import_bookmarks = False) 
	merger.append(open("slides/04 - Convenções, comandos Referência.pdf", 'rb'),    import_bookmarks = False) 
	merger.append(open("slides/05 - Hadoop Distributed  File System.pdf", 'rb'),    import_bookmarks = False) 
	merger.append(open("slides/06 - MapReduce.pdf", 'rb'),                          import_bookmarks = False) 
	merger.append(open("slides/07 - Hive.pdf", 'rb'),                               import_bookmarks = False) 
	merger.append(open("slides/08 - Sqoop.pdf", 'rb'),                              import_bookmarks = False) 
	merger.append(open("slides/09 - Flume.pdf", 'rb'),                              import_bookmarks = False) 
	merger.append(open("slides/10 - NoSQL.pdf", 'rb'),                              import_bookmarks = False) 
	merger.append(open("slides/11 - HBase.pdf", 'rb'),                              import_bookmarks = False) 
	merger.append(open("slides/12 - Kafka.pdf", 'rb'),                              import_bookmarks = False) 
	merger.append(open("slides/13 - Spark.pdf", 'rb'),                              import_bookmarks = False) 
	merger.append(open("slides/14 - Troubleshooting.pdf", 'rb'),                    import_bookmarks = False) 

	merger.write(filename_watermark)
	merger.close()



def addWatermark(aluno, wmpg, pdfOriginal, filename_watermark):

	print "Adicionando marca d'água ao documento do aluno %s." % aluno

	watermark = PdfFileReader(open("watermark.pdf", "rb"))
	watermarkPage = watermark.getPage(wmpg)

	output = PdfFileWriter()

	for page in range(pdfOriginal.getNumPages()):

		try:
		    pdfPage = pdfOriginal.getPage(page)
		    pdfPage.mergePage(watermarkPage)
		    output.addPage(pdfPage)

		except DecimalException:
			print "Erro no slide %d" % (page + 1)

	# Write output
	outputStream = file( filename_watermark, "wb")

	output.write(outputStream)
	outputStream.close()





def compress(aluno, filename_watermark, filename_compressed):

	print "Comprimindo o documento do aluno %s." % aluno

	os.system("ps2pdf  -dPDFSETTINGS=/printer  " + filename_watermark + " " + filename_compressed)




# Encrypt the PDF and add a password
def encrypt(aluno, senha, filename_compressed, filename_encrypt):

	print "Adicionando senha ao documento do aluno %s." % aluno

	pdfFile = open(filename_compressed, 'rb')	

	pdfReader = PdfFileReader(pdfFile)
	pdfWriter = PdfFileWriter()

	for pageNum in range(pdfReader.numPages):
		pdfWriter.addPage(pdfReader.getPage(pageNum) )


	pdfWriter.encrypt( senha )
	resultPdf = open(filename_encrypt, 'wb')
	pdfWriter.write(resultPdf)




def main():

	# Merge PDFs
	filename_merged = ("fundamentos-big-data-merged.pdf").lower().replace(' ', '-')
	merger(filename_merged)

	with open('info_participantes.csv') as csv_file:

		csv_reader = csv.reader(csv_file, delimiter=';')

		for row in csv_reader:

			wmpg  = int(row[0])
			aluno = row[1]
			senha = row[2]
			email = row[3]

			filename_watermark  = (r"output/fundamentos-big-data-watermark-"  + aluno + ".pdf").lower().replace(' ', '-')
			filename_compressed = (r"output/fundamentos-big-data-compressed-" + aluno + ".pdf").lower().replace(' ', '-')
			filename_encrypt    = (r"output/fundamentos-big-data-encrypt-"    + aluno + ".pdf").lower().replace(' ', '-')
			filename_email      = (r"output/" + email + ".pdf").lower().replace(' ', '-')


			pdfOriginal = PdfFileReader( open(filename_merged, "rb") )


			addWatermark(aluno, wmpg, pdfOriginal, filename_watermark)

			#compress(aluno, filename_watermark, filename_compressed)

			encrypt(aluno, senha, filename_watermark, filename_encrypt)

			os.rename(filename_encrypt, filename_email)

			print "Concluído processo para o material do aluno %s." % aluno

  

if __name__== "__main__":
  main()