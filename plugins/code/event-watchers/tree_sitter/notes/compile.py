from .tree_sitter import Language

Language.build_library(
    "my-languages.so",
    [
        "tree-sitter-python",
        "tree-sitter-javascript",
        "tree-sitter-html",
        "tree-sitter-css",
        "tree-sitter-json",
        "tree-sitter-java",
        "tree-sitter-c",
        "tree-sitter-cpp",
        "tree-sitter-go",
        "tree-sitter-gdscript",
    ],
)
