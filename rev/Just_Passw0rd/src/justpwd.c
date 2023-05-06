#include <stdio.h>
#include <string.h>

int main(void) {
  char input[50];
  printf("Input password > ");
  scanf("%s", input);

  if (strlen(input) != 8) {
    puts("Incorrect");
    return 1;
  }

  char pass[8] = {'p', '3', 'U', '2', '8', 'A', 'x', 'W'};

  for (int i = 0; i < sizeof(pass); i++) {
    if (input[i] != pass[i]) {
      puts("Incorrect");
      return 1;
    }
  }
  printf("Correct!\nFLAG is FLAG{1234_P@ssw0rd_admin_toor_qwerty}\n");
  return 0;
}