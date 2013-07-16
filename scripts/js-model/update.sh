#!/bin/sh

time ./js2schedule.py &&
./sorter.py schedule.data &&
./printer.py sorted.data > schedule.txt &&
mv sorted.data schedule.data &&
rm schedule.data.lzma &&

java -classpath .:$PWD/../../android/libs/lzma.jar: SevenZip.LzmaAlone e schedule.data schedule.data.lzma
