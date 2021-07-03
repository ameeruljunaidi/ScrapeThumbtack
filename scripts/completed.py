import glob
from tolist_services import serviceID
from tolist_zipcodes import zipCodeCSV

path = r"data/"
all_csv = glob.glob(path + "/*.csv")


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last, start)
        return s[start:end]
    except ValueError:
        return ""


completed = []
for file in all_csv:
    completed.append(find_between(file, "/", "."))

print(completed)
