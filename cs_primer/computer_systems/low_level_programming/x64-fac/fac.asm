section .text
global fac

fac:
    mov rsi, 1        ; Initialize rsi to zero
    jmp fac_main        ; Jump to the main logic

fac_main:
    cmp rdi, 1
    jle .fin 
	imul rsi, rdi
    dec rdi
    call fac_main
    ret

.fin:
    mov rax, rsi
    ret