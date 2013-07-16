#!/bin/sh

time ./js2schedule.py &&
./sorter.py schedule.data &&
./printer.py sorted.data > schedule.txt &&
mv sorted.data schedule.data &&
rm schedule.data.xz &&
xz -6e schedule.data
