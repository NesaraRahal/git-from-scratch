import re
import sys
import os
import time
import zlib
import hashlib
from pathlib import Path

#For git clone
import requests




def createTree(path):

    entries = []

    for entry in path.iterdir():
        if entry.is_file():
            sha1Hash = hashObj(entry)
            entries.append(("100644", entry.name, sha1Hash))

        elif entry.is_dir():
            if(entry.name == ".git"):
                continue
            
            subtree_sha1 = createTree(entry)
            entries.append(("40000", entry.name, subtree_sha1))            
            #entries.append(createTree(entry))
            #Tree object 
    tree_content = b""
    for mode, name, sha1 in entries:
        tree_content += f"{mode} {name}\0".encode()
        tree_content += bytes.fromhex(sha1)        

    header = f"tree {len(tree_content)}\x00".encode()
    tree_obj = header + tree_content
    sha1_tree_obj = hashlib.sha1(tree_obj).hexdigest()

    folder_name = sha1_tree_obj[0:2]
    file_name = sha1_tree_obj[2:]

    path = os.path.join(".git", "objects", folder_name)
    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, file_name)
    with open(file_path, "wb") as hash_save_tree:
        compressed = zlib.compress(tree_obj)
        hash_save_tree.write(compressed)

    
    return sha1_tree_obj


def hashObj(entry):
    with open(entry, "rb") as f:
            content = f.read()
            header = f"blob {len(content)}\x00".encode()
            before_hash = header + content
            sha1_hash = hashlib.sha1(before_hash).hexdigest()
            #print(sha1_hash)

            folder_name = sha1_hash[0:2]
            file_name = sha1_hash[2:]
            path = os.path.join(".git", "objects", folder_name)
            os.makedirs(path, exist_ok=True)

            file_path = os.path.join(path, file_name)
            with open(file_path, "wb") as hash_save:
                compressed = zlib.compress(before_hash)
                hash_save.write(compressed)

            return sha1_hash
    
def commitTree(author_name, author_email, timestamp, timezone, tree_sha1, parent_header, command_length, commit_msg ):
    if command_length >= 3:
        tree_header = f"tree {tree_sha1}"

        line = [tree_header]

        author_details = f"{author_name} <{author_email}> {timestamp} {timezone}"

        if parent_header != None:
            parent_header = f"parent {parent_header}"
            line.append(parent_header)

        line.append(f"author {author_details}")
        line.append(f"committer {author_details}")
        line.append("")

        if commit_msg:
            line.append(commit_msg)

        commit_content = "\n".join(line).encode()
        commit_obj_header = f"commit {len(commit_content)}\x00".encode()
        commit_content = commit_obj_header + commit_content

        commit_content_sha1 =  hashlib.sha1(commit_content).hexdigest()
        print(commit_content_sha1)

        folder_name = commit_content_sha1[0:2]
        file_name = commit_content_sha1[2:]
        path = os.path.join(".git", "objects", folder_name)
        os.makedirs(path, exist_ok=True)

        file_path = os.path.join(path, file_name)
        with open(file_path, "wb") as commit_save:
            compressed = zlib.compress(commit_content)
            commit_save.write(compressed)



