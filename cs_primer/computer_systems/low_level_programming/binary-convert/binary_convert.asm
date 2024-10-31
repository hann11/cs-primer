section .text
global binary_convert
binary_convert:
	xor ecx, ecx ; char
	xor eax, eax ; bitvec

_base_loop:
	movzx ecx, byte [rdi] ; rdi: source string
	inc rdi
	cmp cl, 0
	je _finish
	and ecx, 0x1 ; get the last bit, same as subtracting 0x30
	shl eax, 1
	or eax, ecx
	jmp _base_loop

_finish:
	ret
