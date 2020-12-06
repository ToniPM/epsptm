import numpy as np

from baseclasses.splitModel import SplitModel, DiffusionModel
from diffusionModel import LocalDiffusionModel, TravelDiffusionModel, StackedDiffusionModel
from populations import from_file
from visualization.modelArtist import GridModelArtist
from visualization.modelScreen import ModelScreen


class BasicModel(SplitModel):

    def __init__(self,
                 population: np.ndarray,
                 reproduction: float,
                 mortality: float,
                 survival: float,
                 diffusion_model: DiffusionModel,
                 population_adjustment=False,
                 stochastic=True):

        super().__init__(diffusion_model,
                         population_adjustment=population_adjustment,
                         stochastic=stochastic)

        self.population = population

        #corrected rates for exponential models
        self.survival = survival
        self.mortality = -np.log(1-mortality)
        self.reproduction = -np.log(1-reproduction)

        self.space = self.population.shape

        self.healthy = self.population.copy()
        self.infected = np.zeros(self.space)
        self.survived = np.zeros(self.space)
        self.deceased = np.zeros(self.space)

    def infect(self, pos):
        if self.population[pos]<1:
            raise Exception("Attempted to infect extremely low density area")
        self.healthy[pos] -= 1
        self.infected[pos] += 1


    def step(self):
        phi = self.getExpectedInfections()
        new_infected = phi*self.healthy/self.population if self.population_adjustment else phi*self.healthy
        new_deceased = self.infected*self.mortality
        new_survived = self.infected*self.survival

        self.healthy -= new_infected
        self.deceased += new_deceased
        self.survived += new_survived
        self.infected += new_infected - new_deceased - new_survived


    def getExpectedInfectiousness(self) -> np.ndarray:
        return self.infected*self.reproduction

    def getHealthy(self):
        return self.healthy

    def getInfected(self):
        return self.infected

# class ProgressModel(SplitModel):
# class DemographyModel(SplitModel):
# class FullModel(SplitModel):

if __name__=="__main__":
    import networkx as nx

    #population = from_file("maps/spain_small.png",1000)
    population = from_file("maps/spain_hd.png",100)

    #bcn, mdd, vlc = (60,215),(100,90),(120,170)
    bcn, mdd, vlc = (230,840),(340,420),(440,666)

    G = nx.DiGraph()
    G.add_nodes_from([bcn,mdd,vlc])
    G.add_edge(bcn,mdd,traffic=0.01)
    G.add_edge(mdd,vlc,traffic=0.01)
    G.add_edge(vlc,bcn,traffic=0.01)
    travel_diffusion_model = TravelDiffusionModel(5, 20, G)

    local_diffusion_model = LocalDiffusionModel(0.5,1)
    diffusion_model = StackedDiffusionModel(travel_diffusion_model, local_diffusion_model)

    model = BasicModel(population, 0.001, 0.001, 0.002,
                       diffusion_model,
                       population_adjustment=False,
                       stochastic=False)

    gridModelArtist = GridModelArtist()
    modelScreen = ModelScreen(model,gridModelArtist, size=(1000,800))

    #model.infect(bcn)
    #model.infect(vlc)
    [model.infect(mdd) for _ in range(100)]
    #from matplotlib import pyplot as plt
    #plt.imshow(population)
    #plt.show()
    modelScreen.run_simulation(100000, 1)
