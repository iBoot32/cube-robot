"""
===============================================================================
ENGR 13300 Fall 2021

Program Description: Checks the solvability of a 2x2 Rubik's cube input. Basically another user-input error checking mechanism
    

Assignment Information
    Assignment:     Python Final Individual Project Fall 2021
    Author:         Tom O'Donnell, tkodonne@purdue.edu
    Team ID:        LC3 - 03

Contributor:   
    
    My contributor(s) helped me:
    [] understand the assignment expectations without
        telling me how they will approach it.
    [] understand different ways to think about a solution
        without helping me plan my solution.
    [] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.
    
ACADEMIC INTEGRITY STATEMENT
I have not used source code obtained from any other unauthorized
source, either modified or unmodified. Neither have I provided
access to my code to another. The project I am submitting
is my own original work.
===============================================================================
"""

color_occurances = {
    "W": 0,
    "O": 0,
    "G": 0,
    "R": 0,
    "B": 0,
    "Y": 0,
}

def validate(cube):
    # error checking #2
    # consists of three main checks:
    #   making sure only 24 stickers were entered
    #   making sure every sticker is a valid color
    #   making sure each color appears exactly 4 times
    # (i could add further checks like corner orientation parity, but these are sufficient most of the time)

    # check only entered 24 stickers
    if len(cube) != 24:
        print("  you have input too many / too little characters. exiting.")
        return False
    
    # loop through cube stickers and count up number of occurances of each color
    for x in range(0,24):
        # as a preliminary, make sure no invalid colors entered.
        if cube[x] not in color_occurances:
            print("  invalid color entered. exiting.")
            return False
        color_occurances[cube[x]] += 1
        
    for key in color_occurances:
        if color_occurances[key] != 4:
            print("  you have entered too many / too little of one or more colors. exiting.")
            return False
    return True
        