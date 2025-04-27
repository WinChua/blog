all: c r

c:
	@gcc -pie -fPIE main.c -o addr_to_read
	@gcc read_addr.c -o read_addr 

r:
	@./addr_to_read &
	@./read_addr `pidof addr_to_read` my_section addr_to_read
	@echo
	@gdb -batch -q -p `pidof addr_to_read` -ex "x/xw `./read_addr $$(pidof addr_to_read) my_section addr_to_read`" 
	@kill -9 `pidof addr_to_read`

