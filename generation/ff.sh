cd output || exit
mkdir videos
cd raw || exit

for i in {1..10}
do
    cd "${i}" || exit
    ffmpeg -r 24 -start_number 0 -i "${i}_%05d.png" -c:v libx264 -crf 12 -pix_fmt yuv420p ../../videos/"${i}".mp4
    cd ..
    done