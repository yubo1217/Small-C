/* 測試 02：變數型別、字元、十六進位與內建數學函式 */
int main() {
    int x = 0xFF;
    char c = 'A';
    int neg = -42;
    int zero = 0;
    printf("hex 0xFF = %d\n", x);
    printf("char 'A' = %c\n", c);
    printf("neg = %d\n", neg);
    printf("zero = %d\n", zero);
    printf("abs(-7) = %d\n", abs(-7));
    printf("max(3,7) = %d\n", max(3, 7));
    printf("min(3,7) = %d\n", min(3, 7));
    printf("pow(2,10) = %d\n", pow(2, 10));
    printf("sqrt(144) = %d\n", sqrt(144));
    printf("sizeof_int() = %d\n", sizeof_int());
    printf("sizeof_char() = %d\n", sizeof_char());
    return 0;
}
