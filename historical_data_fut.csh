#!/bin/bash

date_start=$1
date_end=$2
arg=$#
dir="/home/sachan/Quant/Data/raw/"

if [ $arg != 2 ]; then
echo "Usage:
historical_data.csh start_date end_date"
exit 0
fi

date_format_now=`date -d$date_start +%Y%m%d`
date_format_end=`date -d$date_end +%Y%m%d`

date=$date_format_now

echo "Parameters:
Start Date:$date_start
End Date:$date_end
Directory:$dir
Log File:/tmp/log.txt"
echo "Downloading Files from the NSE server===========>"

while [ "$date" -lt "$date_format_end" ]
do
date_format=`date -d$date +%d%^b%Y`
month=`date -d$date +%^b`
year=`date -d$date +%Y`
day=`date -d$date +%d`

fut_file=fut_${date_start}_${date_end}.csv
opt_file=opt_${date_start}_${date_end}.csv
cat /dev/null > ${dir}$fut_file
cat /dev/null > ${dir}$opt_file

wget -O  $dir${date}.zip -U firefox http://nseindia.com/content/historical/DERIVATIVES/${year}/${month}/fo${date_format}bhav.csv.zip >> /tmp/log.txt 2>&1
	unzip $dir${date}.zip -d${dir}
        echo $dir${date}.zip

        count=`ls -ltr ${dir}|grep csv|wc -l`
        echo $count
        if [ $count -eq 1 ];then
                head -n1 ${dir}fo${day}${month}${year}bhav.csv > ${dir}${fut_file}
                head -n1 ${dir}fo${day}${month}${year}bhav.csv > ${dir}${opt_file}
        fi
        echo ${dir}fo${day}${month}${year}bhav.csv
        cat ${dir}fo${day}${month}${year}bhav.csv|tail -n+2|grep -E "FUTSTK|FUTIDX|FUTIVX" >>${dir}${fut_file}
        cat ${dir}fo${day}${month}${year}bhav.csv|tail -n+2|grep -E "OPTSTK|OPTIDX" >>${dir}${opt_file}

date=`date -d"$date + 1 day" +%Y%m%d`
done

#Remove empty files
echo "Removing Empty Files ====================>"

if [ "$(ls -A $dir)" ]; then

for files in `ls $dir` 
do

if [ ! -s "$dir$files" ]; then
	#rm -f ${dir}fo${15}${month}${year}bhav.csv
	#Remove the zip file and create a whole csv file
	rm "$dir$files"

fi
done
fi


