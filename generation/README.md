# Launch Timeline

### Prelaunch  

1. Upload default image/metadata using `1_get_default_json.py`

1. Use `generate.py` to generate PNG sequences (72 frames)
2. Use `ff.sh` to convert sequences into 12 second videos (initial frames, looped 3 times)
3. Calculate provenance of collection using still frames (frist frame of video) with `0_calculate_provenance.py`.
4. Update contract with provenance hash and freeze it
5. Based on shift value (community genereated) - copy shift stills, videos, and metadata file names. Keep originals for future reference. 

### Initial reveal
6. For amount sold, Upload video files and stills onto IPFS with `1_upload_images_get_initial_cid.py` - get two CIDs.
7. Use the resulting still and video CIDs to generate final metadata with `metadata.py`.
8. Upload final metadata to IPFS.
9. Update baseURI of contract with returned final metadata CID
10. Repeat 6-10 until sold out.

### Once sold out  
11. Freeze baseURI.


