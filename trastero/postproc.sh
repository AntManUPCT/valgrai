#/usr/bin/bash

for i in *.csv
do
	sort $i | uniq | shuf > post$i
	echo rm $i
done
