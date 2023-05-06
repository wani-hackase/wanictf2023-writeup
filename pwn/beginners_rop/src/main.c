#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUF_SIZE 32
#define MAX_READ_LEN 96

void init() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  alarm(180);
}

void show_stack(char *buf) {
  printf("\n  #############################################\n");
  printf("  #                stack state                #\n");
  printf("  #############################################\n\n");

  printf("                 hex           string\n");
  for (int i = 0; i < MAX_READ_LEN; i += 8) {
    printf("       +--------------------+----------+\n");
    printf(" +0x%02x | 0x%016lx | ", i, *(unsigned long *)(buf + i));
    for (int j = 7; j > -1; j--) {
      char c = *(char *)(buf + i + j);
      if (c > 0x7e || c < 0x20)
        c = '.';
      printf("%c", c);
    }
    if (i == 40)
      printf(" | <- TARGET!!!\n");
    else
      printf(" |\n");
  }
  printf("       +--------------------+----------+\n");
}

void pop_rax_ret() { asm("pop %rax; ret"); }

void xor_rsi_ret() { asm("xor %rsi, %rsi; ret"); }

void xor_rdx_ret() { asm("xor %rdx, %rdx; ret"); }

void mov_rsp_rdi_pop_ret() {
  asm("mov %rsp, %rdi\n"
      "add $0x8, %rsp\n"
      "ret");
}

void syscall_ret() { asm("syscall; ret"); }

int ofs = 0, ret = 0;

int main() {
  init();

  char buf[BUF_SIZE] = {0};

  printf("Let's practice ROP attack!\n");

  while (ofs < MAX_READ_LEN) {
    show_stack(buf);

    printf("your input (max. %d bytes) > ", MAX_READ_LEN - ofs);
    ret = read(0, buf + ofs, MAX_READ_LEN - ofs);
    if (ret < 0)
      return 1;
    ofs += ret;
  }
  return 0;
}
