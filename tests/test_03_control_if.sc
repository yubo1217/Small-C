/* 測試 03：if / else if / else 與邏輯運算子 */
int sign(int n) {
    if (n < 0) {
        return -1;
    } else if (n == 0) {
        return 0;
    } else {
        return 1;
    }
}

int in_range(int n, int lo, int hi) {
    if (n >= lo && n <= hi) {
        return 1;
    } else {
        return 0;
    }
}

int main() {
    int i;
    int r;
    int vals[6];
    vals[0] = -10;
    vals[1] = -1;
    vals[2] = 0;
    vals[3] = 1;
    vals[4] = 5;
    vals[5] = 100;

    printf("Sign tests:\n");
    for (i = 0; i < 6; i = i + 1) {
        r = sign(vals[i]);
        if (r < 0) {
            printf("  %d -> negative\n", vals[i]);
        } else if (r == 0) {
            printf("  %d -> zero\n", vals[i]);
        } else {
            printf("  %d -> positive\n", vals[i]);
        }
    }

    printf("Range [1,10] tests:\n");
    for (i = 0; i < 6; i = i + 1) {
        if (in_range(vals[i], 1, 10)) {
            printf("  %d is in range\n", vals[i]);
        } else {
            printf("  %d is out of range\n", vals[i]);
        }
    }

    return 0;
}
