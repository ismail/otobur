#!/bin/sh

./sorter.py schedule.data
mv sorted.data schedule.data
rm schedule.data.lzma

java -classpath .:$PWD/../../android/libs/lzma.jar: SevenZip.LzmaAlone e schedule.data schedule.data.lzma
