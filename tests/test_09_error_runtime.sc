/* 測試 09：執行期錯誤偵測（除以零、陣列越界、sqrt 負數） */
/* 此程式刻意觸發執行期錯誤，預期輸出含 Runtime error 訊息。  */

int safe_div(int a, int b) {
    return a / b;
}

int main() {
    int arr[5];
    int i;

    /* 正常執行段 */
    printf("10 / 2 = %d\n", safe_div(10, 2));

    for (i = 0; i < 5; i = i + 1) {
        arr[i] = i * i;
    }
    printf("arr[3] = %d\n", arr[3]);

    /* 觸發：除以零 */
    printf("10 / 0 = %d\n", safe_div(10, 0));

    return 0;
}
