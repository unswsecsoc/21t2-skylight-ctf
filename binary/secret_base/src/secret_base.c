// gcc -m32 secret_base.c -o secret_base -lm

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <time.h>
#include <ctype.h>
#include <string.h>
#include <stdarg.h>

void toolz () {
    __asm__ (
        "mov %eax, %ebp\n\t"
        "ret\n\t"
    );
}

void tools () {
    __asm__ (
        "mov %ebp, %ecx\n\t"
        "mov %ebp, %edx\n\t"
        "ret\n\t"
    );
}

void exec () {
    __asm__ (
        "int $0x80\n\t"
        "ret\n\t"
    );
}

void ctf () {
    __asm__ (
        "inc %eax\n\t"
        "ret\n\t"
    );
}

void asdf () {
    __asm__ (
        "mov $0xFFFFFFD3, %eax\n\t"
        "ret\n\t"
    );
}

void jame () {
    fflush(stdout);
    ferror((FILE *)12312);
    fclose((FILE *)123123);
    fprintf(stdout, "%s", "asdfsdf");
    fopen("asfd", "r");
    fputc(41, stdout);
    fgetc(stdout);
    getchar();
    putchar(41);
    acos(5);
    asin(5);
    atan(5);
    cos(5);
    sin(5);
    tan(5);
    cosh(5);
    sinh(5);
    tanh(5);
    exp(5);
    fmod(5, 5);
    atof("asdf");
    system("ls");
    clock();
    isalnum(41);
    isalpha(41);
    iscntrl(41);
    isdigit(41);
    isgraph(41);
    islower(41);
    isprint(41);
    ispunct(41);
    isspace(41);
    isupper(41);
    ctime((const time_t *)5);
    difftime((time_t) 5, (time_t) 5);
    memchr((const void *) "asdf", 5, 5);
    memcmp("asfd", "zxcv", 5);
    memset((void *)5, 0, (size_t) 5);
    memmove((void *) NULL, (const void *) NULL, 5);
    strncat((char *) NULL, (const char *) NULL, 5);
    __asm__ (
        "mov %eax, %ebx\n\t"
        "ret\n\t"
    );
}

void *vuln () {
    char input[24];

    printf("Ok! So you've broken into our offices twice.\n");
    printf("I bet you won't be able to get into our secret base.\n");
    printf("We have a secret office which isn't at: %p\n", &vuln);
    printf("The password is: ");
    fwrite(input + 24, 1, 4, stdout);
    printf("\n");
	fflush(stdout);
    fgets(input, 5000, stdin);
}

void main () {
    vuln();
}
