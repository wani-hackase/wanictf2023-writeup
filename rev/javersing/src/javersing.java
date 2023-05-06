import java.util.Scanner;
import java.lang.StringBuilder;


public class javersing{
    public static void main(String[] args){
        String data = "Fcn_yDlvaGpj_Logi}eias{iaeAm_s";
        boolean flag = true;
        Scanner scanner = new Scanner(System.in);
        System.out.println("Input password: ");
        String password = scanner.nextLine();

        password = String.format("%30s",password).replace(" ","0");

        for(int i=0;i<30;i++){
            if(password.charAt((i*7)%30) != data.charAt(i)){
                flag = false;
            }
        }
        if (flag){
            System.out.println("Correct!");
        }
        else{
            System.out.println("Incorrect...");
        }

    }
}