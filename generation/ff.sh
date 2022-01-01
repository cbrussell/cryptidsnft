# cd /mnt/e/output || exit
# mkdir videos
cd output || exit

ffmpeg -r 24 -start_number 0 -i "output%03d.png" -c:v libx264 -crf 12 -pix_fmt yuv420p out.mp4