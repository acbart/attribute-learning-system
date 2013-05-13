import csv

for ft in ("tree", "vector"):
    utilities = []
    for re in xrange(1, 3):
        for mu in xrange(1,4):
            fname = "results-%s-attributes-p%ds%d.data" % (ft, re, mu)
            name = "p%ds%d" % (re, mu)
            f = csv.reader(open(fname, 'rb'), delimiter='|')
            lines = [row for row in f]
            data = lines[4:]
            utilities.append([name] + [line[2] for line in data])
    csvresults = open('%s-attributes.csv' % (ft, ), 'w')
    i = 0
    for line in zip(*utilities):
        csvresults.write(str(i) + ", " + ",".join([str(x) for x in line]) + '\n')
        i += 1
    csvresults.close()