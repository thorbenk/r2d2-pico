mkdir -p mp3
for i in *.wav; do 
  echo $i
  lame --noreplaygain -b 64 -m m -h "${i}" "mp3/${i%.wav}.mp3"
done
