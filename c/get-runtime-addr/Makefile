all: c r

c:
	@gcc -pie -fPIE main.c -o addr_to_read
	@gcc read_addr.c -o read_addr 

r:
	@./addr_to_read &
	@./read_addr `pidof addr_to_read` my_section
	@kill -9 `pidof addr_to_read`

