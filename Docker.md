# Overview

This repo also includes a Dockerfile which allows the turtlebot2 to be ran inside of a docker container. This has the advantage of allowing newer installations to interact with the turtlebot.

You can more learn about docker at https://www.freecodecamp.org/news/the-docker-handbook/

# Building Dockerfile

- dockerfile can be built with `docker build turtlebot:latest .` (assuming you are in the directory of the dockerfile)

# Starting docker container

- You can view all of your docker images with `docker image ls`
- You should see your recently built docker image `turtlebot:latest`
- Start this docker image with `docker run --net=host --privileged -it turtlebot:latest`
  - Note that `-it` will start the container interactively, alternatively you could start headlessly and use the steps in the interacting section to attach.
  - Note that `--privileged` passes ALL IO into the docker container, you can also manually specify which ports to give the docker container access to, this is generally better practice but is not done here as our setups are too variable to universally ensure which USB ports should be passed
  - Note that `--net=host` will pass the host machines network namespace into the container. This may lead to port conflicts.
- You can also start an instance with roscore using `docker run --net=host --privileged -it turtlebot:latest roscore`

# Interacting

You can also open additional interactive instances of your docker container

- `docker container ls`, this will show you some information including container ID. Copy down the container ID of your currently running `turtlebot:latest` image instance
- `docker exec -it {ContainerID} bash` will let you open up additional terminal instances
