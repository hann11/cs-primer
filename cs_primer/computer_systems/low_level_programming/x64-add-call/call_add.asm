section .text
    global call_add

call_add:
    ; Call the add function
    call add

    ; The result is now in rax
    ; Return from the function
    ret

add:
    ; Add the two numbers
    add rdi, rsi
    ; Move the result to rax
    mov rax, rdi
    ; Return from the function
    ret