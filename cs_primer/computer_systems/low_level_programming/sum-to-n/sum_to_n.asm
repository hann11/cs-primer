section .text
global sum_to_n
sum_to_n:
	xor rax, rax ; zero out rax

_loop:
	add rax, rdi ; add rdi to rax
	dec rdi ; decrement rdi by 1 (or sub rdi, 1)
	cmp rdi, 0 ; sets flags based on rdi - 0
	jge _loop ; checks if rdi is greater than or equal to 0 in the flags
	ret ; return rax