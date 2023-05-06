#include <iostream> // for cout
using namespace std;
#include <emscripten.h>
#include <stdlib.h>
#include <string>

EM_JS(char *, prompt_name, (), {
  var result = prompt('Please input your name', '');
  var stringPtr = allocate(intArrayFromString(result || ''), ALLOC_STACK);
  return stringPtr;
});
EM_JS(char *, prompt_pass, (), {
  var result = prompt('Please input your password', '');
  var stringPtr = allocate(intArrayFromString(result || ''), ALLOC_STACK);
  return stringPtr;
});
int main() {
  string correctUserName = "ckwajea";
  string correctPassword = "feag5gwea1411_efae!!";
  string F = "Fla";
  string L = "g{Y0u_C";
  string A1 = "4n_3x";
  string A2 = "3cut3_Cp";
  string G1 = "p_0n_Br";
  string G2 = "0us";
  string G3 = "3r!}";
  string userName = prompt_name();
  string password = prompt_pass();
  cout << "Your UserName : " << userName << endl;
  cout << "Your PassWord : " << password << endl;
  // if (strcmp(password, correctPassword) == 0 && strcmp(userName,
  // correctUserNane) == 0) {
  if (userName == correctUserName && password == correctPassword) {
    cout << "Correct!! Flag is here!!" << endl;
    cout << F << L << A1 << A2 << G1 << G2 << G3 << endl;
    return 0;
  }
  cout << "Incorrect!" << endl;
}