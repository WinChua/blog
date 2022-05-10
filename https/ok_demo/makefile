SELF_SIGN=ca_cert
SELF_SIGN_KEY=$(SELF_SIGN)_key

SVR_CRT=signed_cert
SVR_CRT_KEY=$(SVR_CRT)_key
SVR_CSR=$(SVR_CRT)_csr

test: selfsign csr sign
	python main.py $(SVR_CRT).pem $(SVR_CRT_KEY).pem
	curl --cacert $(SELF_SIGN).pem https://localhost:5000/


selfsign:
	openssl req -nodes -x509 -days 365 -newkey rsa:4096 -keyout $(SELF_SIGN_KEY).pem -out $(SELF_SIGN).pem

csr:
	openssl req -new -nodes -newkey rsa:4096 -keyout $(SVR_CRT_KEY).pem -out $(SVR_CSR).pem

sign:
	openssl x509 -req -in $(SVR_CSR).pem -days 365 -CA $(SELF_SIGN).pem  -CAkey $(SELF_SIGN_KEY).pem  -CAcreateserial -out $(SVR_CRT).pem


clean:
	rm *pem
