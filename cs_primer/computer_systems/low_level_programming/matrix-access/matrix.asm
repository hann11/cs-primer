section .text
global index
index:
	; rdi has the memory address, we need to get value of
	; rdi + (rindex * cols + cindex)*4
	imul rcx, rdx ; rindex * cols
	add rcx, r8 ; rindex * cols + cindex
	shl rcx, 2 ; (rindex * cols + cindex) * 4
	add rdi, rcx ; rdi + (rindex * cols + cindex)*4
	mov rax, [rdi] ; move from memory to register rax
	; rdi: matrix
	; esi: rows
	; edx: cols
	; ecx: rindex, 32bit rcx
	; r8d: cindex
	ret
