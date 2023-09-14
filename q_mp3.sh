mkdir -p q_mp3
for i in ../Random-R2-D2-sound/*.mp3; do 
  echo $i
  lame --noreplaygain -b 64 --resample 22.05 -m m -h "${i}" q_mp3/`basename $i`
done
