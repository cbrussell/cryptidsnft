cd output || exit
mkdir videos
cd raw || exit

for i in {1..20}
do
    cd "${i}" || exit

    ffmpeg -f image2 -framerate 24 -i "${i}_%03d.png" -vf scale=590x590,palettegen palette.png

    ffmpeg -f image2 -framerate 24 -i "${i}_%03d.png" -i palette.png -filter_complex "[0]scale=590x590[j];[j][1]paletteuse" ../../videos/"${i}_test7".gif


    # ffmpeg -y -r 24 -start_number 0 -stream_loop 1 -i "${i}_%03d.png"  -c:v libx264 -crf 12 -pix_fmt yuv420p ../../videos/"${i}".mp4 
    # ffmpeg -f image2 -framerate 24 -i "${i}_%03d.png" -loop -1 -vf scale=590x590 -r 24  ../../videos/"${i}_test7".gif
    
    cd ..
    done