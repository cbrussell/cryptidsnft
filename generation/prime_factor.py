import math
 
def gridSize(n):
     
    grid = []
    a = math.sqrt(n)

    while n % a != 0:
        print("Trying again, not integer..")
        a = math.floor(a) -1
    b = n/a

    grid.append(int(b))
    grid.append(int(a))



    print(f'Highest two divisible factors are {int(b)} and {int(a)}')
    return grid
         

if __name__ == "__main__":
    gridSize()