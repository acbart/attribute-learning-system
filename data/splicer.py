import csv

for ft in ("tree", "vector"):
    utilities = []
    for re in xrange(2, 10, 2):
        for mu in xrange(0, 10, 2):
            fname = "results-%s-gen-%d-%d.data" % (ft, re, mu)
            if re + mu > 10: continue
            co = 10 - re - mu
            name = "r%d-m%d-c%d" % (re, mu, co)
            f = csv.reader(open(fname, 'rb'), delimiter='|')
            lines = [row for row in f]
            data = lines[4:]
            utilities.append([name] + [line[2] for line in data])
    csvresults = open('%s-mureco.csv' % (ft, ), 'w')
    i = 0
    for line in zip(*utilities):
        csvresults.write(str(i) + ", " + ",".join([str(x) for x in line]) + '\n')
        i += 1
    csvresults.close()