#!/bin/bash

# . CONFIG.sh

# set -o xtrace       ## To debug scripts
# set -o errexit      ## To exit on error
# set -o errunset     ## To exit if a variable is referenced but not set
#!/usr/bin/env bash
set -euo pipefail



ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS="$ROOT/.tools"
NODE_DIR="$TOOLS/node"
GRAMMARS_DIR="$ROOT/grammars"
BUILD_DIR="$ROOT/build"
OUTPUT="$ROOT/compiled"
NODE_VERSION="v24.14.1"
NODE_DIST="node-$NODE_VERSION-linux-x64"
NODE_ARCHIVE="$TOOLS/node.tar.xz"
NODE_URL="https://nodejs.org/dist/$NODE_VERSION/$NODE_DIST.tar.xz"
TS_CLI_VERSION="0.22.6"


LANGS=(
    tree-sitter-python
    tree-sitter-javascript
    tree-sitter-html
    tree-sitter-css
    tree-sitter-json
    tree-sitter-java
    tree-sitter-c
    tree-sitter-cpp
    tree-sitter-go
)

REPOS=(
    https://github.com/tree-sitter/tree-sitter-python
    https://github.com/tree-sitter/tree-sitter-javascript
    https://github.com/tree-sitter/tree-sitter-html
    https://github.com/tree-sitter/tree-sitter-css
    https://github.com/tree-sitter/tree-sitter-json
    https://github.com/tree-sitter/tree-sitter-java
    https://github.com/tree-sitter/tree-sitter-c
    https://github.com/tree-sitter/tree-sitter-cpp
    https://github.com/tree-sitter/tree-sitter-go
)

mkdir -p "$TOOLS" "$GRAMMARS_DIR" "$BUILD_DIR" "$OUTPUT"

ensure_node() {
    if [ -x "$NODE_DIR/bin/node" ]; then
        echo "==> Using cached Node.js"
        return
    fi

    echo "==> Downloading Node.js $NODE_VERSION"
    wget -O "$NODE_ARCHIVE" "$NODE_URL"

    echo "==> Extracting Node.js"
    mkdir -p "$NODE_DIR"
    tar -xf "$NODE_ARCHIVE" -C "$NODE_DIR" --strip-components=1
    rm "$NODE_ARCHIVE"

    echo "==> Node installed at $NODE_DIR"
}

ensure_tree_sitter() {
    export PATH="$NODE_DIR/bin:$PATH"
    TS="$TOOLS/node_modules/.bin/tree-sitter"

    if [ -x "$TS" ]; then
        echo "==> Using cached tree-sitter-cli"
        return
    fi

    echo "==> Installing tree-sitter-cli"
    cd "$TOOLS"
    npm init -y >/dev/null 2>&1 || true
    npm install tree-sitter-cli@$TS_CLI_VERSION
}

sync_grammars() {
    echo "==> Syncing grammars"

    for i in "${!LANGS[@]}"; do
        NAME="${LANGS[$i]}"
        REPO="${REPOS[$i]}"
        TARGET="$GRAMMARS_DIR/$NAME"

        if [ -d "$TARGET/.git" ]; then
            echo "Updating $NAME"
            git -C "$TARGET" pull --depth 1
        else
            echo "Cloning $NAME"
            git clone --depth 1 "$REPO" "$TARGET"
        fi
    done
}

build_lib() {
    echo "==> Building Tree-sitter library"

    mkdir -p "$OUTPUT"

    PARSER_SRC=()
    INCLUDE_PATHS=()

    for GRAMMAR in "${LANGS[@]/#/$GRAMMARS_DIR/}"; do
        echo "==> Processing grammar $GRAMMAR"

        PARSER_SRC+=("$GRAMMAR/src/parser.c")

        if [[ -f "$GRAMMAR/src/scanner.c" ]]; then
            PARSER_SRC+=("$GRAMMAR/src/scanner.c")
        fi

        INCLUDE_PATHS+=("-I$GRAMMAR/src")
    done

    gcc -shared -o "$OUTPUT/languages.so" "${PARSER_SRC[@]}" "${INCLUDE_PATHS[@]}" -fPIC

    echo "==> Output: $OUTPUT/languages.so"
}

main() {
    ensure_node
    ensure_tree_sitter
    sync_grammars
    build_lib
}

main "$@"
