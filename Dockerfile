FROM ros:kinetic

RUN apt update && apt upgrade -y
RUN mkdir -p ~/catkin_ws/src
RUN cd ~/catkin_ws/src \
  && git clone https://github.com/jsinapov/tufts_service_robots.git

RUN bash -c " source /opt/ros/kinetic/setup.bash && \
            cd ~/catkin_ws \
            catkin_make"

RUN bash -c "cd ~/catkin_ws \
 && rosdep install --from-paths src --ignore-src --rosdistro kinetic -y "
RUN apt install ros-kinetic-turtlebot* ros-kinetic-astra-* -y
RUN apt install git chrony -y
RUN echo "export TURTLEBOT_3D_SENSOR=astra" >> ~/.bashrc
RUN echo "export TURTLEBOT_BATTERY=/sys/class/power_supply/BAT1" >> ~/.bashrc
RUN echo "echo ROS_DISTRO=kinetic" >> ~/.bashrc
RUN echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
RUN echo "export TURTLEBOT_BASE=kobuki" >> ~/.bashrc