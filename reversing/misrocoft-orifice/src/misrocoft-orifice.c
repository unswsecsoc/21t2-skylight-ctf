#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BUFSIZE 30

// 3CQDB-LE4K5-3CR0T-?????-?????

int cseg2(char *ptr) {
    char *flag = "\x16\x10\x73\xb3\x25";
    char *key = "%S!\x83qkR-4A!";
    for (int i = 0; i < 5; i++) {
        if (ptr[i] != (flag[i] ^ key[i])) {
            return 0;
        }
    }
    return 1;
}

int val1(char *ptr) {
    int sum = 0;
    for (int i = 0; i < 5; i++) {
        sum += ptr[i];
    }
    return sum;
}

int val2(char *ptr) {
    int sum = 0;
    for (int i = 0; i < 5; i++) {
        sum += ptr[4 - i] * i;
    }
    return sum;
}

int cseg3_4(char *ptr, int gval1, int gval2) {
    return val1(ptr) == gval1 && val2(ptr) == gval2;
}

int cseg0(char *ptr) {
    char *target = "BDQC3";
    for (int i = 0; i < 5; i++) {
        if (*(ptr + 4 - i) != target[i])
            return 0;
    }
    return 1;
}

void open_document(void) {
    if (!access("top-sekrit.xdoc", R_OK)) {
        FILE *sekrit = fopen("top-sekrit.xdoc", "r");
        char c;
        while ((c = fgetc(sekrit)) != EOF) {
            putchar(c);
        }
        fflush(stdout);
    } else {
        printf("Nice work! Now, try this on the remote.");
    }
}

int main(void) {
    char license_key[BUFSIZE + 2];


    printf("weclome 2 miscroft ofice copyrite 1989. pls entr ur lisens key.\n");
    printf("format: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX. all UPPERCASE or NUM3R1C separated by dashes.\n");
    printf("key: ");
    fflush(stdout);
    fgets(license_key, BUFSIZE + 2, stdin);
    if (strlen(license_key) != BUFSIZE) {
        printf("bad key 4mat.\n");
        return 1;
    }

    if (!strncmp(&license_key[6], "LE4K5", 5) && cseg0(license_key) && 
        cseg2(&license_key[12]) && cseg3_4(&license_key[18], 308, 724) && 
        cseg3_4(&license_key[24], 315, 690)) {
        open_document();
        return 0;
    }

    printf("wrong key! no ofis for you!\n");
    return 1;
}

