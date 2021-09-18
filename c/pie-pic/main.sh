#!/usr/bin/env bash
echo 2 | sudo tee /proc/sys/kernel/randomize_va_space
for pie in no-pie pie; do
  exe="${pie}.out"
  gcc -O0 -std=c99 "-${pie}" "-f${pie}" -ggdb3 -o "$exe" main.c
  gdb -batch -nh \
    -ex 'set disable-randomization off' \
    -ex 'break main' \
    -ex 'run' \
    -ex 'printf "pc = 0x%llx\n", (long  long unsigned)$pc' \
    -ex 'run' \
    -ex 'printf "pc = 0x%llx\n", (long  long unsigned)$pc' \
    "./$exe" \
  ;
  echo
  echo
done
