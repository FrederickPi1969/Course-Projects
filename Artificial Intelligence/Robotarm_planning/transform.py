
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *




def one_link_case(arm, goals, obstacles, window, granularity):
    arm1_base, arm1_tip = arm.getArmPos()[0]
    arm1_len = int(round(np.sqrt((arm1_base[0]- arm1_tip[0])** 2 + (arm1_base[1] - arm1_tip[1]) ** 2)))
    alpha_limit = arm.getArmLimit()[0]
    initial_angle = arm.getArmAngle()
    length = (alpha_limit[1] - alpha_limit[0]) // granularity + 1
    offset = [alpha_limit[0]]
    maze_map = [WALL_CHAR for i in range(length)]
    initial_pos = angleToIdx(initial_angle, offset, granularity)
    maze_map[initial_pos[0]] = START_CHAR
    print(goals)
    for alpha in range(alpha_limit[0], alpha_limit[1] + 1, granularity):
        arm1_end = computeCoordinate(arm1_base, arm1_len, alpha)

        arm_pos = [(arm1_base, arm1_end)]
        maze_pos = angleToIdx([alpha], offset, granularity)
      
        if doesArmTouchGoals(arm_pos[-1][1], goals):          
            maze_map[maze_pos[0]] = OBJECTIVE_CHAR
            continue

        if not isArmWithinWindow(arm_pos, window) or goal_cornercase_detection(arm_pos, goals):
            maze_map[maze_pos[0]] = WALL_CHAR
            continue

        if maze_map[maze_pos[0]] == "P":
            continue 
        
        maze_map[maze_pos[0]] = " "

    print(maze_map)

    return maze_map


def three_links_case(arm, goals, obstacles, window, granularity):
    arm1_base, arm1_tip = arm.getArmPos()[0]
    arm2_base, arm2_tip = arm.getArmPos()[1]
    arm3_base, arm3_tip = arm.getArmPos()[2]
    arm1_len, arm2_len, arm3_len = int(round(np.sqrt((arm1_base[0]- arm1_tip[0])** 2 + (arm1_base[1] - arm1_tip[1]) ** 2))),\
        int(round(np.sqrt((arm2_base[0]- arm2_tip[0])** 2 + (arm2_base[1] - arm2_tip[1]) ** 2))),\
        int(round(np.sqrt((arm3_base[0]- arm3_tip[0])** 2 + (arm3_base[1] - arm3_tip[1]) ** 2)))
    alpha_limit, beta_limit, gamma_limit = arm.getArmLimit()[0], arm.getArmLimit()[1], arm.getArmLimit()[2]
    initial_angle = arm.getArmAngle()
    width = (alpha_limit[1] - alpha_limit[0]) // granularity + 1
    height = (beta_limit[1] - beta_limit[0]) // granularity + 1
    length = (gamma_limit[1] - gamma_limit[0]) // granularity + 1
    offset = [alpha_limit[0], beta_limit[0], gamma_limit[0]]
    maze_map = np.array([[[" " for i in range(length)] for j in range(height)] for k in range(width)])
    initial_pos = angleToIdx(initial_angle, offset, granularity)
    print(initial_pos)
    maze_map[initial_pos[0]][initial_pos[1]][initial_pos[2]] = START_CHAR

    for alpha in range(alpha_limit[0], alpha_limit[1] + 1, granularity):
        arm1_end = computeCoordinate(arm1_base, arm1_len, alpha)
        arm_pos = [(arm1_base, arm1_end)]
        maze_pos = angleToIdx([alpha], offset, granularity)
        
        if not isArmWithinWindow(arm_pos, window) or doesArmTouchObstacles(arm_pos, obstacles):
            maze_map[maze_pos[0]][:][:] = WALL_CHAR
            continue 
        
        if goal_cornercase_detection(arm_pos, goals):
            maze_map[maze_pos[0]][:][:] = WALL_CHAR
            continue

        for beta in range(beta_limit[0], beta_limit[1] + 1, granularity):
            arm2_end = computeSecondLinkCoordinate(arm1_end, arm2_len, alpha, beta)
            arm_pos = [(arm1_end, arm2_end)]
            maze_pos = angleToIdx([alpha, beta], offset, granularity)

            if not isArmWithinWindow(arm_pos, window) or doesArmTouchObstacles(arm_pos, obstacles):
                maze_map[maze_pos[0]][maze_pos[1]][:] = WALL_CHAR
                continue
        
            if goal_cornercase_detection(arm_pos, goals):
                maze_map[maze_pos[0]][maze_pos[1]][:] = WALL_CHAR
                continue

            for gamma in range(gamma_limit[0], gamma_limit[1] + 1, granularity):
                arm3_end = computeThirdLinkCorrdinate(arm2_end, arm3_len, alpha, beta, gamma)

                arm_pos = [(arm2_end, arm3_end)]
                maze_pos = angleToIdx([alpha, beta, gamma], offset, granularity)

                if not isArmWithinWindow(arm_pos, window) or doesArmTouchObstacles(arm_pos, obstacles):
                    maze_map[maze_pos[0]][maze_pos[1]][maze_pos[2]] = WALL_CHAR 
                    continue

                if doesArmTouchGoals(arm_pos[0][1], goals):
                    ## set the corresponding pos on maze to goal.          
                    maze_map[maze_pos[0]][maze_pos[1]][maze_pos[2]] = OBJECTIVE_CHAR
                    continue

                if goal_cornercase_detection(arm_pos, goals):
                    maze_map[maze_pos[0]][maze_pos[1]][maze_pos[2]] = WALL_CHAR
        

    return maze_map










