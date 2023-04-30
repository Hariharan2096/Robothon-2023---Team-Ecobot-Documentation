# Robothon-2023---Team-Ecobot-Documentation


QUICK START GUIDE:
1.	Turn on the robot controller and bring the robot to the camera pose for capturing the task board.
2.	Connect to robot IP using wireless/wired connection and switch to remote control mode in teach pendent.
3.	Open Visual Studio Code and load the workspace where the main Python program is present.
4.	Position the task board sturdily on the workbench using the velcro strips and connect the camera and task board to the workstation.
5.	Choose the order of the execution of tasks by rearranging the task calls in the main program.
6.	Run the Python script.
  a.	Feature and orientation detection of the taskboard using the camera.
    i.	To begin with, the robot is positioned in the macro capture pose where the rough location of the red button is detected on the image pixel plane using image processing techniques.
    ii.	Detected pixel point is de-projected into the world coordinates using rs2_deproject_pixel_to_point(...) function in pyrealsense2 library.
    iii.	Robot moves to the micro capture pose - the camera frame origin is located directly above the red button at a height of 250 mm and the red button is detected again to get an accurate location.
    iv.	Pixel point is again de-projected into the world coordinate frame to get the red button centre.
    v.	All the features in the taskboard such as the blue button, slider location, and probe test port are calculated from the red button centre using mathematical and geometric methods.
  b.	The robot will start the trial by pushing the blue button and continue to execute the tasks in the order specified.
  c.	Once the task execution is completed, the robot will finish the trial by pushing the red button.
