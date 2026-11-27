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
            if currentArray[0] == "-" or currentArray[0] == "\n":
                print("Skipping comment or blankline (\\n)")
                continue
            else:
                print("Running Line: ")


def writeProfiles(profileEntry, replaced):
    with open("profiles.txt", "w") as _f:
        pass

if __name__ == "__main__":
    readProfiles("blank") # Add more
