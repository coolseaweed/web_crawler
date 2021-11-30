#!/bin/bash




urls="https://note.com/notemag/m/m567dc56dbe84 https://note.com/notemag/m/md68de622a450 https://note.com/notemag/m/m37612976f600 https://note.com/notemag/m/mfe1c69f3b626 https://note.com/notemag/m/mbe11fbbc43b3 https://note.com/notemag/m/m60a43ce4c196 https://note.com/notemag/m/mf2e92ffd6658 https://note.com/notemag/m/m6d7dfb2cedc7 https://note.com/notemag/m/m943ece88b5f6 https://note.com/notemag/m/m0ec4d3a5a4b2 https://note.com/notemag/m/m57787022cedc https://note.com/notemag/m/m8af8e179073a https://note.com/notemag/m/m6b959e231ceb https://note.com/info/m/m4bd0825e8f53"

for url in $urls; do
    (
        echo $url;
        scrapy crawl bot_mag --nolog -a url=$url;
    )&
done




