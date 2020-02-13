# Duckieshock 4
Simple ROS node that connects PS4 controller (Sony Dualshock 4) to a duckiebot to control it remotely.

1. Start roscore Docker container on duckiebot (should be started automatically)
2. Start joystick demo on duckiebot
   - ``dts duckiebot demo --demo_name joystick --duckiebot_name <duckiebot name>``
   - ... or through Portainer interface
3. ``export ROS_MASTER_URI=http://<duckie IP>:11311``
4. ``export ROS_IP=<computer IP>``
5. Plug in PS4 controller with USB
6. python2 control.py
   - Should work with Python 3.6 as well, 3.7 is broken for now (pyglet doesn't fully support 3.7 at time of creation)
