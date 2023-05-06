#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

int compare(char dat, int index) {
  char ans[] = "FLAGmlEAfh.i`,f_N)r?W^c$kx";
  if (dat == ans[index]) {
    return 1;
  } else {
    return 0;
  }
}

int main() {
  char input[50];

  int page_s = getpagesize();
  void *comp_add = (void *)compare;
  void *page_add = (void *)((unsigned long)(comp_add) & ~(page_s - 1));

  mprotect(page_add, page_s, PROT_READ | PROT_WRITE | PROT_EXEC);

  printf("Input flag: ");
  scanf("%s", input);

  int temp = 0;
  for (int i = 0; i < 26; i++) {
    if (i >= 4) {
      temp = (i * 11) % 15;
    }
    if (i <= 7) {
      ((unsigned char *)comp_add)[37 + (i)] =
          ((unsigned char *)comp_add)[37 + (i)] + temp;
    } else if (i <= 15) {
      ((unsigned char *)comp_add)[47 + (i - 8)] =
          ((unsigned char *)comp_add)[47 + (i - 8)] + temp;
    } else if (i <= 23) {
      ((unsigned char *)comp_add)[65 + (i - 16)] =
          ((unsigned char *)comp_add)[65 + (i - 16)] + temp;
    } else {
      ((unsigned char *)comp_add)[81 + (i - 24)] =
          ((unsigned char *)comp_add)[81 + (i - 24)] + temp;
    }
  }

  for (int i = 0; i < 26; i++) {
    if (compare(input[i], i) == 0) {
      printf("Incorrect.\n");
      return 1;
    }
  }
  printf("Correct!\n");
  return 0;
}