def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # Uncomment this block to pass the first stage
    
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif command == "cat-file":
        if sys.argv[2] == "-p":
            hash = sys.argv[3];
            #print(hash)
            folder_name = hash[:2]
            file_name  = hash[2:]
            obj_name = folder_name + file_name;
            #print(obj_name)

            path = os.path.join(".git", "objects", folder_name, file_name)

            #decompress the file in this path and displays it to the user using zlib
            with open(path, "rb")  as compressed:
                data = compressed.read();

            decompressed_content = zlib.decompress(data)
            #print(decompressed_content)      

            #Finding the null byte
            null_byte = decompressed_content.find(b'\x00')
            actual_content = decompressed_content[null_byte+1:]
            print(actual_content.decode("utf-8", errors="replace"), end="")
    elif command == "hash-object":   
        file = sys.argv[3]
        with open(file, "rb") as f:
            content = f.read()
            header = f"blob {len(content)}\x00".encode()
            before_hash = header + content
            sha1_hash = hashlib.sha1(before_hash).hexdigest()
            print(sha1_hash)
        if sys.argv[2] == "-w":
            #save the hash object in the .git/objects folder
            folder_name = sha1_hash[0:2]
            file_name = sha1_hash[2:]
            path = os.path.join(".git", "objects", folder_name)
            os.makedirs(path, exist_ok=True)

            file_path = os.path.join(path, file_name)
            with open(file_path, "wb") as hash_save:
                compressed = zlib.compress(before_hash)
                hash_save.write(compressed)
    elif command == "ls-tree":
        if len(sys.argv) >= 3: 
            
            if sys.argv[2] == "--name-only":
                tree_hash = sys.argv[3]
            else:
                tree_hash = sys.argv[2]

            folder_name = tree_hash[:2]
            file_name = tree_hash[2:]

            tree_path = os.path.join(".git", "objects", folder_name, file_name)

            with open(tree_path, "rb") as tree:
                data = tree.read()

            decompressed_tree = zlib.decompress(data)            

            tree_null_byte = decompressed_tree.find(b'\x00')
            actual_tree_content = decompressed_tree[tree_null_byte+1:]

            position = 0

            if len(sys.argv)>3 and sys.argv[2] == "--name-only":
            #ls-tree command with --name-only command
                while(position < len(actual_tree_content)):

                    space_index = actual_tree_content.find(b' ', position)
    
                    # File Name
                    null_index = actual_tree_content.find(b'\x00', space_index)
                    file_name = actual_tree_content[space_index+1:null_index].decode()

                    #Sha1 Hash
                    sha1_start = null_index + 1 
                    sha1_end = sha1_start + 20

                    print(file_name)

                    position =  sha1_end 
            
            elif len(sys.argv) == 3 and sys.argv[2] != "--name-only":
                #ls-tree command without --name-only
            
                while(position < len(actual_tree_content)):

                    #File type
                    space_index = actual_tree_content.find(b' ', position)
                    file_type = actual_tree_content[position:space_index].decode()

                    if file_type == "40000":
                        file_type_text = "tree"
                    else:
                        file_type_text = "blob"
    
                    # File Name
                    null_index = actual_tree_content.find(b'\x00', space_index)
                    file_name = actual_tree_content[space_index+1:null_index].decode()
        
                    #Sha1 Hash
                    sha1_start = null_index + 1 
                    sha1_end = sha1_start + 20

                    sha_binary = actual_tree_content[sha1_start:sha1_end]
                    sha_hex = sha_binary.hex()

                    print(f"{file_type} {file_type_text}\t{sha_hex}\t{file_name}")
                    
                    position =  sha1_end 
        else:
            raise RuntimeError(f"Unknown command #--name-only")
    elif command == "write-tree":
        root = Path.cwd()
        sha1_tree_obj = createTree(root)
        print(sha1_tree_obj)
    elif command == "commit-tree":
        if len(sys.argv) > 2 :
               tree_sha1 = sys.argv[2]
               
               author_name = "Rahal"
               author_email = "testemail@gmail.com"
               timestamp = int(time.time())
               timezone = "+0530"  

               if sys.argv[3] == "-p" and sys.argv[4] != None:
                    print(sys.argv[4])
                    parent_header = sys.argv[4]
               else:
                    parent_header = None 

               if sys.argv[5] == "-m" and sys.argv[6] != None or sys.argv[6] != "":
                    commit_msg = sys.argv[6]
                    
               else:
                    commit_msg = None 


               command_length = len(sys.argv)

               commitTree(author_name, author_email, timestamp, timezone, tree_sha1, parent_header, command_length, commit_msg)
    elif command == "clone":

        #Create the directory first
        dir = Path(sys.argv[3]) if len(sys.argv) > 3 else Path.cwd()
        print(dir)

        dir.mkdir(parents=True, exist_ok=True)

        git_dir = dir / ".git" 
        git_objects = dir / ".git" / "objects"
        git_refs = dir / ".git" / "refs"
        git_head_file = dir / ".git" / "HEAD"

        heads_dir = git_refs / "heads"

        git_dir.mkdir(parents=True, exist_ok=True)
        git_objects.mkdir(parents=True, exist_ok=True)
        git_refs.mkdir(parents=True, exist_ok=True)
        heads_dir.mkdir(parents=True, exist_ok=True)

        (heads_dir / "main").write_text("")

        with open(git_head_file, "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")  


        repo_url = "https://github.com/NesaraRahal/git-from-scratch"
        info_refs_url = f"{repo_url}/info/refs?service=git-upload-pack"

        r = requests.get(info_refs_url)

        #Parsing the response so we can extract refs and commite objects
        data = r.content.decode()

        print(data)

        lines = data.split('\n')

        refs = {}

        for line in lines:
            if not line or len(line) < 5:
                continue

            # remove pkt-line length
            payload = line[4:]

            # ignore service line
            if payload.startswith('#'):
                continue

            # remove capabilities (after NULL byte)
            payload = payload.split('\x00', 1)[0]

            if ' ' not in payload:
                continue

            sha, ref = payload.split(' ', 1)
            refs[ref] = sha

            print(refs)



        
    else:
        raise RuntimeError(f"Unknown command #{command}")
    
    

if __name__ == "__main__":
    main()
