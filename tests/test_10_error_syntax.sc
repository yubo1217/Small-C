/* 測試 10：語法錯誤偵測
   此程式刻意含有語法錯誤：
     行 10  — 變數宣告缺少分號
     行 14  — printf 呼叫缺少右括號
   預期 CHECK / RUN 輸出語法錯誤訊息。
*/
int main() {
    int x = 10
    int y = 20;
    printf("x = %d\n", x);
    printf("y = %d\n", y;
    return 0;
}
