#! /bin/bash
cur_dir=`dirname  ${0}`
cd  ${cur_dir}
last=""
while [ $# -gt 0 ]
do
    if [ $1 == *Application ]
    then
        last=${1}
        continue
    fi
    if [ -n ${last} ]
    then
        src="${last}\ ${1}"
    else
        src="${1}"
    fi
    cp  "$src" .
    base=`basename $1`
    echo https://github.com/WinChua/blog/blob/master/asset/${base}
    shift
done

git add .
git commit -m "up pic"
git push
