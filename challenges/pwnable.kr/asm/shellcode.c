#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>


/* Syscall numbers:
    __NR_read 0
    __NR_write 1
    __NR_open 2
    __NR_exit 60
    __NR_exit_group 231
*/


int _asm_open(char *filename, unsigned int flags);
ssize_t _asm_read(int fd, void *buf, size_t count);
ssize_t _asm_write(int fd, const void *buf, size_t count);
void _asm_exit(int status);
void _asm_exit_group(int status);


int _start()
{
	char file_name[] = "this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong";
	// char file_name[] = "asm.c";

	#define N 200

	
	char buf[N] = {};

	int fd;
	fd = _asm_open(file_name, O_RDONLY);
	_asm_read(fd, buf, N);
	_asm_write(STDOUT_FILENO, buf, N);
	_asm_exit(0);
}


int _asm_open(char *filename, unsigned int flags)
{
	int res;

	__asm__("movq %1, %%rdi\t\n"  // 1st arg
		"movq %2, %%rsi\t\n"  // 2nd arg
		"movq %3, %%rax\t\n"  // syscall num
		"syscall\t\n"
		: "=r" (res)
		: "r" (filename), "r" ((unsigned long)flags), "i" (0x2)
		: "%rdi","%rsi");

	return res;
}


ssize_t _asm_read(int fd, void *buf, size_t count)
{
	ssize_t res;

	__asm__("movq %1, %%rdi\t\n"  // 1st arg
		"movq %2, %%rsi\t\n"  // 2nd arg
		"movq %3, %%rdx\t\n"  // 3rd arg
		"movq %4, %%rax\t\n"  // syscall num
		"syscall\t\n"
		: "=ra" (res)
		: "r" ((long) fd), "r" (buf), "r" ((long) count), "i" (0x0)
		: "%rdi","%rsi","%rdx");

	return res;
}


ssize_t _asm_write(int fd, const void *buf, size_t count)
{
	ssize_t res;

	__asm__("movq %1, %%rdi\t\n"  // 1st arg
		"movq %2, %%rsi\t\n"  // 2nd arg
		"movq %3, %%rdx\t\n"  // 3rd arg
		"movq %4, %%rax\t\n"  // syscall num
		"syscall\t\n"
		: "=ra" (res)
		: "r" ((long) fd), "r" (buf), "r" ((long) count), "i" (0x1)
		: "%rdi","%rsi","%rdx");

	return res;
}


void _asm_exit(int status)
{
	ssize_t res;

	__asm__("movq %1, %%rdi\t\n"  // 1st arg
		"movq %2, %%rax\t\n"  // syscall num
		"syscall\t\n"
		: "=ra" (res)
		: "r" ((long) status), "i" (60)
		: "%rdi");
}


void _asm_exit_group(int status)
{
	ssize_t res;

	__asm__("movq %1, %%rdi\t\n"  // 1st arg
		"movq %2, %%rax\t\n"  // syscall num
		"syscall\t\n"
		: "=ra" (res)
		: "r" ((long) status), "i" (231)
		: "%rdi");
}
