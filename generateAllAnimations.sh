#! /bin/sh
files= ls $1/*.min.tsv
for eachfile in $files
do
   blender animation.blend -b -P createGLTFAnimation.py -- $eachfile ./gltf/
done