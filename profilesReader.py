################
# Read Profiles
##############
def readProfiles(profileEntry):
    """Get the value of a profile"""
    print(f"Searching for: {profileEntry}")

    with open("profiles.txt", "r") as f:
        for line in f:
            print(f"Checking: {line}")
            #currentLine = line.rstrip()

            # Filter out comments
            # Prefaced with "- "
            currentArray = list(line)
            if currentArray[0] == "-" or currentArray[0] == "\n" or currentArray[0] == ";":
                continue
            else:
                focusLine = line.split()
                sub = ":"
                focusLine = focusLine[0].split(sub)
                if focusLine[0] == profileEntry:
                    print("Line FOUND!")
                    print(f"Line Contents: {line}")
                    contents = line.split(sub)[1]
                    print(f"Compiled FocusLine: {contents}")
                    return contents
                    break
                else:
                    print(f"{focusLine[0]} != {profileEntry}")
                    continue


def writeProfiles(profileEntry, replaced):
    with open("profiles.txt", "w") as _f:
        pass

if __name__ == "__main__":
    print("""-----------------------
- This is a TEST CALL -
-----------------------
- This call is not for running (hence the __name____main__ call)""")
    test = readProfiles("test")
    print(f"FOUND CALL: {test}")
