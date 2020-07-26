This is my first University Python project. The program displays a
group of black dots. When you press "x" you add a infected into
the group, which appears as a red dot. If the red dot touches
any of the black dots, the touched black dot turns red, and is
also labelled an infected. You can reset the program by pressing "z"
"c" cures all infected.

Over a period of time, infected will be cured.

There is a bug which causes some infected to not infect correctly.
This is due to inefficient collisions as the dot has moved off the
infected dot before it is found in the for looped list of infected.