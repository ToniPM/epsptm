import numpy as np

from baseclasses.model import Model

HEALTHY_COLOR = (136,255,130)
DECEASED_COLOR = (99,99,99)
SURVIVED_COLOR = (118,227,242)
INFECTED_COLOR = (255,79,84)

#TODO: figure out a way to convey population density aswell
#maybe colors are dithered and population is actual brightness
COLOR_TENSOR = np.stack([np.asarray(color) for color in [HEALTHY_COLOR,DECEASED_COLOR,SURVIVED_COLOR,INFECTED_COLOR]])


class ModelArtist:
    """
    class for drawing models. carries no internal state about the models, just on how to draw them
    """
    def draw(self, model) -> np.ndarray:
        raise NotImplementedError()

class DiscreteModelArtist(ModelArtist):
    """
    ModelArtist to be used when the underlying space is finite (in the cardinality sense)
    """
    def __init__(self, areas):
        """
        stores a collection of specifiers for areas of the model.
        format is up to the client, so long as drawArea can interpret it correctly
        """
        self.areas = areas

    def draw_area(self, area, image: np.ndarray, color: np.ndarray) -> None:
        """
        draws some area (provided in the same format as @ init) in the color & image specified
        """
        raise NotImplementedError()

    def draw_empty(self):
        """
        returns base blank image to be passed to drawArea
        """
        raise NotImplementedError()

    def draw(self, model: Model) -> np.ndarray:
        image = self.draw_empty()
        for area, population, healthy, deceased, survived, infected in zip(self.areas,
                                                                           model.getPopulation(),
                                                                           model.getHealthy(),
                                                                           model.getDeceased(),
                                                                           model.getSurvived(),
                                                                           model.getInfected()):
            affine_coeffs = np.asarray(healthy,deceased,survived,infected)/population
            assert abs(np.sum(affine_coeffs) - 1) < 1e-3
            color = (affine_coeffs@COLOR_TENSOR).astype(int)
            self.draw_area(area, image, color)
        return image


class GridModelArtist(ModelArtist):
    """
    ModelArtist to be used when the underlying space is flat 2D euc space
    """
    def draw(self, model: Model) -> np.ndarray:

        healthy = model.getHealthy()
        deceased = model.getDeceased()
        infected = model.getInfected()
        survived = model.getSurvived()
        population = model.getPopulation()

        affine_map = np.stack([healthy,deceased,survived,infected])/population

        error = np.max(np.abs(np.sum(affine_map,axis=0) - 1))
        if error > 1e-3:
            print("Error @ {}".format(error))

        return np.tensordot(affine_map,COLOR_TENSOR,axes=((0),(0))).astype(int)


import matplotlib.pyplot as plt
class SphereModelArtist(ModelArtist):
    """
    ModelArtist to be used when the underlying space is S_2
        (with a pretty uninteresting projection. if this was actually used for any purpose,
        both this and the associated model would have to be informed by a better projection,
        eg. dymaxion, though perhaps a more easily metrizable one would be best)

        also, mb change drawing to something that doesn't slow down for >1000 points
    """

    def draw(self, model: Model) -> np.ndarray:

        healthy = model.getHealthy()
        deceased = model.getDeceased()
        infected = model.getInfected()
        survived = model.getSurvived()
        population = model.getPopulation()

        affine_map = np.stack([healthy,deceased,survived,infected])/population
        assert np.max(np.abs(np.sum(affine_map,axis=0) - 1)) < 1e-3
        colors = np.tensordot(affine_map,COLOR_TENSOR,axes=((0),(0)))/255

        t_lon, t_lat,_ = affine_map.shape
        m_lon, m_lat = t_lon/2, t_lat/2
        d_lon, d_lat = 2/t_lon, 2/t_lat
        def project(lat,lon):
            lat, lon = d_lat*(lat-m_lat), d_lon*(lon-m_lon)
            return np.asarray([np.cos(lat)*np.cos(lon),np.cos(lat)*np.sin(lon),np.sin(lat)])

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for position in np.ndindex(colors.shape[:-1]):
            ax.scatter(*project(*position), c=np.expand_dims(colors[position],0))
        plt.show()