list = [1, 2, 3]

with open("src/null_dataframes.txt", "w") as f:
    for item in list:
        f.write("%s\n" % item)


nullDataFrames = open("src/null_dataframes.txt").read().splitlines()
