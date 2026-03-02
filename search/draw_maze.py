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