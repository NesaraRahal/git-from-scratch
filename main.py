import sys
import os
import zlib
import hashlib



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
        if len(sys.argv) > 3 and sys.argv[2] == "--name-only":
            print(sys.argv[3])
            tree_hash = sys.argv[3]
            folder_name = tree_hash[:2]
            file_name = tree_hash[2:]

            tree_path = os.path.join(".git", "objects", folder_name, file_name)

            with open(tree_path, "rb") as tree:
                data = tree.read()

            decompressed_tree = zlib.decompress(data)
            

            tree_null_byte = decompressed_tree.find(b'\x00')
            actual_tree_content = decompressed_tree[tree_null_byte+1:]

            position = 0

            while(position < len(actual_tree_content)):

                #File type
                space_index = actual_tree_content.find(b' ', position)
                file_type = actual_tree_content[position:space_index].decode()
 
                # File Name
                null_index = actual_tree_content.find(b'\x00', space_index)
                file_name = actual_tree_content[space_index+1:null_index].decode()

                #Sha1 Hash
                sha1_start = null_index + 1 
                sha1_end = sha1_start + 20

                sha_binary = actual_tree_content[sha1_start:sha1_end]
                sha_hex = sha_binary.hex()

                print(sha_hex)
                

            print(actual_tree_content)
        else:
            raise RuntimeError(f"Unknown command #--name-only")

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
