/* 測試 06：遞迴函式（階乘與費氏數列） */
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

int fibonacci(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int power(int base, int exp) {
    if (exp == 0) return 1;
    return base * power(base, exp - 1);
}

int main() {
    int i;
    printf("Factorials:\n");
    for (i = 0; i <= 7; i = i + 1) {
        printf("  %d! = %d\n", i, factorial(i));
    }
    printf("Fibonacci:\n");
    for (i = 0; i <= 10; i = i + 1) {
        printf("  F(%d) = %d\n", i, fibonacci(i));
    }
    printf("Powers of 2:\n");
    for (i = 0; i <= 8; i = i + 1) {
        printf("  2^%d = %d\n", i, power(2, i));
    }
    return 0;
}
