section .text
global fib

fib:
	; base case if n<=1, return n (stored in rdi)
	cmp rdi, 1
	jle .base_case

	; push n to stack
	push rdi

	; call fib with n-1
	dec rdi
	call fib

	; pop n from stack
	pop rdi

	; push result of fib(n-1) to stack
	push rax

	; call fib with n-2
	sub rdi, 2
	call fib

	; pop result of fib(n-1) from stack
	pop rsi

	; add fib(n-1) and fib(n-2)
	add rax, rsi
	ret

.base_case:
	mov rax, rdi
	ret