def two_links_case(arm, goals, obstacles, window, granularity):
    arm1_base, arm1_tip = arm.getArmPos()[0]
    arm2_base, arm2_tip = arm.getArmPos()[1]
    arm1_len, arm2_len = int(round(np.sqrt((arm1_base[0]- arm1_tip[0])** 2 + (arm1_base[1] - arm1_tip[1]) ** 2))), int(round(np.sqrt((arm2_base[0]- arm2_tip[0])** 2 + (arm2_base[1] - arm2_tip[1]) ** 2)))
    alpha_limit, beta_limit = arm.getArmLimit()[0], arm.getArmLimit()[1]
    initial_angle = arm.getArmAngle()
    height = (alpha_limit[1] - alpha_limit[0]) // granularity + 1
    width = (beta_limit[1] - beta_limit[0]) // granularity + 1
    offset = [alpha_limit[0], beta_limit[0]]
    maze_map = [[" " for i in range(width)] for j in range(height)]  

    initial_pos = angleToIdx(initial_angle, offset, granularity)
    maze_map[initial_pos[0]][initial_pos[1]] = START_CHAR


    for alpha in range(alpha_limit[0], alpha_limit[1] + 1, granularity):
        arm1_end = computeCoordinate(arm1_base, arm1_len, alpha)
        for beta in range(beta_limit[0], beta_limit[1] + 1, granularity):
            arm2_end =  computeSecondLinkCoordinate(arm1_end, arm2_len, alpha, beta)
            arm_pos = [(arm1_base, arm1_end), (arm1_end, arm2_end)]
            maze_pos = angleToIdx([alpha, beta], offset, granularity)

            if not isArmWithinWindow(arm_pos, window):
                maze_map[maze_pos[0]][maze_pos[1]] = WALL_CHAR 
                continue

            if doesArmTouchObstacles(arm_pos, obstacles):
                ## set the corresponding to obstacle       
                maze_map[maze_pos[0]][maze_pos[1]] = WALL_CHAR     
                continue

            if doesArmTouchGoals(arm_pos[1][1], goals):
                ## set the corresponding pos on maze to goal.          
                maze_map[maze_pos[0]][maze_pos[1]] = OBJECTIVE_CHAR
                continue

            if goal_cornercase_detection(arm_pos, goals):
                maze_map[maze_pos[0]][maze_pos[1]] = WALL_CHAR
        
    # print(maze_map)
    return maze_map







def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.
    
        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    link = arm.getNumArmLinks()
    offset = []

    for temp in arm.getArmLimit():
        offset.append(temp[0])
    
    if link == 1:
        maze = one_link_case(arm, goals, obstacles, window, granularity)
        return Maze(maze, offset, granularity)

    elif link == 2:
        maze = two_links_case(arm, goals, obstacles, window, granularity)
        return Maze(maze, offset, granularity)

    elif link == 3:
        maze = three_links_case(arm, goals, obstacles, window, granularity)
        return Maze(maze, offset, granularity)

