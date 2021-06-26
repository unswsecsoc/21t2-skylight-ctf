// gcc -m32 -z execstack -fno-stack-protector new_office.c -o new_office
#include <stdio.h>
#include <stdlib.h>

void vuln () {
    char input[50];

    printf("Welcome to the Skylight Cyber CTF again!\n");
    printf("We've put in new security measures since you hacked us before.\n");
    printf("We have a secret office which is at: %p\n", &input);
	fflush(stdout);
    fgets(input, 5000, stdin);
}

void main () {
    vuln();
}
