cd output || exit
cd videos


ffmpeg -t 2 -i 3d-bite_loop.mp4 -filter_complex "[0:v] scale=w=80:h=-1,split [a][b];[a] palettegen=stats_mode=single [p];[b][p] paletteuse=new=1" 3d-bite_loop.gif

# ffmpeg -t 4.0 -i 3d-bite_loop.mp4 -filter_complex "[0]reverse[r];[0][r]concat=n=2:v=1:a=0,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" 1_test6.gif


# mkdir videos
# cd raw || exit

# for i in {1..1}
# do
    # cd "${i}" || exit
    # ffmpeg -y -r 24 -start_number 0 -stream_loop 1 -i "${i}_%03d.png"  -c:v libx264 -crf 12 -pix_fmt yuv420p ../../videos/"${i}".mp4 

# ffmpeg -ss 1:24 -t 2 -i 3d-bite_loop.mp4 -filter_complex "[0:v] fps=15,scale=w=128:h=-1,split [a][b];[a] palettegen=stats_mode=single [p];[b][p] paletteuse=new=1" 3dloop.gif

    # cd ..

# ffmpeg -i 1.gif -f mp4 -pix_fmt yuv420p benji.mp4

# ffmpeg -ss 61.0 -t 2.5 -i StickAround.mp4 -filter_complex "[0:v] palettegen" palette.png
# $ ffmpeg -ss 61.0 -t 2.5 -i StickAround.mp4 -i palette.png -filter_complex "[0:v][1:v] paletteuse" prettyStickAround.gif
# done

 