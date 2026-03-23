#include <stdio.h>

void reverse(char *str, int len) {
    int i = 0;          // начало строки
    int j = len - 1;    // конец строки

    while (i < j) {
        // меняем символы местами
        char t = str[i];
        str[i] = str[j];
        str[j] = t;

        i++;
        j--;
    }
}

void to_base(int n, int base, char *result) {

    // таблица символов для цифр
    const char digits[] = "0123456789ABCDEF";

    int i = 0;

    // приводим число к unsigned
    unsigned int un = (unsigned int)n;

    // специальный случай: если число 0
    if (un == 0) {
        result[i++] = '0';
    }

    while (un > 0) {

        // остаток определяет цифру
        int digit = un % base;

        // берём символ из таблицы digits
        result[i++] = digits[digit];

        // уменьшаем число
        un /= base;
    }

    // завершаем строку
    result[i] = '\0';
    reverse(result, i);
}

unsigned int rotate_right(unsigned int n, int k) {

    // количество бит в unsigned int
    int bits = sizeof(unsigned int) * 8;

    // нормализация сдвига
    // если k больше размера числа
    k %= bits;

    // если сдвиг 0 — возвращаем число
    if (k == 0)
        return n;

    return (n >> k) | (n << (bits - k));
}

int main() {

    char result[32];   // буфер для строки

    // пример перевода числа
    to_base(255, 16, result);
    printf("255 -> base16 = %s\n", result);

    // число в бинарном виде
    unsigned int n = 0b10110000;

    // пример циклического сдвига
    printf("rotate = %u\n", rotate_right(n, 2));

    return 0;
}