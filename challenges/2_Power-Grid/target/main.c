#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void c_help()
{
	puts("ScadaOS 18.21_2p1 (x86_64-pc-linux-gnu)");
	puts("?          Display this menu");
	puts("dir        List files on a filesystem");
	puts("erase      Erase the filesystem");
	puts("exit       Exit the shell");
	puts("help       Display this menu");
	puts("more       Display the contents of a file");
	puts("quit       Exit the shell");
	puts("shutdown   Shut down the system");
	puts("status     View the system status");
	puts("write      Write to a file");
}

void c_dir()
{
	puts("Directory listing for flash:");
	puts("rw-rw-r--   admin  admin     note.txt");
}

void c_erase()
{
	puts("Error: filesystem protected from erasure at the kernel. Please contact ScadaOS support.");
}

void c_more_err()
{
	puts("Usage: more <file>");
}

void c_more(char *filename)
{
	char buffer;
	FILE *fp;

	if (strcmp(filename, "note.txt") != 0)
	{
		c_more_err();
		return;
	}

	if ((fp = fopen("./note.txt", "r")) == NULL)
	{
		puts("Error: file not found.");
		return;
	}

	buffer = fgetc(fp);
	while (buffer != EOF)
	{
		printf("%c", buffer);
		buffer = fgetc(fp);
	}

	fclose(fp);
}

void c_shutdown()
{
	char buffer[8];
	FILE *fp;

	printf("Are you sure? This may disrupt service. [y/n] ");
	fgets(buffer, 8, stdin);
	buffer[strlen(buffer)-1]='\0';

	if (strcmp(buffer, "y") == 0)
	{
		printf("Beginning shutdown procedure...");

		fp = fopen("./shutdown.state", "w");
		fprintf(fp, "1");
		fclose(fp);

		sleep(5);
		puts("\n\nConnection terminated.");
		exit(0);
	}
}

void c_status()
{
	puts("Server Status");
	puts("  56%% cur resource load");
	puts("  52%% avg resource load");
	puts("  97%% avg uptime");
	puts("");
	puts("Service Status");
	puts("  13%% cur load");
}

int scadaos_shell()
{
	char command[1024];
	char *token;

	printf("scadaos-uced# ");
	fgets(command, 1024, stdin);
	command[strlen(command)-1]='\0';

	token = strtok(command, " ");

	if ((strcmp(token, "exit") == 0) || (strcmp(token, "quit") == 0))
		return 1;
	else if ((strcmp(token, "help") == 0) || (strcmp(token, "?") == 0))
		c_help();
	else if (strcmp(token, "dir") == 0)
		c_dir();
	else if (strcmp(token, "erase") == 0)
		c_erase();
	else if (strcmp(token, "more") == 0)
	{
		token = strtok(NULL, " ");
		if (token == NULL)
			c_more_err();
		else
			c_more(token);
	}
	else if (strcmp(token, "shutdown") == 0)
		c_shutdown();
	else if (strcmp(token, "status") == 0)
		c_status();
//	else if (strcmp(token, "write") == 0)
//	{
//
//	}

	return 0;
}

int main()
{
	char uUsername[256];
	char uPassword[256];
	char cPassword[256];
	FILE *fp;

	setvbuf(stdout, NULL, _IONBF, 0);

	if ((fp = fopen(SECRET_LOCATION, "r")) == NULL)
	{
		puts("!! No valid logins loaded.");
		exit(-1);
	}

	fgets(cPassword, 256, fp);
	fclose(fp);

	puts("ScadaOS 18.21_2p1 cterm tty1\n");

	while (1)
	{
		printf("scadaos-uced login: ");
		fgets(uUsername, 256, stdin);
		uUsername[strlen(uUsername)-1]='\0';
		printf("password: ");
		system("stty -echo");
		fgets(uPassword, 256, stdin);
		uPassword[strlen(uPassword)-1]='\0';
		system("stty echo");

		if ((strcmp(uUsername, "admin") == 0) && (strcmp(uPassword, cPassword) == 0))
			break;

		puts("\n\nCould not log in for the following user:");
		printf(uUsername);
		printf("\n\n");
		continue;
	}

	puts("\n\nLogin successful.");

	while (!scadaos_shell());

	puts("\nConnection terminated.");
	return 0;
}
