#! /bin/bash
cur_dir=`dirname  ${0}`
cd  ${cur_dir}
while [ $# -gt 0 ]
do
    cp  $1 .
    shift
done

git add .
git commit -m "up pic"
git push
