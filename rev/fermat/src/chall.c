#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ptrace.h>

bool check(uint32_t a, uint32_t b, uint32_t c) {
  if (a < 3 || b < 3 || c < 3)
    return false;
  if (a * a * a + b * b * b != c * c * c)
    return false;

  return true;
}
void print_flag() {
  uint32_t flag[19] = {4152491142, 3316631995, 3584417439, 4020367268,
                       4021608364, 3298809519, 4020624809, 4020559521,
                       3752253093, 3298804914, 3753111471, 4020618924,
                       3585529266, 3735667634, 2163404711, 2280968952,
                       2264323234, 3567485603, 2965425656};
  char buffer[19 * 4] = {};
  for (int i = 0; i < 19; ++i) {
    buffer[4 * i + 0] = ((flag[i] ^ 0x000000c0U) >> 0x00) & 0xff;
    buffer[4 * i + 1] = ((flag[i] ^ 0x0000b000U) >> 0x08) & 0xff;
    buffer[4 * i + 2] = ((flag[i] ^ 0x00c00000U) >> 0x10) & 0xff;
    buffer[4 * i + 3] = ((flag[i] ^ 0xb0000000U) >> 0x18) & 0xff;
  }
  printf("%s\n", buffer);
}

int main() {

  uint32_t a, b, c;
  printf("Input a> ");
  scanf("%u", &a);
  printf("Input b> ");
  scanf("%u", &b);
  printf("Input c> ");
  scanf("%u", &c);

  printf("(a, b, c) = (%u, %u, %u)\n", a, b, c);

  if (check(a, b, c)) {
    puts("wow :o");
    print_flag();
  } else {
    puts("Invalid value :(");
  }

  return 0;
}
