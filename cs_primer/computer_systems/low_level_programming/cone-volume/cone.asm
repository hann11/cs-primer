default rel

section .rodata
	pi_over_three dd 1.0471975512


section .text
global volume
volume:
	mulss xmm0, xmm0
	mulss xmm0, [pi_over_three]
	mulss xmm0, xmm1
 	ret
