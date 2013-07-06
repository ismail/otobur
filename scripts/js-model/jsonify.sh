#!/bin/sh
#http://www.bursa.bel.tr/mobil/json.php?islem=hatlar
#http://www.bursa.bel.tr/mobil/json.php?islem=hat_durak&hat=1/A
#http://www.bursa.bel.tr/mobil/json.php?islem=durak_saatler&durak=D0432&hat=1/A

linesURL=$1

data=`curl -s $linesURL|iconv -f iso8859-9 -t utf-8`

cat << EOF | node | json_pp
a=$data
process.stdout.write(JSON.stringify(a))
EOF

