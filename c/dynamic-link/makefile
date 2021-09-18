SRC := $(shell find src -type f -name "*.c")
OBJ := $(patsubst src/%.c, obj/%.o, $(SRC))
LIB := liblib.so

all: targets lib/$(LIB) main main_pie main_pic 

targets: $(OBJ)

lib/$(LIB): targets
	@gcc -shared $(OBJ) -o $@

obj/%.o: src/%.c
	@gcc $< -c -fPIC -o $@

main: main.c
	@gcc main.c -L lib -l lib -Wl,-rpath=lib -o $@

main_pie: main.c
	@gcc -fPIC main.c -L lib -l lib -Wl,-rpath=lib -pie -o $@

main_pic: main.c
	@gcc -fPIC main.c -L lib -l lib -Wl,-rpath=lib -o $@

clean:
	rm -rf $(OBJ) lib/$(LIB) main main_pie main_pic

exam:
	@echo ------------main--------------
	@echo execute main[no pic no pie] twice, the address of hello, world, main should be same
	@echo 1st
	@./main
	@echo 2sn
	@./main
	@echo ------------main_pic--------------
	@echo execute main_pic[pic no pie] twice, the address of main should be same, while hello, world should be randomize
	@echo 1st
	@./main_pic
	@echo 2sn
	@./main_pic
	@echo ------------main_pie--------------
	@echo execute main_pie[pic, pie] twice, the address of hello, world, main_pie should be randomize
	@echo 1st
	@./main_pie
	@echo 2sn
	@./main_pie
