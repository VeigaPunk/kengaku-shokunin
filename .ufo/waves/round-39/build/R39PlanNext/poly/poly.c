#if 0
import sys
a, b = 0, 1
for _ in range(int(sys.argv[1])):
    a, b = b, a + b
print(a)
sys.exit()
'''
#endif
#include <stdio.h>
#include <stdlib.h>
int main(int c, char **v) { long a = 0, b = 1, t; for (long i = 0; i < atol(v[1]); i++) { t = a + b; a = b; b = t; } printf("%ld\n", a); return 0; }
#if 0
'''
#endif
