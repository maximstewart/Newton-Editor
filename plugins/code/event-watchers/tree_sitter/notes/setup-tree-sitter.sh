#!/bin/bash

# . CONFIG.sh

# set -o xtrace       ## To debug scripts
# set -o errexit      ## To exit on error
# set -o errunset     ## To exit if a variable is referenced but not set




function old_build() {
    touch __init__.py

cat <<'EOF' > compile.py
from tree_sitter import Language

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
        "tree-sitter-go"
        "tree-sitter-gdscript",
    ],
)
EOF

    python compile.py
    cd ..
}

function build() {
    touch __init__.py

cat <<'EOF' > compile.py
from tree_sitter_language_pack import init, download, get_language, get_parser, available_languages
from tree_sitter_language_pack import process, ProcessConfig

# Optional: Pre-download specific languages for offline use
# init(["python", "javascript", "rust"])

# Get a language (auto-downloads if not cached)
language = get_language("python")

# Get a pre-configured parser (auto-downloads if needed)
parser   = get_parser("python")
tree     = parser.parse(b"def hello(): pass")
print(tree.root_node)

# List all available languages
for lang in available_languages():
    print(lang)


# Extract file intelligence (auto-downloads language if needed)
result = process(
    "def hello(): pass",
    ProcessConfig(
        language = "python"
    )
)
print(f"Functions: {len(result['structure'])}")

# Pre-download languages for offline use
download(["python", "javascript"])

# With chunking
result = process(
    source,
    ProcessConfig(
        language       = "python",
        chunk_max_size = 1000,
        comments       = True
    )
)
print(f"Chunks: {len(result['chunks'])}")

EOF

    python compile.py
    cd ..
}

function clone() {
    git clone --depth 1 https://github.com/tree-sitter/tree-sitter-python
    git clone --depth 1 https://github.com/tree-sitter/tree-sitter-javascript
    git clone --depth 1 https://github.com/tree-sitter/tree-sitter-html
    git clone --depth 1 https://github.com/tree-sitter/tree-sitter-css
    git clone --depth 1 https://github.com/tree-sitter/tree-sitter-json
    git clone --depth 1 https://github.com/tree-sitter/tree-sitter-java
    git clone --depth 1 https://github.com/tree-sitter/tree-sitter-c
    git clone --depth 1 https://github.com/tree-sitter/tree-sitter-cpp
    git clone --depth 1 https://github.com/tree-sitter/tree-sitter-go
#    git clone --depth 1 https://github.com/godotengine/tree-sitter-gdscript
}

function setup() {
#    pip install tree-sitter -t .
    pip install tree-sitter-language-pack -t .
#    pip install tree_sitter_languages -t . # Old unmaintained library
}

function main() {
    cd "$(dirname "$0")"
    echo "Working Dir: " $(pwd)

    mkdir -p build
    cd build

#    clone "$@"
    setup "$@"
    build "$@"
}
main "$@";
