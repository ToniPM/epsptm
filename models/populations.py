import numpy as np
from PIL import Image

def test_population():
    population = np.zeros((100,100))
    population += 1
    population[10:20,10:20] = 10
    population[10:20,80:90] = 10
    population[80:90,10:20] = 10
    population[80:90,80:90] = 10
    population[14:16,14:86] = 10
    population[14:86,84:86] = 10
    population[84:86,14:86] = 100
    population[14:86,14:16] = 100
    return population

def from_file(filename: str, max_pop) -> np.ndarray:
    im = np.array(Image.open(filename))
    if len(im.shape)>2:
        im = np.mean(im,axis=2)
    im *= max_pop/np.max(im)
    return im

if __name__=="__main__":
    import os
    from matplotlib import pyplot as plt
    plt.imshow(from_file("maps/spain_small.png",100))
    plt.show()
    print(os.getcwd())