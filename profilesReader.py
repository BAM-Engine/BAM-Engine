################
# Read Profiles
##############
def readProfiles(profileEntry):
    print(f"Searching for: {profileEntry}")
    i = 0

    with open("profiles.txt", "r") as f:
        for line in f:
            print(line)
            #currentLine = line.rstrip()

            # Filter out comments
            # Prefaced with "- "
            currentArray = list(line)
            print(currentArray)
            if currentArray[0] == "-" or currentArray[0] == "\n" or currentArray[0] == ";":
                print("""Skipping from:
                    - Comment (-)
                    - Blankline (\\n)
                    - Blanked Code (;)
                    """)
                continue
            else:
                print(f"Running Line: {line}")
                focusLine = line.split()
                print(f"Focused Line: {focusLine}")
                if focusLine[0] == profileEntry:
                    print("Line FOUND!")
                    break
                else:
                    print(f"{focusLine[0]} != {profileEntry}")
                    continue


def writeProfiles(profileEntry, replaced):
    with open("profiles.txt", "w") as _f:
        pass

if __name__ == "__main__":
    readProfiles("controlPath") # Add more
