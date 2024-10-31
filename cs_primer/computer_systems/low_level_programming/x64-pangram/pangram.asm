section .text
global pangram
pangram:
	xor rax, rax
	xor ecx, ecx ; bitvec
	xor edx, edx ; char
	xor r8, r8 ; 
	xor ebx, ebx ; 

_base_loop:
	movzx edx, byte [rdi] ; rdi: source string
	inc rdi
	cmp dl, 0
	je _finish
	
	cmp edx, 0x41
	jl _base_loop
	cmp edx, 0x5a
	jg _lowercheck
	add edx, 0x20
	jmp _lowercheck

_lowercheck:
	cmp edx, 0x61
	jl _base_loop
	cmp edx, 0x7a
	jg _base_loop
	mov ebx, 1
	sub edx, 0x61
	mov ecx, edx
	shl ebx, cl
	or r8, rbx
	jmp _base_loop


_finish:
	cmp r8, 0x3ffffff
	jne _not_pangram
	mov rax, 1
	ret

_not_pangram:
	xor rax, rax
	ret