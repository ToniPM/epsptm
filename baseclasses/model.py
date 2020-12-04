
class Model:
    """
    abstract class for a growth model
    """

    #(space)-shaped tensors
    population = None
    survived = None
    deceased = None

    #(space-demographics)-shaped tensors
    healthy = None

    #(space-demographics-disease)-shaped tensors
    infected = None

    #accessors for (space)-format tensors for drawing
    def getPopulation(self): return self.population
    def getSurvived(self): return self.survived
    def getDeceased(self): return self.deceased
    def getHealthy(self): raise NotImplementedError()
    def getInfected(self): raise NotImplementedError()

    def step(self):
        """
        model evolution step
        """
        raise NotImplementedError()



