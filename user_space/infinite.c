#include <stdio.h>

int main() {
    volatile int i = 0; // volatile kullanarak derleyicinin (compiler) bu sonsuz döngüyü silmesini (optimize etmesini) engelliyoruz.
    while(1) {
        i = (i + 1) % 1000;
    }
    return 0;
}
