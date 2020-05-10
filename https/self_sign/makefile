self_sign: prepare genrsa self_sign_req
	openssl ca -selfsign -in rootCA.csr

self_sign_req:
	openssl req -new -key demoCA/private/cakey.pem -out rootCA.csr

genrsa:
	openssl genrsa -out demoCA/private/cakey.pem

prepare:
	mkdir -p demoCA/newcerts
	mkdir -p demoCA/private
	touch demoCA/index.txt
	echo 01 > demoCA/serial
