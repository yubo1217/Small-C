/* 測試 07：陣列操作（建立、走訪、搜尋、反轉） */
#define N 7

void print_array(int *arr, int n) {
    int i;
    for (i = 0; i < n; i = i + 1) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int sum_array(int *arr, int n) {
    int i;
    int s = 0;
    for (i = 0; i < n; i = i + 1) {
        s += arr[i];
    }
    return s;
}

int linear_search(int *arr, int n, int target) {
    int i;
    for (i = 0; i < n; i = i + 1) {
        if (arr[i] == target) return i;
    }
    return -1;
}

void reverse_array(int *arr, int n) {
    int i;
    int j;
    int tmp;
    i = 0;
    j = n - 1;
    while (i < j) {
        tmp = arr[i];
        arr[i] = arr[j];
        arr[j] = tmp;
        i = i + 1;
        j = j - 1;
    }
}

int main() {
    int data[N];
    int idx;
    data[0] = 15; data[1] = 3; data[2] = 9;
    data[3] = 7;  data[4] = 1; data[5] = 12; data[6] = 5;

    printf("Array:   ");
    print_array(data, N);
    printf("Sum = %d\n", sum_array(data, N));

    idx = linear_search(data, N, 7);
    printf("Search 7: index %d\n", idx);

    idx = linear_search(data, N, 99);
    printf("Search 99: index %d\n", idx);

    reverse_array(data, N);
    printf("Reversed: ");
    print_array(data, N);

    return 0;
}
