import os.path


# method reads a list of known airports and their basic parameters
def readairportslist():
    filename = "util/airports.dat"

    if os.path.isfile(filename):
        f = open(filename)
        # reading full line content
        inputdatalist = (line.replace('""', '000').translate(None, '"').rsplit(',') for line in f)
        # storing just necessary information about the airports
        processedlist = []
        for line in inputdatalist:
            if not any(char.isdigit() for char in line[4]) :
                processedlist.append((line[4], line[2], line[3], line[6], line[7], line[8]))
        # sort w.r.t. airport code
        processedlist.sort()
        return processedlist
    else:
        print "Couldn't find a file " + filename + "\nAborting execution"
        exit()
