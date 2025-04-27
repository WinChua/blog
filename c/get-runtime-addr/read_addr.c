#include <string.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <elf.h>

int main(int argc, char * argv[]) {
  if (argc <= 2) {
    printf("Usage: %s pid section_name\n", argv[0]);
    return 0;
  }
  char filename[50];
  sprintf(filename, "/proc/%s/maps", argv[1]);
  FILE *maps = fopen(filename, "r");
  if (maps == NULL) {
    printf("can't read %s\n", filename);
    return 1;
  }
  char line[1000];
  while(fgets(line, 1000, maps) != NULL) {
    line[strlen(line)-1] = '\0';
    unsigned long start = 0;
    unsigned long path_pos = 0;
    sscanf(line, "%lx-%*x %*s %*s %*s %*s %ln", &start, &path_pos);
    if (!path_pos) {
      continue;
    }
    const char *path = line + path_pos;
    const char *filename = strrchr(path, '/');
    if (filename) {
        filename++;  // Move past the '/'
    } else {
        filename = path;  // No directories, or an empty string
    }
    int fd = open(filename, O_RDONLY);
    struct stat file_stats;
    if (fstat(fd, &file_stats) != 0) {
      continue;
    }
    void *file_memory = NULL;
    file_memory = mmap(NULL, file_stats.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    Elf64_Ehdr* elf_header = (Elf64_Ehdr*)file_memory;
    Elf64_Shdr* section_header_table = (Elf64_Shdr*)(file_memory + elf_header->e_shoff);

    Elf64_Shdr* shstrtab_section = &section_header_table[elf_header->e_shstrndx];
    char* shstrtab = (char*)(file_memory + shstrtab_section->sh_offset);

    Elf64_Shdr* section = NULL;
    for (int i = 0; i < elf_header->e_shnum; i++) {
        char* this_sec_name = shstrtab + section_header_table[i].sh_name;
        // Move 1 character to account for the leading "."
        this_sec_name += 1;
        if (strcmp(this_sec_name, argv[2]) == 0) {
          printf("find\n");
          section = &section_header_table[i];
          break;
        }
    }

    Elf64_Phdr* program_header_table = (Elf64_Phdr*)(file_memory + elf_header->e_phoff);
    // Find the first PT_LOAD segment
    Elf64_Phdr* first_load_segment = NULL;
    for (int i = 0; i < elf_header->e_phnum; i++) {
        if (program_header_table[i].p_type == PT_LOAD) {
            first_load_segment = &program_header_table[i];
            break;
        }
    }

    uintptr_t start_address = start;
    uintptr_t result = 0;
    if (section != NULL && first_load_segment != NULL) {
      uintptr_t elf_load_addr = first_load_segment->p_vaddr
          - (first_load_segment->p_vaddr % first_load_segment->p_align);
      result = start_address + (uintptr_t)section->sh_addr - elf_load_addr;
    }
    if (result != 0) {
      printf("result is %p\n", (void*)result);
      return 0;
    }
  }
}
