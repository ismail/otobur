#!/bin/sh

linesURL=$1
data=`curl -s $linesURL|iconv -f iso8859-9 -t utf-8`

cat << EOF | node
a=$data
process.stdout.write(JSON.stringify(a))
EOF

