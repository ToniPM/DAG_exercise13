def circular_pairs(collection):
    yield from zip(collection, collection[1:]+collection[:1])