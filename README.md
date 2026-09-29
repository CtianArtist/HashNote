HashNote

A note-taking app built from the ground up in Python, starting with a hand-written hash map and growing into a linked-notes app in the style of Obsidian.

This is my #100DaysOfCode project. Each day adds one working piece, and every layer is built on the one below it rather than on a library that already does the job.

Why build it this way

Most note apps hide their data structures behind a database. Building each layer myself (storage, indexing, linking, search) is a way to understand the trade-offs that those tools make for you, and to end up with a small app I actually use.

Roadmap

Status is updated as the project progresses.

Phase 1: Core data structures
 Hash map with separate chaining (put, get, delete)
 Automatic resizing based on load factor
 Iteration over keys and values
 Unit tests and simple benchmarks against Python's dict
Phase 2: Notes and storage
 Note model (title, body, created and updated timestamps)
 Save and load notes as Markdown files in a vault folder
 Command-line interface: create, read, edit, delete, list
Phase 3: Linking and search
 [[wiki-link]] parsing between notes
 Backlinks index (which notes link to this one)
 Tags
 Full-text search with an inverted index
Phase 4: Interface
 Desktop or web interface with a note editor
 Graph view of links between notes
Progress log
Day	Work
1	Project set up
License
