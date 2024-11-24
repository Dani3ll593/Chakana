def generate_index(structure):
    if not structure:
        return {f"Block {i}": f"Block {i}" for i in range(len(structure))}
    return structure