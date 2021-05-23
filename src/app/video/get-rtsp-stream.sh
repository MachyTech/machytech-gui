gst-launch-1.0 rtspsrc location="rtsp://192.168.178.116:8554/test" latency=200 ! decodebin ! autovideoconvert ! clockoverlay ! x264enc tune=zerolatency ! mpegtsmux ! hlssink location=/home/timo/Projects/machytech/machytech-gui/src/app/video/segment_%05d.ts target-duration=5 max-files=5
#gst-launch-1.0 rtspsrc location="rtsp://192.168.178.116:8554/test" ! rtph265depay ! avdec_h265 ! clockoverlay ! videoconvert ! x264enc bitrate=1024 ! mpegtsmux ! hlssink location=/home/timo/Projects/machytech/machytech-gui/src/app/video/segment_%05d.ts target-duration=5

