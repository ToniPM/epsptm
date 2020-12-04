import numpy as np
from scipy.signal import convolve2d
import networkx as nx

from baseclasses.splitModel import DiffusionModel


def _get_explicit_gaussian_kernel(variance,radius,norm=1):
    diameter = 2*radius+1
    x,y = np.meshgrid(np.linspace(-radius, radius, diameter), np.linspace(-radius, radius, diameter))
    sqd = x*x+y*y
    var_coef = 2*variance*variance
    convolution = np.exp(-sqd/var_coef)
    convolution *= norm/np.sum(convolution)
    return convolution


class StackedDiffusionModel(DiffusionModel):
    def __init__(self, *diffusion_models):
        self.diffusion_models = diffusion_models

    def diffuse(self, expected_infectiousness) -> np.ndarray:
        for diffusion_model in self.diffusion_models:
            expected_infectiousness = diffusion_model.diffuse(expected_infectiousness)
        return expected_infectiousness


class LocalDiffusionModel(DiffusionModel):

    def __init__(self, variance, radius):
        self.convolution = _get_explicit_gaussian_kernel(variance,radius)

    def diffuse(self, expected_infectiousness) -> np.ndarray:
        return convolve2d(expected_infectiousness, self.convolution, mode="same")


class TravelDiffusionModel(DiffusionModel):

    def __init__(self, variance, radius, transfer_graph: nx.DiGraph):
        self.radius = radius
        self.variance = variance
        self.convolution = _get_explicit_gaussian_kernel(variance,radius)
        self.transfer_graph = transfer_graph

        out_traffic_density = {origin:sum([transfer_graph[origin][destination]["traffic"]
                                                for destination in transfer_graph[origin]])
                                    for origin in transfer_graph}

        # impressively inefficient one-liner
        in_traffic_density = {destination:sum([transfer_graph[origin][destination]["traffic"]
                                                for origin in transfer_graph if destination in transfer_graph[origin]])
                                    for destination in transfer_graph}

        if max([abs(in_traffic_density[node]-out_traffic_density[node]) for node in transfer_graph])>1e-3:
            raise Exception("traffic in transfer graph provided is unstable")

        if max([out_traffic_density[node] for node in transfer_graph])>1:
            raise Exception("traffic in transfer graph provided exceeds 100% leaving")

        self.out_traffic_density = out_traffic_density

    def diffuse(self, expected_infectiousness) -> np.ndarray:
        r = self.radius

        max_out_traffic = dict()
        in_traffic = {destination:0 for destination in self.transfer_graph}
        for origin in self.transfer_graph:
            x,y = origin
            max_out_traffic[origin] = np.sum(expected_infectiousness[x-r:x+r+1,y-r:y+r+1]*self.convolution)
            expected_infectiousness[x-r:x+r+1,y-r:y+r+1] *= 1 - self.out_traffic_density[origin]*self.convolution
            for destination in self.transfer_graph[origin]:
                in_traffic[destination] += max_out_traffic[origin]*self.transfer_graph[origin][destination]["traffic"]

        for destination in self.transfer_graph:
            x,y = destination
            expected_infectiousness[x-r:x+r+1,y-r:y+r+1] += in_traffic[destination]*self.convolution
        return expected_infectiousness


if __name__=="__main__":

    def  eq_exp():
        G = nx.DiGraph()
        G.add_nodes_from([(50,50),(50,100),(100,50),(100,100)])
        G.add_edge((50,50),(50,100),traffic=0.5)
        G.add_edge((50,100),(100,100),traffic=0.5)
        G.add_edge((100,100),(100,50),traffic=0.5)
        G.add_edge((100,50),(50,50),traffic=0.5)

        pop = np.zeros((200,200))
        pop[25:75,25:75] = 1
        pop[125:175,125:175] = 1

        diffusion_model = TravelDiffusionModel(5,20,G)


        from matplotlib import pyplot as plt
        for i in range(5000):
            if i%500==0:
                print(np.sum(pop))
                print(pop[0,0])
                plt.imshow(pop)
                plt.show()
            pop = diffusion_model.diffuse(pop)

    def stack_exp():
        G = nx.DiGraph()
        G.add_nodes_from([(50,50),(50,100),(100,50),(100,100)])
        #traffic should never be this big
        G.add_edge((50,50),(50,100),traffic=5)
        G.add_edge((50,100),(100,100),traffic=5)
        G.add_edge((100,100),(100,50),traffic=5)
        G.add_edge((100,50),(50,50),traffic=5)

        pop = np.zeros((200,200))
        pop[25:75,25:75] = 1
        pop[125:175,125:175] = 1

        travel_diffusion_model = TravelDiffusionModel(5,20,G)
        local_diffusion_model = LocalDiffusionModel(1,3)
        diffusion_model = StackedDiffusionModel(travel_diffusion_model, local_diffusion_model)


        from matplotlib import pyplot as plt
        for i in range(100):
            if i%5==0:
                print(np.sum(pop))
                print(pop[0,0])
                plt.imshow(pop)
                plt.show()
            pop = diffusion_model.diffuse(pop)

    stack_exp()