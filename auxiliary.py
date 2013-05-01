def random_weighted_subset(weights, max_length):
    features = []
    for x in xrange(random.randint(1, max_length)):
        possibilities = []
        for feature, occurrences in weights.items():
            if feature not in features:
                possibilities += [feature] * occurrences
        features.append(random.choice(possibilities))
    return features