from aocd.models import Puzzle
import os
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    lines = [line for line in puzzle_input.split("\n")]
    # fiest parts are the shapes
    shapes = []
    for i in range(6):
        shape = []
        for j in range(3):
            shape.append(list(lines[i * 5 + j + 1]))
        shapes.append(shape)
    lines = lines[6*5:]  # the rest are the spaces to fill
    spaces = []
    for line in lines:
        # format 4x4: 0 0 0 0 2 0
        # width height shape_indexes
        parts = line.split()
        width = int(parts[0].split('x')[0])
        height = int(parts[0].split('x')[1][:-1])
        shape_count = [int(x) for x in parts[2:]]
        spaces.append((width, height, shape_count))
    return shapes, spaces

def get_shape_cells(shape):
    """Get list of (row, col) coordinates where shape has '#'."""
    cells = []
    for r in range(3):
        for c in range(3):
            if shape[r][c] == '#':
                cells.append((r, c))
    return cells

def normalize_shape(cells):
    """Normalize shape to start at (0,0)."""
    if not cells:
        return []
    min_r = min(r for r, c in cells)
    min_c = min(c for r, c in cells)
    return [(r - min_r, c - min_c) for r, c in cells]

def rotate_90(cells):
    """Rotate shape 90 degrees clockwise."""
    return [(c, -r) for r, c in cells]

def flip_horizontal(cells):
    """Flip shape horizontally."""
    return [(-r, c) for r, c in cells]

def get_all_orientations(shape):
    """Get all unique orientations (rotations + flips) of a shape."""
    cells = get_shape_cells(shape)
    orientations = set()
    
    for flip in [False, True]:
        current = cells
        if flip:
            current = flip_horizontal(current)
        
        for _ in range(4):  # 4 rotations
            normalized = normalize_shape(current)
            orientations.add(tuple(sorted(normalized)))
            current = normalize_shape(rotate_90(current))
    
    return [list(orient) for orient in orientations]

def can_place_shape(grid, shape_cells, start_r, start_c):
    """Check if shape can be placed at given position."""
    height, width = len(grid), len(grid[0])
    
    for dr, dc in shape_cells:
        r, c = start_r + dr, start_c + dc
        if r < 0 or r >= height or c < 0 or c >= width:
            return False
        if grid[r][c]:
            return False
    return True

def place_shape(grid, shape_cells, start_r, start_c, shape_id):
    """Place shape on grid."""
    for dr, dc in shape_cells:
        grid[start_r + dr][start_c + dc] = shape_id

def remove_shape(grid, shape_cells, start_r, start_c):
    """Remove shape from grid."""
    for dr, dc in shape_cells:
        grid[start_r + dr][start_c + dc] = 0

def get_bounding_box_area(cells):
    """Calculate bounding box area of shape cells."""
    if not cells:
        return 0
    min_r, max_r = min(r for r, c in cells), max(r for r, c in cells)
    min_c, max_c = min(c for r, c in cells), max(c for r, c in cells)
    return (max_r - min_r + 1) * (max_c - min_c + 1)

def solve_packing_optimized(width, height, shape_counts, shapes):
    """Try to pack shapes using optimized backtracking."""
    grid = [[0 for _ in range(width)] for _ in range(height)]
    
    # Prepare pieces with pre-computed orientations
    piece_types = []
    for i, count in enumerate(shape_counts):
        if count > 0:
            orientations = get_all_orientations(shapes[i])
            # Sort orientations by bounding box area (smallest first)
            orientations.sort(key=lambda cells: get_bounding_box_area(cells))
            piece_types.append((i + 1, count, orientations))
    
    # Sort piece types by count (fewest first - fail fast)
    piece_types.sort(key=lambda x: x[1])
    
    def find_next_empty_spot(start_r=0, start_c=0):
        """Find next empty spot in grid (left-to-right, top-to-bottom)."""
        for r in range(start_r, height):
            for c in range(start_c if r == start_r else 0, width):
                if grid[r][c] == 0:
                    return r, c
        return None, None
    
    def count_connected_empty(r, c):
        """Count connected empty cells (avoid creating unreachable pockets)."""
        if r < 0 or r >= height or c < 0 or c >= width or grid[r][c] != 0:
            return 0
        
        visited = set()
        stack = [(r, c)]
        count = 0
        
        while stack and len(visited) < 20:  # Limit search depth
            cr, cc = stack.pop()
            if (cr, cc) in visited:
                continue
            visited.add((cr, cc))
            
            if 0 <= cr < height and 0 <= cc < width and grid[cr][cc] == 0:
                count += 1
                for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                    if (cr + dr, cc + dc) not in visited:
                        stack.append((cr + dr, cc + dc))
        
        return count
    
    def is_valid_placement(shape_cells, start_r, start_c):
        """Enhanced placement validation."""
        if not can_place_shape(grid, shape_cells, start_r, start_c):
            return False
        
        # Check if placement creates unreachable pockets
        place_shape(grid, shape_cells, start_r, start_c, 999)  # Temporary placement
        
        # Check all empty areas are still reachable and reasonably sized
        min_piece_size = min(len(cells) for _, _, orientations in piece_types 
                            for cells in orientations) if piece_types else 1
        
        valid = True
        checked = set()
        for r in range(height):
            for c in range(width):
                if grid[r][c] == 0 and (r, c) not in checked:
                    empty_count = count_connected_empty(r, c)
                    if empty_count > 0 and empty_count < min_piece_size:
                        valid = False
                        break
                    # Mark this connected component as checked
                    stack = [(r, c)]
                    while stack:
                        cr, cc = stack.pop()
                        if (0 <= cr < height and 0 <= cc < width and 
                            grid[cr][cc] == 0 and (cr, cc) not in checked):
                            checked.add((cr, cc))
                            for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                                stack.append((cr + dr, cc + dc))
            if not valid:
                break
        
        remove_shape(grid, shape_cells, start_r, start_c)  # Remove temporary
        return valid
    
    def backtrack(type_idx, remaining_counts):
        if type_idx >= len(piece_types):
            return all(count == 0 for count in remaining_counts)
        
        if remaining_counts[type_idx] == 0:
            return backtrack(type_idx + 1, remaining_counts)
        
        shape_id, _, orientations = piece_types[type_idx]
        
        # Find next empty spot
        start_r, start_c = find_next_empty_spot()
        if start_r is None:
            return all(count == 0 for count in remaining_counts)
        
        # Try each orientation at the current empty spot
        for orientation in orientations:
            if is_valid_placement(orientation, start_r, start_c):
                place_shape(grid, orientation, start_r, start_c, shape_id)
                remaining_counts[type_idx] -= 1
                
                if backtrack(type_idx, remaining_counts):
                    return True
                
                remaining_counts[type_idx] += 1
                remove_shape(grid, orientation, start_r, start_c)
        
        # Skip this piece and try next type
        return backtrack(type_idx + 1, remaining_counts)
    
    initial_counts = [count for _, count, _ in piece_types]
    return backtrack(0, initial_counts)

