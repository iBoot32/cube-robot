"""
===============================================================================
ENGR 13300 Fall 2021

Program Description: Final Project: A Rubik's Cube solver using buffers and iterative piece solving
    

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
import math
from datetime import datetime
import cube_checker
from cube_checker import validate

solved = False
cube_arr = []
setup = ""
sticker = 0
undo = ""
stick = ""
run = 0

#define which stickers on cube belong to which pieces
pieces = [
    [0, 4, 17],
    [1, 13, 16],
    [2, 12, 9],
    [3, 5, 8],
    [20, 6, 11],
    [21, 15, 10],
    [22, 14, 19],
    [23, 7, 18]
    ]

solved_cube = [
    'W','W','W','W','O','O','O','O','G','G','G','G','R','R','R','R','B','B','B','B','Y','Y','Y','Y']

# define which swaps to perform based on which sticker we shoot to
# for example, swaps[6] refers to the stickers the buffer will swap with,
# if we shoot to sticker 6 (indexed from zero). Since 0, 4, and 6 refer to 
# all the stickers of the buffer, cube_arr[0] will swap with swaps[6][0],
# cube_arr[4] with swaps[6][1], and cube_arr[14] with swaps[6][2].
# this completes a corner swap of the buffer and sticker 6's piece.
swaps = [
    
    [], [1, 16, 13], [2, 12, 9], [3, 8, 5], # face 1
    [], [5, 3, 8], [6, 11, 20], [7, 23, 18], # face 2 and so on
    [8, 5, 3], [9, 2, 12], [10, 15, 21], [11, 20, 6],
    [12, 9, 2], [13, 1, 16], [14, 19, 22], [15, 21, 10],
    [16, 13, 1], [], [18, 7, 23], [19, 22, 14],
    [20, 6, 11], [21, 10, 15], [22, 14, 19], [23, 18, 7],
    
    ]


def check_if_solved(arr):
    for stick in range(0,24):
        if solved_cube[stick] != cube_arr[stick]:
            # if any sticker om the cube does not match sticker in same location of a solved cube
            # then the cube must be unsolved
            return False
                
            
def handle_twisted_buffer(arr):
    global sticker
    global cube_arr
    
    # if we're here, the buffer is either twisted in place or solved
    # this means the program will see a piece in the buffer, and be like,
    # "oh, this piece belongs at sticker zero!" which leads to an infinite loop.
    # how do we fix this?
    # the way i chose is to shoot the buffer to some random unsolved piece
    # so we have an unsolved piece in the buffer again, and continue as normal.
    
    for stick in range(0,24):
        # loop through stickers to find an unsolved one
        if solved_cube[stick] != cube_arr[stick] and stick != 0 and stick != 4 and stick != 17:
            sticker = stick # we found one
            break;
            
    
    
    # we found a sticker that is unsolved, 
    # now we iterate through the pieces array to find which piece the sticker belongs to
    for x in range(0,8):
        for i in range(0,3):
            if pieces[x][i] == stick:
                piece = x
                break
    
    # find the remaining stickers on that piece and solve the piece
    pieceindexes = pieces[piece]
    solve_piece(solved_cube[pieceindexes[0]] + solved_cube[pieceindexes[1]] + solved_cube[pieceindexes[2]], cube_arr)
        
    return
    
def update_cube_state(sticker):
    # basically does what i described above at the swaps array definition
    cube_arr[0], cube_arr[swaps[sticker][0]] = cube_arr[swaps[sticker][0]], cube_arr[0]
    cube_arr[4], cube_arr[swaps[sticker][1]] = cube_arr[swaps[sticker][1]], cube_arr[4]
    cube_arr[17], cube_arr[swaps[sticker][2]] = cube_arr[swaps[sticker][2]], cube_arr[17]
    
    return
    
        
    
def solve_piece(p, arr):
    global run
    global cube_arr
    # take a certain piece on the cube as input and determine where it belongs
    # determines the setup moves required to move the sticker to the swap location
    global setup
    global undo
    global sticker
    
    if run == 10:
        quit()

    
    
    if "W" in p and "O" in p and "B" in p:
        # buff solved, however
        # we verified cube is not solved so that means 
        # we have a solved buffer yet other pieces not solved
        handle_twisted_buffer(arr)
        return
    elif "W" in p and "R" in p and "B" in p:
    # change this to an array of setups and undos so can access
        if p[0] == "W":
            setup = "R D'"
            undo = "D R'"
            sticker = 1
        elif p[0] == "R":
            setup = "R2"
            undo = "R2'"
            sticker = 13
        else:
            setup = "R' F"
            undo = "F' R"
            sticker = 16
    elif "W" in p and "R" in p and "G" in p:
        if p[0] == "W":
            setup = "F"
            undo = "F'"
            sticker = 2
        elif p[0] == "R":
            setup = "R'"
            undo = "R"
            sticker = 12
        else:
            setup = "F2 D"
            undo = "D' F2"
            sticker = 9
    elif "W" in p and "O" in p and "G" in p:
        if p[0] == "W":
            setup = "L D L'"
            undo = "L D' L"
            sticker = 3
        elif p[0] == "O":
            setup = "F2"
            undo = "F2"
            sticker = 5
        else:
            setup = "F' D"
            undo = "D' F"
            sticker = 8
    elif "Y" in p and "O" in p and "G" in p:
        if p[0] == "Y":
            setup = "F'"
            undo = "F"
            sticker = 20
        elif p[0] == "O":
            setup = "D2 R";
            undo = "R' D2"
            sticker = 6
        else:
            setup = "D"
            undo = "D'"
            sticker = 11
    elif "Y" in p and "O" in p and "B" in p:
        if p[0] == "Y":
            setup = "D F'"
            undo = "F D'"
            sticker = 23 
        elif p[0] == "O":
            setup = "D2";
            undo = "D2"
            sticker = 7
        else:
            setup = "D' R"
            undo = "R' D"
            sticker = 18
    elif "Y" in p and "G" in p and "R" in p:
        if p[0] == "Y":
            setup = "D' F'"
            undo = "F D"
            sticker = 21
        elif p[0] == "G":
            setup = "F D";
            undo = "D' F'"
            sticker = 10
        else:
            setup = ""
            undo = ""
            sticker = 15
    elif "Y" in p and "R" in p and "B" in p:
        if p[0] == "Y":
            setup = "D2 F'"
            undo = "F D2"
            sticker =  22
        elif p[0] == "R":
            setup = "R";
            undo = "R'"
            sticker = 14
        else:
            setup = "D'"
            undo = "D"
            sticker = 19
       
    # move piece to swap location, swap buffer and piece, undo setup moves.
    print(f'  {setup} R U\' R\' U\' R U R\' F\' R U R\' U\' R\' F R {undo}')
    update_cube_state(sticker)
    run = run + 1
    return
    
    

def solve_cube(arr):
    global sticker
    global cube_arr
    
    print("")    
    print("   solution to your cube:")
    print("")
    
    # this line here actually functions as error checking algorithm #1
    # it jumps to the check_if_solved function, and verifies we only keep solving the cube if the cube is unsolved, and exits if it is.
    while(check_if_solved(arr) == False):
        solve_piece(arr[pieces[0][0]] + arr[pieces[0][1]] + arr[pieces[0][2]], arr)
        
    # when the loop breaks, the cube is solved. 
    # so we do some math to find the elapsed solve time, and it's mission accomplished.
    endtime = datetime.now()
    elapsed = endtime - starttime
    print("")
    print(f'   cube solved in {elapsed.microseconds / 1000000} seconds')
    print("   py_cubebot by tom o'donnell")
    print("   written for engr133 at purdue university")
    return

def main():
    global cube_arr
    global starttime
    
    starttime = datetime.now()
    
    cube_str = input("Input cube state (type \"help\" for help): ")
    if cube_str == "help":
        print(f'\n ORDER TO INPUT YOUR CUBE: ')
        print(f' Example: WWWWOOOOGGGGRRRRBBBBYYYY')
        
        #print diagram of cube showing in what order to input cube's stickers
        print(r"""
		                 _________________ 
		                 |       |       |
		                 |   1   |   2   |
		                 |-------|-------|
		                 |   4   |   3   |
		                 |_______|_______|
    _________________    _________________    _________________    _________________ 
    |       |       |    |       |       |    |       |       |    |       |       |
	|   5   |   6   |    |   9   |   10  |	  |   13  |   14  |    |   17  |   18  |
	|-------|-------|    |-------|-------|	  |-------|-------|    |-------|-------|
	|   8   |   7   |    |   12  |   11  |	  |   16  |   15  |    |   20  |   19  |
	|_______|_______|    |_______|_______|	  |_______|_______|    |_______|_______|
                         _________________ 
		                 |       |       |
		                 |   21  |   22  |
		                 |-------|-------|
		                 |   24  |   23  |
		                 |_______|_______|


                """)
    else:
        #example could be WWWWOOOOGGGGRRRRBBBBYYYY, 
        #split cube_str by letters to get array with each element being 1 sticker
        cube_arr = [sticker for sticker in cube_str]
        
        
        # error checking algorithm #2
        # calls an external file equipped to check if the user's input is likely to be correct
        # makes sure that you only entered 24 stickers, and that there's exactly 4 of each color, and so on
        if(validate(cube_arr) == False):
            return
        
        #cube array is set up, now we call solving function while passing cube array
        solve_cube(cube_arr)
    return

if __name__ == "__main__":
    main()