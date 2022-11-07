#! /bin/sh
files= ls $1/*.min.tsv
for eachfile in $files
do
   blender animation.blend -b -P createVideo.py -- $eachfile ./videos/iso_cam ISO_CAM
   blender animation.blend -b -P createVideo.py -- $eachfile ./videos/rear_cam REAR_CAM
   blender animation.blend -b -P createVideo.py -- $eachfile ./videos/side_cam SIDE_CAM
done