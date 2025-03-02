section .text
global fac

fac:
    cmp rdi, 1          ; Compare rdi with 1
    jle .base_case      ; If rdi <= 1, jump to base_case

    push rdi
    dec rdi
    call fac
    pop rdi
    imul rax, rdi
    ret

.base_case:
    mov rax, 1          ; Base case: return 1
    ret                 ; Return from the function