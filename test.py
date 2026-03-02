def gen_line(line: int, maze: list[list[list]], width: int) -> None:

    line_cell: list[list] = []

    for i in range(width):

        cell: list = [0, 0, 0, 0]
        if i == 0:
            cell[3] = 1
        else:
            if line_cell[i - 1][3] == 1:
                cell[1] = 1
        if line == 0 or maze[line-1][i][2] == 1:
            cell[0] = 1
        line_cell.append(cell)
    maze.append(line_cell)


def gen_first_line(width: int, maze: list[list[list]]) -> None:

    line_cell: list[list] = []

    for i in range(width):
        cell: list = [1, 0, 0, 0]
        if i == 0:
            cell[3] = 1
        elif i == width - 1:
            cell[1] = 1
        if i != 0 and line_cell[i - 1][1] == 1:
            cell[3] = 1
        line_cell.append(cell)
    maze.append(line_cell)


def gen_last_line(height: int, width: int, maze: list[list[list]]) -> None:

    line_cell: list[list] = []

    for i in range(width):
        cell: list = [0, 0, 1, 0]
        if i == 0:
            cell[3] = 1
        elif i == width - 1:
            cell[1] = 1
        if maze[height-3][i][2] == 1:
            cell[0] = 1
        if i != 0 and line_cell[i - 1][1] == 1:
            cell[3] = 1
        line_cell.append(cell)
    maze.append(line_cell)


def draw_maze(maze):
    """
    Dessine un labyrinthe fluide en utilisant les connexions entre cellules.
    Format cell : [Haut, Gauche, Bas, Droite] (1 = mur, 0 = vide)
    """
    if not maze:
        return

    # Caractères de construction
    H_LINE = "───"  # Ligne horizontale
    V_LINE = "│"    # Ligne verticale
    SPACE  = "   "  # Vide
    
    # Dictionnaire des jointures (Coins et T)
    # Clé : (Haut, Gauche, Bas, Droite) où 1 = connexion
    corners = {
        (0,0,1,1): "┌", (0,1,1,1): "┬", (0,1,1,0): "┐",
        (1,0,1,1): "├", (1,1,1,1): "┼", (1,1,1,0): "┤",
        (1,0,0,1): "└", (1,1,0,1): "┴", (1,1,0,0): "┘",
        (1,0,1,0): "│", (0,1,0,1): "─", (0,0,1,0): "╷",
        (1,0,0,0): "╵", (0,1,0,0): "╴", (0,0,0,1): "╶",
        (0,0,0,0): " "
    }

    height = len(maze)
    width = len(maze[0])

    for r in range(height):
        top_line = ""
        mid_line = ""
        
        for c in range(width):
            cell = maze[r][c]
            
            # 1. Calcul du COIN (Haut-Gauche de la cellule actuelle)
            # On regarde les voisins pour savoir si le coin doit être un +, un L, etc.
            up    = maze[r-1][c][1] if r > 0 else 0
            left  = maze[r][c-1][0] if c > 0 else 0
            down  = cell[1] # Mur Gauche de la cellule actuelle
            right = cell[0] # Mur Haut de la cellule actuelle
            
            top_line += corners.get((up, left, down, right), " ")
            
            # 2. Segment horizontal (Haut)
            top_line += H_LINE if cell[0] else SPACE
            
            # 3. Segment vertical (Gauche)
            mid_line += V_LINE if cell[1] else " "
            mid_line += SPACE # Intérieur de la cellule
            
            # Cas particulier : Fermeture de la dernière colonne (Droite)
            if c == width - 1:
                # Coin Haut-Droit final
                u_f = maze[r-1][c][3] if r > 0 else 0
                top_line += corners.get((u_f, cell[0], cell[3], 0), " ")
                # Mur droit final
                mid_line += V_LINE if cell[3] else " "
        
        print(top_line)
        print(mid_line)

    # 4. Ligne finale pour fermer le bas du labyrinthe
    last_line = ""
    for c in range(width):
        cell = maze[height-1][c]
        l = maze[height-1][c-1][2] if c > 0 else 0
        last_line += corners.get((cell[2], l, 0, cell[2]), " ")
        last_line += H_LINE if cell[2] else SPACE
        if c == width - 1:
            last_line += corners.get((cell[3], cell[2], 0, 0), " ")
    print(last_line)



def main() -> None:
    width: int = 4
    height: int = 4
    maze: list[list[list]] = []
    gen_first_line(width, maze)
    for i in range(height-2):
        gen_line(i, maze, width)
    gen_last_line(height, width, maze)
    for lines in maze:
        print("")
        for cell in lines:
            if cell == [0, 0, 0, 1]:
                print("1", end="")
            elif cell == [0, 0, 1, 0]:
                print("2", end="")
            elif cell == [0, 0, 1, 1]:
                print("3", end="")
            elif cell == [0, 1, 0, 1]:
                print("4", end="")
            elif cell == [0, 1, 0, 1]:
                print("5", end="")
            elif cell == [0, 1, 1, 0]:
                print("6", end="")
            elif cell == [0, 1, 1, 1]:
                print("7", end="")
            elif cell == [1, 0, 0, 0]:
                print("8", end="")
            elif cell == [1, 0, 0, 1]:
                print("9", end="")
            elif cell == [1, 0, 1, 0]:
                print("A", end="")
            elif cell == [1, 0, 1, 1]:
                print("B", end="")
            elif cell == [1, 1, 0, 0]:
                print("C", end="")
            elif cell == [1, 1, 0, 1]:
                print("D", end="")
            elif cell == [1, 1, 1, 0]:
                print("E", end="")
            elif cell == [1, 1, 1, 1]:
                print("F", end="")
            else:
                print(".", end="")
    print()
    draw_maze(maze)


if __name__ == "__main__":
    main()
