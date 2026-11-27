################
# Read Profiles
##############
def readProfiles(profileEntry):
    print(f"Searching for: {profileEntry}")

    with open("profiles.txt", "r") as f:
        for line in f:
            currentLine = line.rstrip()

            # Filter out comments
            # Prefaced with "- "
            currentArray = list(currentLine)
            if currentArray[0] == "-":
                print("Skipping comment")
                continue
            else:
                print("Found line")
                print(line)


def writeProfiles(profileEntry, replaced):
    with open("profiles.txt", "w") as _f:
        pass

if __name__ == "__main__":
    readProfiles("blank") # Add more
