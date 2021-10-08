gencert:
	openssl req -new -x509 -days 365 -nodes -out cert.out -keyout cert.pri.key

genrsa:
	## 生成rsa密钥
	openssl genrsa -out rsa.pem 1024

rsa:
	## 从rsa密钥里面提取公钥
	openssl rsa -in rsa.pem -pubout > rsa.pub


## 公钥加密, 私钥解密
encdec:
	echo hello world > plain.txt
	openssl rsautl -pubin -inkey rsa.pub -in plain.txt -out plain.enc.bin -encrypt
	openssl rsautl -inkey rsa.pem -in plain.enc.bin -decrypt

## 私钥签名, 公钥验证
signverify:
	echo hello world > signed.txt
	openssl rsautl -inkey rsa.pem -in signed.txt -out signed.sign.bin -sign
	openssl rsautl -inkey rsa.pub -pubin -in signed.sign.bin -verify
