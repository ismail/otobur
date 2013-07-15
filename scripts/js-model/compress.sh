#!/bin/sh

java -classpath .:$PWD/../../android/libs/lzma.jar: SevenZip.LzmaAlone e schedule.data schedule.data.lzma
