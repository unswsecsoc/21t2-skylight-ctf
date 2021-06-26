// gcc -m32 -fno-stack-protector -no-pie office.c -o office
#include <stdio.h>
#include <stdlib.h>

void win () {
    char flag[50];
    printf("HEY! You aren't supposed to be here!\n");
    FILE *fp = fopen("flag.txt", "rb");
	char c;
	while ((c = fgetc(fp)) != EOF) {
		printf("%c", c);
	}
	fflush(stdout);
    fclose(fp);
}

void vuln () {
    char input[50];

    printf("Welcome to the Skylight Cyber CTF!\n");
    printf("Here is the address of our Sydney office: %p\n", &win);

    printf("Would you like to visit us? (y/n): ");
	fflush(stdout);
    gets(&input);
}

void main () {
    vuln();
}
