

def get_cell_adjacency(cell, shape):
    r, c = cell
    num_rows, num_cols = shape

    adjacency = dict()
    if r > 0:
        adjacency['t'] = (r - 1, c)
    if r < num_rows - 1:
        adjacency['b'] = (r + 1, c)
    if c > 0:
        adjacency['l'] = (r, c - 1)
    if c < num_cols - 1:
        adjacency['r'] = (r, c + 1)

    return adjacency


inverse_direction_map = {
    'r': 'l',
    'l': 'r',
    't': 'b',
    'b': 't'
}


def has_valid_connection(module1, module2, direction):
    inverse_direction = inverse_direction_map[direction]
    m1_connections = set(module1["connections"][direction])
    m2_connections = set(module2["connections"][inverse_direction])
    return bool(m1_connections.intersection(m2_connections))

