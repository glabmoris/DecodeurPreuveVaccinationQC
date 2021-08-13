####################################################
#  QR vaccination proof decoding PoC               #
#                                                  #
#  Guillaume Labbe-Morissette                      #
####################################################

import sys
import zxing
import base64
import zlib
import json
from pdf2image import convert_from_path

# Decode SMART Health Cards Framework encoded strings
def decodeSHC(shc):
	decodedString = ""

	for first,second in (shc[i:i+2] for i in range(0, len(shc), 2)):
		decodedString += chr(int(first + second) + 45)

	return decodedString

#decode JSON Web Token encoded data
def decodeJWT(jwtString):
	# Uses JWT compact serialization
	header = base64.urlsafe_b64decode(jwtString.split(".")[0] + '=' * (4 - len(jwtString.split(".")[0]) % 4)) 
	body   = base64.urlsafe_b64decode(jwtString.split(".")[1] + '=' * (4 - len(jwtString.split(".")[1]) % 4))

	#body uses DEFLATE RFC 1950 encoding
	decompress = zlib.decompressobj(-zlib.MAX_WBITS)
	decodedBody = decompress.decompress(body)
	decodedBody += decompress.flush()

	return decodedBody


def decodeImage(qrFile):
	qr = zxing.BarCodeReader()
	qrdata = qr.decode(qrFile)

	if qrdata.raw.startswith("shc:/"):
		shcString = qrdata.raw[5:]

		#sys.stderr.write("SHC String: {}\n\n".format(shcString))

		jwtString = decodeSHC(shcString)

		#sys.stderr.write("JWT String: {}\n\n".format(jwtString))

		print(json.dumps(json.loads(decodeJWT(jwtString)),indent=4))
	else:
		sys.stderr.write("Bad QR data\n\n")



if len(sys.argv) != 2:
	sys.stderr.write("Usage: extract.py path-to-pdf\n\n")
	sys.exit(1)

pdfPath = sys.argv[1]

sys.stderr.write("Extracting from {}...\n\n".format(pdfPath))

# Convert all pages from PDF to images. Because f*** you.
pages = convert_from_path(pdfPath, 500,fmt='png')

pages[0].save("qr.png",'PNG')
decodeImage("qr.png")
