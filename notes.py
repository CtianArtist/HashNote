from hashmap import HashMap
#the above imports the hashmap class from hashmap.py

def main():
    notes = HashMap()
    #The main logic. While it's running, it will ask the user for a command. The user can create a new note, read an existing note, list all notes, delete a note, or quit the program.
    while True:
        cmd = input("\n[new / read / list / delete / quit] > ").strip().lower()

        if cmd == "new":
            title = input("Title: ").strip()
            body = input("Note: ")
            notes.put(title, body)
            print(f"Saved '{title}'.")

        elif cmd == "read":
            title = input("Title: ").strip()
            body = notes.get(title)
            print(body if body is not None else "No note with that title.")

        elif cmd == "list":
            pairs = notes.get_keys_and_values()
            if pairs.length() == 0:
                print("No notes yet.")
            for i in range(pairs.length()):
                title, _ = pairs.get_at_index(i)
                print(f"- {title}")

        elif cmd == "delete":
            title = input("Title: ").strip()
            notes.remove(title)
            print(f"Deleted '{title}' (if it existed).")

        elif cmd == "quit":
            break


if __name__ == "__main__":
    main()

#currently this only saves in memory but it is a proof of concept for having it all work with the hashmap itself    