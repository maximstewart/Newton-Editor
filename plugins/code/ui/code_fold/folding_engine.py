# Python imports

# Lib imports

# Application imports
from .fold_types import FOLD_NODES



def get_folding_ranges(lang_name: str, ast):
    root       = ast.root_node
    fold_types = FOLD_NODES.get(lang_name, set())
    ranges     = []

    def visit(node):
        if node.type in fold_types:
            start_line = node.start_point[0]
            end_line   = node.end_point[0]

            if end_line > start_line:
                ranges.append({
                    "start_line": start_line,
                    "end_line": end_line,
                    "id": (start_line, end_line, node.type),
                })

        for child in node.children:
            visit(child)

    visit(root)
    return ranges
