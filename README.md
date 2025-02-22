# Local Video Streamer (lvs)

## Description

Stream video using lvs from any computer on your home network to any other computer on the same network. Any video file, or one of the attached camera device on a computer can be used as a video source for streaming.

### A Note to Users

This program provides `video_streamer` package, but is also a working implementation using that package to show some of the features we can get using it. So, it might have bugs. 

### A Note to Developers

The main focus of the package is to make it easy to get video frame by frame (thanks to [opencv](https://opencv.org)), from any computer on the network, which can then be modified in any way preferable. </br>

The package provides `video_streamer.py` module with following main classes -

* `MasterVideoIter` to get the video frame by frame from a camera or video file available in a computer.
* `SlaveVideoIter` to get get the video frame by frame over a network using sockets.

`stream_server.py` is somewhat complicated implementation which uses `MasterVideoIter` to read video and make it available to any program using `SlaveVideoIter`

Then there is the `dataclass_objects.py` module providing following main dataclasses -

* `StreamData` currently only holding `frame`, meaning that `SlaveVideoIter` receives and makes available one video frame at a time. It can be easily extended to include more data per frame, like perhaps an audio frame, making this a complete video with audio streaming program.
* `PreStreamDataByClient` and `PreStreamDataByServer` are only containers which are shared by client and the server before the streaming starts. Gives them a chance to negotiate settings, other data, etc.

## Features

* `lvs start` runs the server, and multiple clients can connect to it. Fewer clients will result in better performance generally.
* Server sleeps in 2 seconds intervals until a client requests the stream.
  * Advantage - Video file or camera is not used when no clients connect, making the source available for use by other services in the meantime, and does not waste processing power.
  * Disadvantage - While the camera will always return what it captures right now, Video file will be read from the beginning each time the server wakes up from the sleep.
* Sweep interval can be set for saved videos which deletes old video files ending with '.avi' in the filename
* Stream can be requested to include datetime information, with preferred text color, etc. Grayscale(black and white) stream can also be requested instead of colored.
* Following extensions connect to the running server to provide additional services -
  * `lvs e_http` extends stream service to clients using browser. Closes connection to the server and sleeps in 2 seconds intervals just like the server itself if no client(s) are connected for 10 seconds.
  * `lvs e_view` opens up a window showing video stream. Press `q` or `Q` when this window is selected to stop the video stream.
  * `lvs e_save` saves the video stream in one of the two given ways -
    * Keeps saving video stream continuously in specified length chunks.
    * Saves video of specified length chuck when detection occurs based on provided cascade classifier file

## Installation

Requires python 3.7 or above installed and available in `PATH`

### Windows Users

* Go to [python.org/downloads](https://python.org/downloads), and download python.
* Open downloaded file, select `Add Python 3.* to PATH`, and click `Install Now`

### Linux Users

* Install python3.7 or above using your linux distribution specific package manager.
For ubuntu, you can install it by entering `sudo apt install python3.7` in the terminal

### Installing lvs

Open command prompt or terminal, and enter `python3 -m pip install lvs`</br>
This should install lvs and all its dependencies.

## Usage

* First of all, I would encourage to have a look at or modify the default configuration file, because this configuration is the heart of this app's behavior. You can view it in terminal by typing `lvs cfg`, or better yet open it in your preferred editor. The file location can be found by entering `lvs cfg_path`. Most settings available in this configuration files can be overridden on the command line. This file contains comments which I hope will be very helpful to understand the program's requirements for use. Here's current copy of config.toml file

```
# log_level = <level>, a <level> could be "debug", "info", "warn",
# "critical", like log_level = "info"
# log_level = critical will show almost no information
log_level = "info"

# log_to_file = "" will not log to file
# log_to_file = "lvs_log.txt" will save log to <home>/`lvs_log.txt`
# where <home> is your home directory, like C:/Users/Me
log_to_file = ""


[server_address]

    # Use ip = "127.0.0.1" or "localhost" to connect to server streaming
    # on this device
    # If using stream server on other device, use that device's ip
    ip = "127.0.0.1"

    # Use port = 4289 for default, use something else if the stream server
    # is using different port
    port = 4289


[server_settings]

    # source = 0 will try to use default camera device
    # source = 1 will try to use next available camera device
    # source = "C:/Path/to/video.mp4" will use video.mp4
    source = 0

    # Use ip = "127.0.0.1" or "localhost" to serve on this device
    # Use ip = "0.0.0.0" to make this server available on local network
    ip = "0.0.0.0"

    # Use port = 4289 for default, use something else if not available
    # Clients will get served by this server when they connect on this port
    port = 4289

    # Number of connections to be queued for serving
    backlog = 0


[flask_settings]

    # Use ip = "127.0.0.1" or "localhost" to serve on this device
    # Use ip = "0.0.0.0" to make this server available on local network
    ip = "0.0.0.0"

    # Use port = 4288 for default, use something else if not available
    # Clients will get served by this server when connected to this port
    # Enter "<ip>:<port>" in the browser to access the video stream, where
    # <ip> shall be replaced by server ip like 192.168.1.23, and <port>
    # shall be replaced by port number like 1234
    # Note that :<port> can be omitted from entering in browser if port = 80,
    # however, using port = 80 may require privileged permissions to run
    port = 4288

    # Number of seconds to wait for closing connection to the server after
    # all browser clients have disconnected. Default sleep_delay = 10 seconds
    sleep_delay = 10

    # background_color = <color>, changes `index.html`'s background color,
    # where <color> is html background property such as "white", "gray", etc
    background_color = "gray"

    # debug = true, will show debug information on errors
    debug = false


[stream_settings]

    # grayscale = true will result in black and white colored video,
    # but may slightly improve performance
    grayscale = false

    # show_datetime = true will embed current datetime info as given by
    # server machine on top of video stream
    show_datetime = false

    # show_fps = true will show estimated frames per second served by server
    show_fps = false

    # Text color in BGR format i.e [Blue, Green, Red], [255, 0, 0] is blue
    # text_color = [255, 255, 255] is white, [0, 0, 0] is black
    text_color = [255, 255, 255]

    # font_scale = 1, size of font
    font_scale = 1

    # thickness = 1, text thickness, a whole number
    thickness = 2


[save_settings]

    # cascade classifier to use for detection purposes. Inside res folder
    # haarcascade_frontalface_default.xml has been copied from opencv,
    # location, <python-installed-here>/Python<version>/site-packages/cv2/data/*.xml
    cascade_classifier = "cascade_classifiers/haarcascade_frontalface_default.xml"

    # detection_interval = 15 means run detection on every 15th frame
    # Note that detection is computationally intensive task, and
    # lowering this value could lower performance. Minimum value is 1
    detection_interval = 15

    # dir_name = "lvs_saves" will result in saving videos inside lvs_saves folder
    dir_name = "lvs_saves"

    # save_dir = "" will default to user's home plus above mentioned dir_name
    # Example path for windows, save_dir = "C:/Users/Me/Videos"
    # Example path for linux, save_dir = "/home/Me/Videos"
    # Note that certain characters such as a  space ' ' need escaping like '\ '
    save_dir = ""

    # save_type = "continuous" will save all the time ignoring detection
    # save_type = "detection" will only save when detection occurs
    save_type = "continuous"

    # save_duration = 3600 will save videos in 3600 seconds video chunks for
    # save_type = "continuous" or save once for every detection when using
    # save_type = "detection"
    save_duration = 3600

    # older_than = 86400 will delete video files which were created 86400 seconds
    # (1 day) ago and end in ".avi" extension
    older_than = 86400

    # sweep_interval = 0 will result in not sweeping at all
    # sweep_interval = 3600 will check every 3600 seconds(1 hour) to find out
    # the files which should be deleted
    sweep_interval = 0

```

* `lvs --help` entered in command prompt or terminal will show help for the program in general, which can relate to Features defined above.

```
C:\Users\Harsh>lvs --help
Usage: lvs [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  cfg       Shows current configuration settings
  cfg_path  Shows location of configuration file currently in use
  e_http    Extension to serve video stream for client(s) using browser(s)
  e_save    Extension to help in saving video stream
  e_view    Extension to show video stream from a running stream server
  start     Starts the video stream server
  ```

* To get help for a particular feature like `e_view`, enter `lvs e_view --help` and so on. This will show default settings being used for the feature, but can be overridden

```
C:\Users\Harsh>lvs e_view --help
Usage: lvs e_view [OPTIONS]

  Extension to show video stream from a running stream server. Press 'q' to quit when running.

Options:
  --server_ip TEXT                [default: 127.0.0.1]
  --server_port INTEGER           [default: 4289]
  -G, --grayscale / --no-grayscale
                                  [default: False]
  -D, --show_datetime / --no-show_datetime
                                  [default: False]
  -F, --show_fps / --no-show_fps  [default: False]
  --text_color <INTEGER INTEGER INTEGER>...
                                  [default: 255, 255, 255]
  --font_scale INTEGER            [default: 1]
  --thickness INTEGER             [default: 2]
  --help                          Show this message and exit.
```

* Example streaming on same computer
  * Enter `lvs start` in a terminal to start video stream from default camera on this computer.
  * Open another terminal and enter `lvs e_view -D --text_color 0 255 0` This will show video stream with datetime information added on top left with red colored text.
* Example streaming over a network
  * First type `ipconfig` (only for windows) and find Ipv4 address, it might be something like `192.168.1.23`. Now enter `lvs start` to start the stream server.
  * Go to the computer where you would like to watch the stream. Enter `lvs e_view --server_ip="192.168.1.23"` as we found the address earlier.
