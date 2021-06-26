#include <stdio.h>
#include <string.h>
             
// gcc -m32 -g vuln.c -o vuln

int main(int argc, char *argv[]) {
    char fmt[100];
    char buf[100];
    int i = 5;
    printf("i = %d\n", i);
    printf("%s", "I want i to be bigger. Much bigger.\nHere's some useful info:\n");
    printf("i @ %p\n", &i);
    fflush(stdout);

    scanf("%100s", buf);

    //snprintf(fmt, sizeof fmt, "%s", buf);
    snprintf(fmt, sizeof fmt, buf);

    printf("buffer = %s\n", fmt);
    printf("i = %d\n", i);
    if (i == 999) {
        printf("%s\n", "SKYLIGHT{FLAG_WILL_BE_HERE}");
    }
    fflush(stdout);
    return 0;
}
