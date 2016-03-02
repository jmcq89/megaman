import numpy as np
from sklearn import neighbors

# from six.py
def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    return meta("NewBase", bases, {})


class AdjacencyMeta(type):
    """Metaclass for Adjacency object which registers subclasses"""
    def __init__(cls, name, bases, dct):
        if name == 'NewBase':
            # class created as part of six.with_metaclas
            pass
        elif not hasattr(cls, '_method_registry'):
            # this is the base class.  Create an empty registry
            cls._method_registry = {}
        else:
            # this is a derived class.  Add cls to the registry
            interface_id = name.lower()
            cls._method_registry[getattr(cls, 'name', name.lower())] = cls

        super(AdjacencyMeta, cls).__init__(name, bases, dct)


class Adjacency(with_metaclass(AdjacencyMeta)):
    """Base class for adjacency methods"""
    @classmethod
    def get_method(cls, name):
        return cls._method_registry[name]

    @classmethod
    def methods(cls):
        return cls._method_registry.keys()

    def __init__(self, radius=None, n_neighbors=None,
                 mode='distance', kwds=None):
        self.radius = radius
        self.n_neighbors = n_neighbors
        self.mode = mode
        self.kwds = kwds or {}

        if (radius is None) == (n_neighbors is None):
           raise ValueError("Must specify either radius or n_neighbors, "
                            "but not both.")

    def adjacency_graph(self, X):
        if self.n_neighbors is not None:
            return self.knn_adjacency(X)
        elif self.radius is not None:
            return self.radius_adjacency(X)

    def knn_adjacency(self, X):
        raise NotImplementedError()

    def radius_adjacency(self, X):
        raise NotImplementedError()


class BruteForceAdjacency(Adjacency):
    name = 'brute'

    def radius_adjacency(self, X):
        model = neighbors.NearestNeighbors(algorithm=self.name).fit(X)
        return model.radius_neighbors_graph(radius=self.radius,
                                            mode=self.mode)

    def knn_adjacency(self, X):
        model = neighbors.NearestNeighbors(algorithm=self.name).fit(X)
        return model.kneighbors_graph(n_neighbors=self.n_neighbors,
                                      mode=self.mode)


class KDTreeAdjacency(BruteForceAdjacency):
    name = 'kd_tree'


class BallTreeAdjacency(BruteForceAdjacency):
    name = 'ball_tree'