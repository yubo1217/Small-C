/* 測試 08：指標操作（取址、解參考、傳指標） */
void swap(int *a, int *b) {
    int temp;
    temp = *a;
    *a = *b;
    *b = temp;
}

int sum_via_ptr(int *arr, int n) {
    int i;
    int s = 0;
    for (i = 0; i < n; i = i + 1) {
        s += *(arr + i);
    }
    return s;
}

void bubble_sort(int *arr, int n) {
    int i;
    int j;
    for (i = 0; i < n - 1; i = i + 1) {
        for (j = 0; j < n - 1 - i; j = j + 1) {
            if (arr[j] > arr[j + 1]) {
                swap(&arr[j], &arr[j + 1]);
            }
        }
    }
}

int main() {
    int x = 10;
    int y = 20;
    int *p;
    int arr[5];
    int i;

    /* 基本指標操作 */
    printf("Before swap: x=%d, y=%d\n", x, y);
    swap(&x, &y);
    printf("After swap:  x=%d, y=%d\n", x, y);

    p = &x;
    printf("*p = %d\n", *p);
    *p = 99;
    printf("x after *p=99: %d\n", x);

    /* 透過指標求和 */
    for (i = 0; i < 5; i = i + 1) arr[i] = (i + 1) * 10;
    printf("sum via ptr = %d\n", sum_via_ptr(arr, 5));

    /* 傳指標排序 */
    arr[0] = 40; arr[1] = 10; arr[2] = 30; arr[3] = 50; arr[4] = 20;
    bubble_sort(arr, 5);
    printf("sorted: ");
    for (i = 0; i < 5; i = i + 1) printf("%d ", arr[i]);
    printf("\n");

    return 0;
}