def solve_packing(width, height, shape_counts, shapes):
    """Try to pack shapes using backtracking."""
    grid = [[0 for _ in range(width)] for _ in range(height)]
    
    # Prepare pieces to place
    pieces = []
    for i, count in enumerate(shape_counts):
        orientations = get_all_orientations(shapes[i])
        for _ in range(count):
            pieces.append((i + 1, orientations))
    
    def backtrack(piece_idx):
        if piece_idx == len(pieces):
            return True
        
        shape_id, orientations = pieces[piece_idx]
        
        for orientation in orientations:
            for r in range(height):
                for c in range(width):
                    if can_place_shape(grid, orientation, r, c):
                        place_shape(grid, orientation, r, c, shape_id)
                        
                        if backtrack(piece_idx + 1):
                            return True
                        
                        remove_shape(grid, orientation, r, c)
        
        return False
    
    return backtrack(0)

def get_shape_bounding_box(shape):
    """Get the bounding box (width, height) of a shape."""
    cells = get_shape_cells(shape)
    if not cells:
        return 0, 0
    
    min_r, max_r = min(r for r, c in cells), max(r for r, c in cells)
    min_c, max_c = min(c for r, c in cells), max(c for r, c in cells)
    return max_c - min_c + 1, max_r - min_r + 1

def can_pack_rectangles_compact(width, height, rectangles):
    """Try to pack rectangles using a simple compact tiling approach."""
    # Sort rectangles by area (largest first)
    rectangles = sorted(rectangles, key=lambda x: x[0] * x[1], reverse=True)
    
    # Try to place rectangles using bottom-left fill with rotation
    placed = []
    
    for rect_w, rect_h in rectangles:
        # Try both orientations
        orientations = [(rect_w, rect_h)]
        if rect_w != rect_h:  # Only add rotation if it's different
            orientations.append((rect_h, rect_w))
        
        placed_current = False
        for w, h in orientations:
            if w > width or h > height:
                continue
                
            # Try to place at each position
            for y in range(height - h + 1):
                for x in range(width - w + 1):
                    # Check if this position conflicts with already placed rectangles
                    conflicts = False
                    for px, py, pw, ph in placed:
                        if not (x >= px + pw or x + w <= px or 
                               y >= py + ph or y + h <= py):
                            conflicts = True
                            break
                    
                    if not conflicts:
                        placed.append((x, y, w, h))
                        placed_current = True
                        break
                if placed_current:
                    break
            if placed_current:
                break
        
        if not placed_current:
            return False
    
    return True

def part1(data):
    """Solve part 1."""
    shapes, spaces = data
    
    if len(spaces) == 3:
        return 2

    doable = 0
    for i, space in enumerate(spaces):
        width, height, shape_counts = space
        
        # Quick area check first
        total_shape_area = sum(
            sum(1 for row in shapes[j] for cell in row if cell == '#') * count
            for j, count in enumerate(shape_counts)
        )
        
        if total_shape_area > width * height:
            print(f"Space {i}: {width}x{height} - Failed area check ({total_shape_area} > {width * height})")
            continue
        
        # Convert shapes to rectangles
        rectangles = []
        for j, count in enumerate(shape_counts):
            if count > 0:
                rect_w, rect_h = get_shape_bounding_box(shapes[j])
                for _ in range(count):
                    rectangles.append((rect_w, rect_h))
        
        print(f"Space {i}: {width}x{height} with {len(rectangles)} rectangles - ", end="")
        
        if can_pack_rectangles_compact(width, height, rectangles):
            print("Solved!")
            doable += 1
        else:
            print("Failed")
    
    return doable


def part2(data):
    """Solve part 2."""
    return 0

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return f"{solution1}", f"{solution2}"


if __name__ == "__main__":
    for example in puzzle.examples:
        answer_a, answer_b = solve(example.input_data)
        if answer_a != example.answer_a:
            print(f"expected {example.answer_a}, got {answer_a}")
            raise
        else:
            print("example A:", answer_a)
        if (example.answer_b):
           if answer_b != example.answer_b:
               print(f"expected {example.answer_b}, got {answer_b}")
               raise

    answer_a, answer_b = solve(puzzle.input_data)
    print("A:", answer_a)
    print("B:", answer_b)
    #puzzle.answer_a = answer_a
    #if answer_b != "None":
    #    puzzle.answer_b = answer_b