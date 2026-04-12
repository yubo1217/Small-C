/* 測試 04：while / for / do-while / break / continue */
int main() {
    int i;
    int sum;

    /* while */
    i = 1;
    sum = 0;
    while (i <= 5) {
        sum += i;
        i = i + 1;
    }
    printf("while  1..5 sum = %d\n", sum);

    /* for */
    sum = 0;
    for (i = 1; i <= 5; i = i + 1) {
        sum += i;
    }
    printf("for    1..5 sum = %d\n", sum);

    /* do-while */
    i = 1;
    sum = 0;
    do {
        sum += i;
        i = i + 1;
    } while (i <= 5);
    printf("do-while 1..5 sum = %d\n", sum);

    /* break：超過 5 就停 */
    sum = 0;
    for (i = 1; i <= 10; i = i + 1) {
        if (i > 5) break;
        sum += i;
    }
    printf("break at 5: sum = %d\n", sum);

    /* continue：跳過偶數 */
    sum = 0;
    for (i = 1; i <= 10; i = i + 1) {
        if (i % 2 == 0) continue;
        sum += i;
    }
    printf("odd sum 1..10 = %d\n", sum);

    return 0;
}
