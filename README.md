Git From Scratch (Python)


A learning-focused implementation of core Git internals written in Python.
This project explores how Git stores data, represents objects, and creates commits by rebuilding essential mechanisms from scratch.

Note: This is not a full Git replacement. The project is intended for understanding Git internals.

Overview

This implementation recreates key parts of Git’s internal design:

Content-addressable storage using SHA-1

Blob, tree, and commit object formats

zlib-compressed object storage under .git/objects

Minimal repository structure and object inspection

Supported Commands
Initialize a repository
python main.py init

Create and store a blob object
python main.py hash-object -w <file>

Display the contents of an object
python main.py cat-file -p <object_sha>

Create a tree object
python main.py write-tree

List contents of a tree object
python main.py ls-tree <tree_sha>
python main.py ls-tree --name-only <tree_sha>

Create a commit object
python main.py commit-tree <tree_sha> -m "commit message"

Clone (Work in Progress)
python main.py clone <repo_path> [destination]

Quick Start Example Workflow

Follow these steps to see how the project works:

Initialize a repository

python main.py init


Creates .git directory structure.

Create and store blob objects

python main.py hash-object -w file1.txt
python main.py hash-object -w file2.txt


Generates SHA-1 hashes and stores the file contents as blobs.

Create a tree object

python main.py write-tree


Generates a tree object representing the current directory.

Create a commit

python main.py commit-tree <tree_sha> -m "Initial commit"


Creates a commit object pointing to the tree.

Inspect objects

python main.py cat-file -p <object_sha>
python main.py ls-tree <tree_sha>


Check contents of blobs, trees, and commits.

Project Scope
Implemented

Blob object creation and storage

Tree object generation with recursive directory traversal

Commit object creation with optional parent linking

Object inspection and tree listing

Git-compatible object hashing and zlib compression

Not implemented / Work in progress

Clone 


Key Learning Outcomes

Git object model (blob, tree, commit)

Content hashing and immutability

Binary object encoding

zlib compression

Filesystem-based version control design

Low-level understanding of Git internals

Technologies Used

Python 3

hashlib

zlib

pathlib





Project Structure

main.py

.git/

objects/

refs/

HEAD

Author

Nesara Rahal
