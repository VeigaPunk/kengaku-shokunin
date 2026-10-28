#define pgopen b /*
import sys

def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

_k = int(sys.argv[1])
print(fib(_k))
"""
#define pgclose b */
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    unsigned long long a = 0, b = 1, t;
    unsigned int n = (unsigned int)strtoul(argv[1], NULL, 10);
    for (unsigned int i = 0; i < n; ++i) { t = a + b; a = b; b = t; }
    printf("%llu\n", a);
    return 0;
}
#define pgtail """
