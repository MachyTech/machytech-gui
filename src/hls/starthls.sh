#!/bin/sh
DIR=/home/timo/Projects/machytech/machytech-gui/src/video
mkdir -p $DIR
( cd $DIR && gst-launch-1.0 rtspsrc location="rtsp://192.168.178.116:8554/test" latency=2000 ! decodebin ! autovideoconvert ! x264enc bitrate=512 tune=zerolatency ! mpegtsmux ! hlssink playlist-root=http://192.168.178.203:5000/video/ location=/home/timo/Projects/machytech/machytech-gui/src/video/segment_%05d.ts )
rm -r $DIR
