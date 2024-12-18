top so question;
why processing sorted array faster than unsorted?
leaking of the microarch?

can be to do with branch prediction
given size of pipelines on CPU, substantal penalty for branch mis-prediction

try to write branchless code where you can, if the compiler cant find a branchless approach / where branch predictor not setup for success.

problem:
given a bitmap file, outputs an 8bit quantized version
bmp; each pixel encoded uses 24bits, 8bits for rgb channels

8bit; 3-3-2 bit RGB channels. get 256 possible colours
3r,3g,2b.

program outputs 8bit version of bmp

given in the files; 2 bmp files to play with.

core work in quantize.c won't need to change other files to do teh exercise

fix the quantize function. super branchy

given r,g,b byte values (3 bytes separately) return 1 byte value

convert.c will invoke quantize on the color channel bytes

Google Benchmark doesn't seem to work locally for me, so can run
`make convert`
`./convert filepath outpath`

timer
`time ./convert teapots.bmp teapots_out.bmp`

think about how you're actually making improvements, how to extend it etc.

consider branch misprediction on sprinkles.bmp
