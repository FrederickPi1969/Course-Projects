# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
import numpy as np
from const import *

def computeCoordinate(start, length, angle):
    """Compute the end cooridinate based on the given start position, length and angle.

        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to couter-clockwise

        Return:
            End position of the arm link, (x-coordinate, y-coordinate)
    """
    # print(np.cos(angle))
    angle = angle / 360.0 * 2 * np.pi
    return (int(round(start[0] + np.cos(angle) * length)), int(round(start[1] - np.sin(angle) * length)))


def computeSecondLinkCoordinate(start, length, alpha, angle):
    angle = (angle + alpha) / 360.0 * 2 * np.pi
    return (int(round(start[0] + np.cos(angle) * length)), int(round(start[1] - np.sin(angle) * length)))

def computeThirdLinkCorrdinate(start, length, alpha, beta, angle):
    angle = (angle + alpha + beta) / 360.0 * 2 * np.pi 
    return (int(round(start[0] + np.cos(angle) * length)), int(round(start[1] - np.sin(angle) * length)))

# def calc_distance_from_center_to_line(abline, circle):
#     if x2 == x1:
#         return 
#     x1, y1 = abline[0][0], abline[0][1]
#     x2, y2 = abline[1][0], abline[1][1]
#     k = (y2 - y1) / (x2 - x1)
#     b = y1 - k * x1 
#     A = -1 * k
#     B = 1
#     C = -1 * b
#     a, b = circle[0], circle[1]
#     distance = np.abs(A * a + B * b + C) / np.sqrt(A ** 2 + B ** 2)
#     return distance

def check_sanity(arm, circle):
    start_x, start_y, end_x, end_y = arm[0][0], arm[0][1], arm[1][0], arm[1][1]
    center_x, center_y, r = circle[0],  circle[1], circle[2]
    distance1 = (start_x - center_x) ** 2 + (start_y - center_y) ** 2
    distance2 = (end_x - center_x) ** 2+ (end_y - center_y) ** 2
    if distance1 <= r ** 2 or distance2 <= r ** 2:
        return True 

    distance_start_center = np.sqrt(distance1)
    sin_alpha = r / distance_start_center 
    alpha = np.arcsin(sin_alpha)
    distance_end_center = np.sqrt(distance2) 
    arm_length = np.sqrt(((start_x - end_x)**2 + (start_y - end_y)** 2))
    cos_beta = (arm_length ** 2 + distance_start_center ** 2 - distance_end_center ** 2) / (2 * arm_length * distance_start_center)
    if np.abs(cos_beta) > 1:
        cos_beta = round(cos_beta, 1)

    beta = np.arccos(cos_beta)
    if beta > alpha: 
        return False 
    else: 
        return arm_length >= np.cos(alpha) * distance_start_center 




def doesArmTouchObstacles(armPos, obstacles):
    """Determine whether the given arm links touch obstacles

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            obstacles (list): x-, y- coordinate and radius of obstacles [(x, y, r)]

        Return:
            True if touched. False it not.
    """    
    for arm in armPos:
        for obs in obstacles:
            if check_sanity(arm, obs):
               return True  
    

    return False




def goal_cornercase_detection(arm, goals):
    armEnd = arm[-1][1]
    if doesArmTouchGoals(armEnd, goals):
        return False 

    return doesArmTouchObstacles(arm, goals)
    


def doesArmTouchGoals(armEnd, goals):
    """Determine whether the given arm links touch goals

        Args:
            armEnd (tuple): the arm tick position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]

        Return:
            True if touched. False it not.
    """

    goal = goals[0]
    distance = np.sqrt((armEnd[0] - goal[0]) ** 2 +  (armEnd[1] - goal[1]) ** 2)
    return distance < goal[2] or distance == goal[2]


def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False it not.
    """
    width, height = window[0], window[1]
    for arm in armPos:
        if (arm[0][0] > width or arm[0][1] > height or arm[0][0] < 0 or arm[0][1] < 0) or\
             (arm[1][0] > width or arm[1][1] > height or arm[1][0] < 0 or arm[1][1] < 0):
            return False
    return  True
