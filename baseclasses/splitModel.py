import numpy as np
from baseclasses.model import Model


class DiffusionModel:
    def diffuse(self, expected_infectiousness) -> np.ndarray:
        """
        computes phi given the infectiousness tensor
        """
        raise NotImplementedError



class SplitModel(Model):
    """
    models where the equation governing the increase of infections has a form like
        PHI * H / P + (death and survival factors)
    wherein H is the saturation dampening factor, P is an optional population correction factor,
    and PHI is some convolution or (dot) product of
        a model of displacement
        some model of space-wise "expected infectiousness"
    thus, SplitModels are parametrized by the presence/abscence of P, V and intergenous growth
    """

    def __init__(self, diffusion_model: DiffusionModel,
                 population_adjustment=False,
                 stochastic=True):
        self.stochastic = stochastic
        self.diffusion_model = diffusion_model
        self.population_adjustment = population_adjustment

    def step(self):
        """
        update all values depending on format and expected infections
        """
        raise NotImplementedError()

    def getExpectedInfections(self) -> np.ndarray:
        expected_infectiousness = self.getExpectedInfectiousness()
        expected_infections = self.diffusion_model.diffuse(expected_infectiousness)
        if self.stochastic:
            floors = np.floor(expected_infections)
            expected_infections = np.where(expected_infections-floors<np.random.uniform(0,1,floors.shape),
                                           floors,
                                           floors+1)
        return expected_infections

    def getExpectedInfectiousness(self) -> np.ndarray:
        """
        returns (space-demographics)-shaped tensor
        """
        raise NotImplementedError()

