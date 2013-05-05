import numpy as np
d = {}
for line in open("dtn.log", "r"):
    ad, av, ac = line.split(", ")
    if int(ad) > 1:
        if int(ad) in d:
            d[int(ad)].append(float(av))
        else:
            d[int(ad)] = [float(av)]
    
for key, values in d.iteritems():
    print key, np.mean(values, dtype=np.float64), np.std(values, dtype=np.float64), min(values), max(values)
