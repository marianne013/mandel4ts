#!/bin/env tcsh
@ l = 0
while ($l<3000)
  echo $l
  python mandelbrot.py -P 0.0001 -L $l -N 500 data_$l.bmp &
  @ l += 500
end
