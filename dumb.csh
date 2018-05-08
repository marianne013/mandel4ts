#!/bin/env tcsh
@ l = 0
while ($l<8000)
  echo $l
  python mandelbrot.py -P 0.0005 -M 1000 -L $l -N 200 data_$l.bmp &
  @ l += 200
end
