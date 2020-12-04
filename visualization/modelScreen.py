import cv2
import numpy as np

from baseclasses.model import Model
from visualization.modelArtist import ModelArtist

MAX_SIZE=800


class ModelScreen:
    def __init__(self, model: Model, modelArtist: ModelArtist, size=None):
        self.model = model
        self.modelArtist = modelArtist
        self.size = size

    def run_simulation(self, step_qt, draw_every):
        if self.size is not None:
            cv2.namedWindow("sim",cv2.WINDOW_NORMAL)
            cv2.resizeWindow("sim", *self.size)
        for index in range(step_qt):
            self.model.step()
            if index%draw_every==0:
                print("Iteration {}".format(index))

                im = self.modelArtist.draw(self.model)
                formatted_im = np.flip(im/255,axis=-1)

                cv2.imshow("sim", formatted_im)
                cv2.waitKey(1)






if __name__=="__main__":
    from visualization.modelArtist import GridModelArtist
    class TestModel(Model):
        def __init__(self,shape):
            self.shape = shape
            self.randomize()
        def step(self): self.randomize()
        def randomize(self):
            self.healthy = np.random.uniform(0,100,self.shape)
            self.infected = np.random.uniform(0,100,self.shape)
            self.survived = np.random.uniform(0,100,self.shape)
            self.deceased = np.random.uniform(0,100,self.shape)
            self.population = self.healthy+self.infected+self.survived+self.deceased
        def getHealthy(self):
            return self.healthy
        def getInfected(self):
            return self.infected

    testModel = TestModel((300,500))
    gridModelArtist = GridModelArtist()
    modelScreen = ModelScreen(testModel,gridModelArtist)
    modelScreen.run_simulation(100, 5)