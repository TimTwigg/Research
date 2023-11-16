<h1 align = "center">Mixed Ability Play GUI</h1>

## Note on Camera
The Camera component is capable of downloading the image, but it downloads to the user's download folder. We will probably have to use the python program to take images still.

### Possible Flow
- display live feed on website to position
- click button on web interface to take the picture
    - take a screenshot and display to the side
    - disconnect the camera
    - send message to python program through flask to take images
        - send msg back through flask on completion to recapture camera? or just try and wait?
    - reconnect camera
- python module will change focus to MC and run the commands