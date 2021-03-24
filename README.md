# machytech-gui

code used for the graphical user interface.

## getting started
```
pip install requirements.txt
python run.py
```
## Docker container

use the dockerfile in repository.
```
docker build image -t machytech-ui .
```
then run the image in a container
```
docker run -dp 5000:5000 machytech-ui
```
remove old images....
```
docker image rm --force machytech-ui:latest
```
stop the container with the name in docker ls.
```
docker stop name
```