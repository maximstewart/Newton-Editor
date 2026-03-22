from .libs.tree_sitter_language_pack import \
    init, download, get_language, get_parser, available_languages, process, ProcessConfig

# Optional: Pre-download specific languages for offline use
#init(["python", "javascript", "rust"])

# Get a language (auto-downloads if not cached)
language = get_language("python")

# Get a pre-configured parser (auto-downloads if needed)
parser = get_parser("python")
tree = parser.parse(b"def hello(): pass")
print(tree.root_node)

# List all available languages
for lang in available_languages():
    print(lang)


# Extract file intelligence (auto-downloads language if needed)
result = process(
    "def hello(): pass",
    ProcessConfig( language = "python")
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
