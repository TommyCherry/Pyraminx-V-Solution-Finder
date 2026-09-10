from collections import deque

# Edge position / piece constants
GR = 0  # Green-Red
RB = 1  # Red-Blue
BG = 2  # Blue-Green
GY = 3  # Green-Yellow
RY = 4  # Red-Yellow
BY = 5  # Blue-Yellow

# Center constants (A center is identified by the color that it does NOT contain)
G = 0   # Green
R = 1   # Red
B = 2   # Blue
Y = 3   # Yellow

MOVES = ("U", "U'", "L", "L'", "R", "R'", "B", "B'")

FACE_EDGES = {
    G: (GR, BG, GY),
    R: (GR, RB, RY),
    B: (RB, BG, BY),
    Y: (GY, RY, BY)
}

FACE_CENTERS = {
    G: (R, B, Y),
    R: (G, B, Y),
    B: (G, R, Y),
    Y: (G, R, B)
}

class Pyraminx:
    def __init__(self):
        # ------------------------------------------------------------
        # EDGE POSITIONS
        # ------------------------------------------------------------
        # edges[position] = edge piece currently occupying that position
        #
        # Positions and pieces use the same constants:
        #   GR = Green-Red
        #   RB = Red-Blue
        #   BG = Blue-Green
        #   GY = Green-Yellow
        #   RY = Red-Yellow
        #   BY = Blue-Yellow
        #
        # For example:
        #   self.edges[GR] = RY
        # means that the Red-Yellow edge piece is currently in the
        # Green-Red edge position.
        #
        # In the solved state, every edge is in its corresponding position.

        self.edges = (GR, RB, BG, GY, RY, BY)

        # ------------------------------------------------------------
        # EDGE ORIENTATIONS
        # ------------------------------------------------------------
        # Each edge position has an ordered pair of sides:
        #
        #   GR = G | R
        #   RB = R | B
        #   BG = B | G
        #   GY = G | Y
        #   RY = R | Y
        #   BY = B | Y
        #
        # Each edge piece uses the same color ordering.
        #
        # edge_orientations[position] gives the orientation of the edge
        # currently occupying that position.
        #
        #   0 = piece's first color faces the position's first side
        #   1 = piece's first color faces the position's second side
        #
        # In other words, orientation 1 is the reverse of orientation 0.
        #
        # In the solved state, all edges have orientation 0.

        self.edge_orientations = (0, 0, 0, 0, 0, 0)


        # ------------------------------------------------------------
        # CENTER STATES
        # ------------------------------------------------------------
        # Center constants
        # A center is identified by the color that it does NOT contain.
        #
        # G = center containing Red, Blue, Yellow
        # R = center containing Green, Blue, Yellow
        # B = center containing Green, Red, Yellow
        # Y = center containing Green, Red, Blue (top center)
        #         
        # A Pyraminx center has three possible orientations:
        #   0 = solved
        #   1 = rotated clockwise
        #   2 = rotated counterclockwise
        #
        # In the solved state, all centers have orientation 0.
        
        self.centers = (0, 0, 0, 0)
        
        # ------------------------------------------------------------
        # MOVES
        # ------------------------------------------------------------
        # The Pyraminx has 8 non-tip moves:
        #
        #   U   = Upper layer clockwise
        #   U'  = Upper layer counterclockwise
        #
        #   L   = Left layer clockwise
        #   L'  = Left layer counterclockwise
        #
        #   R   = Right layer clockwise
        #   R'  = Right layer counterclockwise
        #
        #   B   = Back layer clockwise
        #   B'  = Back layer counterclockwise
        #
        # Clockwise/counterclockwise is defined while looking directly
        # at the corresponding vertex.
        #
        # Tips are ignored because they do not affect the V and are trivial.

    def move(self, move):
        if move not in MOVES:
            raise ValueError(f"Invalid move: {move}")
    
        if move == "U":
            return self._U()
        elif move == "U'":
            return self._U_prime()
        elif move == "L":
            return self._L()
        elif move == "L'":
            return self._L_prime()
        elif move == "R":
            return self._R()
        elif move == "R'":
            return self._R_prime()
        elif move == "B":
            return self._B()
        elif move == "B'":
            return self._B_prime()
    

    def _cycle_edges(self, a, b, c, flips=()):
        edges = list(self.edges)
        orientations = list(self.edge_orientations)

        # Cycle edge pieces: a -> b -> c -> a
        edges[b] = self.edges[a]
        edges[c] = self.edges[b]
        edges[a] = self.edges[c]

        # The orientations travel with their corresponding edge pieces
        orientations[b] = self.edge_orientations[a]
        orientations[c] = self.edge_orientations[b]
        orientations[a] = self.edge_orientations[c]

        # Reverse orientation where required
        for position in flips:
            orientations[position] ^= 1

        self.edges = tuple(edges)
        self.edge_orientations = tuple(orientations)
    
    def _rotate_center(self, face, clockwise):
        centers = list(self.centers)

        if clockwise:
            centers[face] = (centers[face] + 1) % 3
        else:
            centers[face] = (centers[face] - 1) % 3

        self.centers = tuple(centers)
    
    def _U(self):
        self._cycle_edges(GR, RB, BG, flips=())
        self._rotate_center(Y, True)

    def _U_prime(self):
        self._cycle_edges(GR, BG, RB, flips=())
        self._rotate_center(Y, False)


    def _L(self):
        self._cycle_edges(GR, GY, RY, flips=(GY, RY))
        self._rotate_center(B, True)

    def _L_prime(self):
        self._cycle_edges(GR, RY, GY, flips=(GR, GY))
        self._rotate_center(B, False)

    def _R(self):
        self._cycle_edges(BG, BY, GY, flips=(GY, BY))
        self._rotate_center(R, False)
    
    def _R_prime(self):
        self._cycle_edges(BG, GY, BY, flips=(BG, BY))
        self._rotate_center(R, True)


    def _B(self):
        self._cycle_edges(RB, RY, BY, flips=(BY, RY))
        self._rotate_center(G, True)

    def _B_prime(self):
        self._cycle_edges(RB, BY, RY, flips=(RB, RY))
        self._rotate_center(G, False)
    
    def print_state(self):
        print("Edges:            ", self.edges)
        print("Edge orientations:", self.edge_orientations)
        print("Centers:          ", self.centers)
    
    def copy(self):
        new_pyraminx = Pyraminx()
        new_pyraminx.edges = self.edges
        new_pyraminx.edge_orientations = self.edge_orientations
        new_pyraminx.centers = self.centers
        return new_pyraminx

    def state(self):
        return (
            self.edges,
            self.edge_orientations,
            self.centers
        )
    def _edge_solved(self, edge):
        return (
            self.edges[edge] == edge
            and self.edge_orientations[edge] == 0
        )
    def _solved_edges_on_face(self, face):
        return sum(
            self._edge_solved(edge)
            for edge in FACE_EDGES[face]
        )
    def is_v_solved(self):
        for face in (G, R, B, Y):

            # Count solved edges belonging to this face
            solved_edges = 0

            for edge in FACE_EDGES[face]:
                if self._edge_solved(edge):
                    solved_edges += 1

            # Check that all three centers belonging to this face are solved
            centers_solved = all(
                self.centers[center] == 0
                for center in FACE_CENTERS[face]
            )

            # A V is a solved layer with at most one edge missing
            if solved_edges >= 2 and centers_solved:
                return True

        return False
    
    def scramble(self, scramble):
        moves = scramble.split()

        for move in moves:
            if move not in MOVES:
                raise ValueError(f"Invalid move: {move}")

            self.move(move)
    def get_face_colors(self):
        faces = {
            "green":  ["green"] * 9,
            "red":    ["red"] * 9,
            "blue":   ["blue"] * 9,
            "yellow": ["yellow"] * 9
        }

        # --------------------------------------------------
        # EDGES
        # --------------------------------------------------

        # The two colors belonging to each edge piece
        edge_colors = {
            GR: ("green", "red"),
            RB: ("red", "blue"),
            BG: ("blue", "green"),
            GY: ("green", "yellow"),
            RY: ("red", "yellow"),
            BY: ("blue", "yellow")
        }

        # The two sticker locations belonging to each edge position
        edge_stickers = {
            GR: [("green", 1), ("red", 1)],
            RB: [("red", 5), ("blue", 5)],
            BG: [("blue", 2), ("green", 2)],
            GY: [("green", 5), ("yellow", 5)],
            RY: [("red", 2), ("yellow", 2)],
            BY: [("blue", 1), ("yellow", 1)]
        }

        for position in range(6):
            # Which edge piece is currently in this position?
            piece = self.edges[position]

            # Is that edge flipped?
            orientation = self.edge_orientations[position]

            colors = edge_colors[piece]

            if orientation == 1:
                colors = (colors[1], colors[0])

            locations = edge_stickers[position]

            # Put the edge's two colors onto the correct face stickers
            for i in range(2):
                face, sticker = locations[i]
                faces[face][sticker] = colors[i]

        # --------------------------------------------------
        # CENTERS + TIPS
        # --------------------------------------------------

        # The three sticker locations belonging to each center
        center_stickers = {
            G: [("red", 8),   ("blue", 7),  ("yellow", 3)],
            R: [("green", 8), ("blue", 3),  ("yellow", 7)],
            B: [("green", 7), ("red", 3),   ("yellow", 8)],
            Y: [("green", 3), ("red", 7),   ("blue", 8)]
        }

        # The three tip stickers belonging to the same four vertices
        tip_stickers = {
            G: [("red", 6),   ("blue", 4),  ("yellow", 0)],
            R: [("green", 6), ("blue", 0),  ("yellow", 4)],
            B: [("green", 4), ("red", 0),   ("yellow", 6)],
            Y: [("green", 0), ("red", 4),   ("blue", 6)]
        }

        for center in range(4):
            center_locations = center_stickers[center]
            tip_locations = tip_stickers[center]

            # In orientation 0, every sticker has the color
            # of the face it currently sits on.
            colors = [
                center_locations[0][0],
                center_locations[1][0],
                center_locations[2][0]
            ]

            orientation = self.centers[center]

            # Rotate the three colors around the center
            if orientation == 1:
                colors = [colors[2], colors[0], colors[1]]

            elif orientation == 2:
                colors = [colors[1], colors[2], colors[0]]

            for i in range(3):
                color = colors[i]

                # Center sticker
                face, sticker = center_locations[i]
                faces[face][sticker] = color

                # Tip sticker rotates with the corresponding center
                face, sticker = tip_locations[i]
                faces[face][sticker] = color

        return faces

