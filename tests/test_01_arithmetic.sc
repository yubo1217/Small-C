/* 測試 01：基本算術與複合指定運算子 */
int main() {
    int a = 10;
    int b = 3;
    printf("a = %d\n", a);
    printf("b = %d\n", b);
    printf("a + b = %d\n", a + b);
    printf("a - b = %d\n", a - b);
    printf("a * b = %d\n", a * b);
    printf("a / b = %d\n", a / b);
    printf("a %% b = %d\n", a % b);
    printf("a & b = %d\n", a & b);
    printf("a | b = %d\n", a | b);
    printf("a ^ b = %d\n", a ^ b);
    printf("a << 1 = %d\n", a << 1);
    printf("a >> 1 = %d\n", a >> 1);
    a += 5;
    printf("a += 5: %d\n", a);
    a -= 2;
    printf("a -= 2: %d\n", a);
    a *= 2;
    printf("a *= 2: %d\n", a);
    a /= 3;
    printf("a /= 3: %d\n", a);
    a %= 4;
    printf("a %%= 4: %d\n", a);
    return 0;
}
