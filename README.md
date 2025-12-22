

# Git From Scratch (Python)

A deep-dive, learning-focused implementation of core Git internals. This project explores how Git manages data integrity, represents file hierarchies, and creates immutable history by rebuilding essential mechanisms from the ground up.

> **Note:** This is a technical exploration of Git's architecture, not a full production replacement. It is designed to showcase the beauty of content-addressable storage.

---

## 🏗️ The Git Object Model

This project implements the core "Plumbing" of Git. At its heart, Git is a simple key-value data store where the key is the SHA-1 hash of the content.

### How it works:

1. **Blobs**: Store the raw file content (data).
2. **Trees**: Act like directories, mapping filenames to Blobs or other Trees.
3. **Commits**: Store snapshots (Trees) along with metadata like author, timestamp, and parent pointers.

---

## 🚀 Supported Commands

### Core Plumbing

| Command | Description |
| --- | --- |
| `python main.py init` | Initializes the `.git` directory structure. |
| `python main.py hash-object -w <file>` | Hashes a file and stores it as a compressed blob. |
| `python main.py cat-file -p <sha>` | Decompresses and prints the contents of a stored object. |

### Tree & History Management

| Command | Description |
| --- | --- |
| `python main.py write-tree` | Recursively captures the current directory as a Tree object. |
| `python main.py ls-tree <sha>` | Lists the contents of a tree (supports `--name-only`). |
| `python main.py commit-tree <sha>` | Creates a commit object pointing to a tree with author metadata. |

---

## 🛠️ Quick Start Workflow

Follow these steps to build your first manual commit:

1. **Initialize the repository**
```bash
python main.py init

```


2. **Hash and store content**
```bash
python main.py hash-object -w example.txt

```


3. **Snapshot the directory**
```bash
python main.py write-tree
# Outputs a <tree_sha>

```


4. **Create a commit**
```bash
python main.py commit-tree <tree_sha> -m "Initial commit"

```



---

## 🧠 Technical Highlights & Learning Outcomes

* **Content-Addressable Storage**: Implemented Git’s unique hashing strategy where identical content results in the same SHA-1, preventing data duplication.
* **Recursive Merkle Trees**: Developed a recursive directory walker to generate Tree objects, effectively replicating a filesystem hierarchy in a flat database.
* **Binary Data Engineering**: Handled Git’s specific binary format, including null-byte delimiters (`\x00`) and 20-byte binary SHA-1 representations.
* **Data Efficiency**: Implemented `zlib` compression to mirror Git’s disk-space management.
* **Object Sharding**: Implemented the `2/38` character folder split (e.g., `.git/objects/a1/b2c3...`) to optimize filesystem performance for large object counts.

---

## 🚧 Roadmap

* [x] Recursive Tree Generation
* [x] SHA-1 Integrity Hashing
* [x] Commit History Linking
* [ ] **In Progress:** Git Clone 

---

## 💻 Technologies Used

* **Python 3**: Core logic.
* **Hashlib**: SHA-1 generation.
* **Zlib**: Object compression.
* **Pathlib**: Modern filesystem path management.

**Author:** Nesara Rahal