def bfs(start, max_depth):
    queue = deque()
    solutions = [[] for _ in range(max_depth + 1)]

    queue.append((start, []))

    # Check for a 0-move solution
    if start.is_v_solved():
        solutions[0].append([])

    while queue:
        current, moves_so_far = queue.popleft()

        if len(moves_so_far) >= max_depth:
            continue

        for move in MOVES:
            # Don't allow consecutive moves on the same axis
            if moves_so_far and moves_so_far[-1][0] == move[0]:
                continue
            next_pyraminx = current.copy()
            next_pyraminx.move(move)

            new_moves = moves_so_far + [move]

            if next_pyraminx.is_v_solved():
                solutions[len(new_moves)].append(new_moves)

            queue.append((next_pyraminx, new_moves))

    return solutions

def main():
    scramble = input("Enter scramble: ")
    max_depth = int(input("Maximum solution length: "))

    p = Pyraminx()
    #print(p.get_face_colors()) testing for mapping color to element
    p.scramble(scramble)

    solutions = bfs(p, max_depth)

    for depth in range(max_depth + 1):
        print(f"\nSolutions of length {depth}:")

        if solutions[depth]:
            for solution in solutions[depth]:
                print(" ".join(solution))
        else:
            print("None")
if __name__ == "__main__":
    main() 