#!/bin/bash



src_dir=$1
out_dir=$2



mkdir -p $out_dir

find $src_dir -type f -name '*.srt' -o -name '*.smi' | rename 's/ /_/g'
find $src_dir -type f -name '*.srt' -o -name '*.smi' | rename 's/-/_/g'
srt_list=$(find $src_dir -type f -name '*.srt')

for src in $srt_list; do 
    vtt_out=$(echo $src | sed 's/.srt/.vtt/g')
    ffmpeg -y -loglevel error -i $src $vtt_out
    out_file=$(basename $src | sed 's/.srt/.txt/g')
    cat $vtt_out | sed -e '1d' -E -e '/^$|]|>$|%$/d' | sed "s/^[0-9]*[0-9\:\.\ \>\-]*//g" | awk '!seen[$0]++' > $2/$out_file
done

