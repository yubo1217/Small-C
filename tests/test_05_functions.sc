/* 測試 05：函式定義、呼叫、參數傳遞與回傳值 */
int add(int a, int b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}

int gcd(int a, int b) {
    int temp;
    while (b != 0) {
        temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int is_even(int n) {
    if (n % 2 == 0) {
        return 1;
    } else {
        return 0;
    }
}

void print_parity(int n) {
    if (is_even(n)) {
        printf("%d is even\n", n);
    } else {
        printf("%d is odd\n", n);
    }
}

int main() {
    int i;
    printf("add(12, 8) = %d\n", add(12, 8));
    printf("multiply(6, 7) = %d\n", multiply(6, 7));
    printf("gcd(48, 18) = %d\n", gcd(48, 18));
    printf("gcd(100, 75) = %d\n", gcd(100, 75));
    for (i = 1; i <= 6; i = i + 1) {
        print_parity(i);
    }
    return 0;
}
