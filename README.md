_This project has been created as part of the 42 curriculum by msuizu_

## **--- Description ---**

fly-in is a python project that designs an efficient drone routing system that navigates multiple drones\
through connected zones while minimizing simulation turns and handling movement constraints.

## **--- Instructions ---**

`make lint-strict` to check flake8 and mypy in strict

`make install` install dependencies

`make run` execute the challenger map by default\
or\
`python3 main.py <path_to_map.txt>`

`make clean` keep the project space clean

## **--- Resources ---**

[dijkstra algorithm](https://www.youtube.com/watch?v=b2vhFxthCA4)

AI was used for formula math (for drones' animation)

## **--- Algorithm ---**

the dijkstra algorithm was used to first calculate the lowest cost path, \
then simulate each drones' path with the given constraints to \
calculcate the coordinates of each drones for each turn in the simulation,\
to then pass it in the visulalizer part.

## **--- Visual representation ---**

the final animation is generated with matplotlib package. \
each frame is calculated to create a smooth animation with the help of numpy. \
the animation can be saved with the option in the main as a gif.
