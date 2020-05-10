all: pri pub cert

pri:
	openssl genrsa -out key

pub:
	openssl rsa -pubout -in key -out key.pub

cert:
	openssl req -new -key key -out key.cert
