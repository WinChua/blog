#! /bin/bash
cur_dir=`dirname  ${0}`
cd  ${cur_dir}
while [ $# -gt 0 ]
do
    cp  "$1" .
    base=`basename "$1"`
    echo https://github.com/WinChua/blog/blob/master/asset/${base}
    shift
done

git add .
git commit -m "up pic"
git push
