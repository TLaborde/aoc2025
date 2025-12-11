from aocd.models import Puzzle
import os
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split("\n")]


def part1(data):
    """Solve part 1."""
    # create a graph from the input data
    # each line represents a node and its connections
    graph = {}
    for line in data:
        parts = line.split(" ")
        node = parts[0][0:-1]
        connections = parts[1:]
        graph[node] = connections
    # find all path from "you" to "out"
    def dfs(node, visited):
        if node == "out":
            return 1
        visited.add(node)
        total_paths = 0
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                total_paths += dfs(neighbor, visited)
        visited.remove(node)
        return total_paths
    total_paths = dfs("you", set())
    return total_paths if total_paths else 0
    return 0


def part2(data):
    """Solve part 2."""
    graph = {}
    for line in data:
        parts = line.split(" ")
        node = parts[0][0:-1]
        connections = parts[1:]
        graph[node] = connections

    # invert the graph
    inverted_graph = {}
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if neighbor not in inverted_graph:
                inverted_graph[neighbor] = []
            inverted_graph[neighbor].append(node)



    def dfs(graph, start, target, avoid_set):
        """Count paths from start to target using iterative DFS with backtracking."""
        if start == target:
            return 1
        
        stack = [(start, {start}, [])]  # (node, visited, path)
        total_paths = 0
        
        while stack:
            node, visited, path = stack.pop()
            
            if node == target:
                total_paths += 1
                continue
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited and neighbor not in avoid_set:
                    new_visited = visited.copy()
                    new_visited.add(neighbor)
                    stack.append((neighbor, new_visited, path + [neighbor]))
        
        return total_paths
    
    # function to get all the nodes reachable from a start node avoiding a specific node
    def reachable_nodes(graph, start, avoid):
        stack = [start]
        reachable = set()
        
        while stack:
            node = stack.pop()
            if node in reachable or node == avoid:
                continue
            reachable.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in reachable and neighbor != avoid:
                    stack.append(neighbor)
        
        return reachable

    def reduce_graph(graph, inverted_graph, start, end, avoid):
        reachable_from_start = reachable_nodes(graph, start, avoid)
        reachable_from_end = reachable_nodes(inverted_graph, end, avoid)
        subgraph_nodes = reachable_from_start.intersection(reachable_from_end)
        reduced_graph = {node: [n for n in graph[node] if n in subgraph_nodes] for node in subgraph_nodes if node in graph}
        inverted_reduced_graph = {node: [n for n in inverted_graph[node] if n in subgraph_nodes] for node in subgraph_nodes if node in inverted_graph}
        return reduced_graph, inverted_reduced_graph

    total_paths_svr_to_fft = dfs(inverted_graph, "fft", "svr", set('dac'))
    print("Paths from svr to fft avoiding dac:", total_paths_svr_to_fft)
    

    reduced_graph, inverted_reduced_graph = reduce_graph(graph, inverted_graph, "fft", "dac", "svr")
    total_paths_fft_to_dac = dfs(inverted_reduced_graph, "dac", "fft",  set('svr'))
    print("Paths from fft to dac in reduced graph avoiding svr:", total_paths_fft_to_dac)

    if "fft" not in reachable_nodes(graph, "dac", "out"):
        print("fft not reachable from dac avoiding out")
    else:
        reduced_graph, inverted_reduced_graph = reduce_graph(graph, inverted_graph, "svr", "fft", "dac")
        total_paths_svr_to_dac = dfs(reduced_graph, "svr", "fft", set('dac'))
        print("Paths from svr to fft in reduced graph avoiding dac:", total_paths_svr_to_dac)

        reduced_graph, inverted_reduced_graph = reduce_graph(graph, inverted_graph, "dac", "fft", "out")
        total_paths_dac_to_fft = dfs(inverted_reduced_graph, "fft","dac",  set('out'))
        print("Paths from dac to fft in reduced graph avoiding out:", total_paths_dac_to_fft)

        reduced_graph, inverted_reduced_graph = reduce_graph(graph, inverted_graph, "fft", "out", "dac")
        total_paths_fft_to_out = dfs(inverted_reduced_graph, "out", "fft", set('dac'))
        print("Paths from fft to out in reduced graph avoiding dac:", total_paths_fft_to_out)

    reduced_graph, inverted_reduced_graph = reduce_graph(graph, inverted_graph, "dac", "out", "fft")
    total_paths_dac_to_out = dfs(reduced_graph, "dac", "out", set('fft'))
    print("Paths from dac to out in reduced graph avoiding fft:", total_paths_dac_to_out)
    return total_paths_svr_to_fft * total_paths_fft_to_dac * total_paths_dac_to_out #+ total_paths_svr_to_dac * total_paths_dac_to_fft * total_paths_fft_to_out
    return 0



def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return f"{solution1}", f"{solution2}"


if __name__ == "__main__":
    #for example in puzzle.examples:
    #    answer_a, answer_b = solve(example.input_data)
    #    if answer_a != '5':
    #        print(f"expected {example.answer_a}, got {answer_a}")
    #        raise
        #if (example.answer_b):
        #   if answer_b != '2':
        #       print(f"expected {example.answer_b}, got {answer_b}")
        #       raise
    input_data = '''
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
'''
    
    answer_a, answer_b = solve(input_data)
    answer_a, answer_b = solve(puzzle.input_data)
    print("B:", answer_b)
    #puzzle.answer_a = answer_a
    #if answer_b != "None":
    #    puzzle.answer_b = answer_b