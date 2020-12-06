# epsptm

### Introduction (the why)

This project was started because of a discussion regarding the use of "per capita" units in comparing how different countries have been affected by the recent pandemic - in particular, how fair these comparisons were when devoid of context. In essence, the disagreement was regarding which of these two models was more legitimate:

(a) <img src="https://render.githubusercontent.com/render/math?math=I' = kI(P-I)">

(b) <img src="https://render.githubusercontent.com/render/math?math=I' = kI(P-I)P">

If one makes the assumption that population density is linear with rate of spread of disease, using the above models to compare different countries is tantamount to assuming:

(a) Both countries have the same population density, i.e. area scales with population

(b) Both countries have the same area, i.e. density scales with population

I was curious whether a framework could be developed to compare two countries that, as is usually the case, have different surface area and population density (and distribution thereof). This eventually grew to also encompass disease progression and demographic factors.

**Take note that** spatial epidemiology and epidemiological modeling are academic areas that exist, that I have no experience in, and that would surely provide far more nuanced and accurate takes on the subject matter than anything in this repository. **This is only a hobby project.**

### Model (the what)

Both of the above models have a constant <img src="https://render.githubusercontent.com/render/math?math=P"> (population) and a variable <img src="https://render.githubusercontent.com/render/math?math=I">, infected people, depending on time. It is straightforward to also include <img src="https://render.githubusercontent.com/render/math?math=S"> (survived) and <img src="https://render.githubusercontent.com/render/math?math=D"> (deceased), and thus <img src="https://render.githubusercontent.com/render/math?math=H=P-(I %2B S %2B D)"> (healthy and susceptible to infection). Therefore, given some measurable space <img src="https://render.githubusercontent.com/render/math?math=\mathbb{X}"> which we understand to be the area on which our epidemic is spreading, we use the first model on every point of this space, with some diffusion - given <img src="https://render.githubusercontent.com/render/math?math=i,s,d\in\mathbb{R}"> representing the infectiousness and survival/death rate:

With x and t being space/time variables, i.e. <img src="https://render.githubusercontent.com/render/math?math=x\in\mathbb{X}, y\in\mathbb{T}=\mathbb{R}">, then <img src="https://render.githubusercontent.com/render/math?math=\frac{dI(x,t)}{dt} = iI_E(x,t)H(x) - \frac{dD(x,t)}{dt} - \frac{dS(x,t)}{dt}, \quad \frac{dD(x,t)}{dt} = ln(1-d)\cdot I(x,t), \quad \frac{dS(x,t)}{dt} = ln(1-s)\cdot I(x,t)">

Where <img src="https://render.githubusercontent.com/render/math?math=I_E"> is exogenous infection density, <img src="https://render.githubusercontent.com/render/math?math=I_E(x,t) = \int_{y\in\mathbb{X}}V(x,y)\cdot I_I(y,t)">

Where <img src="https://render.githubusercontent.com/render/math?math=I_I"> is raw infection density, <img src="https://render.githubusercontent.com/render/math?math=I_I(x,t) = i\cdot I_I(y,t)">

in here <img src="https://render.githubusercontent.com/render/math?math=V(x,y)"> is called a transfer map, and it models infection diffusion (thus it is bound to having its first marginal be equal to one everywhere). For example, a straightforward choice would be:

<img src="https://render.githubusercontent.com/render/math?math=V(x,y) = G(x-y)">

where <img src="https://render.githubusercontent.com/render/math?math=G"> is the usual gaussian kernel. It is also important to model travel - mathematically speaking, <img src="https://render.githubusercontent.com/render/math?math=V"> is perfectly capable of doing this, but it is not straightforward to actually define a function with first marginal one that can have bumps at the desired <img src="https://render.githubusercontent.com/render/math?math=(x,y)"> pairs (modeling travel from <img src="https://render.githubusercontent.com/render/math?math=x"> to <img src="https://render.githubusercontent.com/render/math?math=y">).

In implementation, straightforward gaussian difussion is accomplished by LocalDiffusionModel. TravelDiffusionModel does what it's name promises, but it is unclear to me if it can be written in the <img src="https://render.githubusercontent.com/render/math?math=V(x,y)"> form or if it is just a 1-norm preserving map from <img src="https://render.githubusercontent.com/render/math?math=\mathbb{R}^\mathbb{X}"> to <img src="https://render.githubusercontent.com/render/math?math=\mathbb{R}^\mathbb{X}"> (in the way that <img src="https://render.githubusercontent.com/render/math?math=V"> is used to define a map <img src="https://render.githubusercontent.com/render/math?math=I_I\mapsto I_E">). It is interesting to note that TravelDiffusionModel takes a directed graph as argument to its constructor, and in essence distributes infection along the edges of those graph - this is tantamount to using a local diffusion model on the space obtained by collapsing the original space along that directed graph (some "balance" restrictions on the graph ensure that this is well defined). This might be relevant in the future, as while the model is defined for non-flat surfaces (indeed, any measurable space will do), there is as of yet no implementation of this, which will be necessary for global simulations (no matter their scale).

It is also worthwhile to note that, in making the model general enough to use any measure space as <img src="https://render.githubusercontent.com/render/math?math=\mathbb{X}">, this also includes finite measure spaces, which subsumes discrete county-based & similar models. This also lets us avoid having to worry about geometry.

### Further generalization

Though not yet implemented, there are two pending generalizations of the model (which can both be applied at the same time):

- Along a(nother) time axis, <img src="https://render.githubusercontent.com/render/math?math=\mathbb{T}'=\mathbb{R}">

The <img src="https://render.githubusercontent.com/render/math?math=i,s,d"> parameters are now functions <img src="https://render.githubusercontent.com/render/math?math=\mathbb{T}'\rightarrow\mathbb{R}"> indicating infection, survival and death rate density for people some f time along the disease (multiplicatively, for <img src="https://render.githubusercontent.com/render/math?math=d"> and <img src="https://render.githubusercontent.com/render/math?math=s">). Then, <img src="https://render.githubusercontent.com/render/math?math=P,S,D"> as before, and <img src="https://render.githubusercontent.com/render/math?math=I"> is now a map <img src="https://render.githubusercontent.com/render/math?math=\mathbb{X},\mathbb{T},\mathbb{T}'\rightarrow\mathbb{R}">. We can define total infections at a point (analogous to <img src="https://render.githubusercontent.com/render/math?math=I"> in the last section) as <img src="https://render.githubusercontent.com/render/math?math=I_T(x,t) = \int_{f\in \mathbb{T}'}I(x,t,f)">, and in a way analogous to before <img src="https://render.githubusercontent.com/render/math?math=H = P-(I_T %2B D %2B S)">. The actual evolution rules then are:

<img src="https://render.githubusercontent.com/render/math?math=I(x,t,0) = I_E(x,t)\cdot H(x,t)">

<img src="https://render.githubusercontent.com/render/math?math=I_E(x,t) = \int_{y\in\mathbb{X}}V(x,y)I_I(x,t)">  

<img src="https://render.githubusercontent.com/render/math?math=I_I(x,t) = <I(y,t,\cdot),i(\cdot)>_{\mathbb{T}'} \quad\quad <f,g>_A = \int_{x\in A}f(x)g(x)">  

<img src="https://render.githubusercontent.com/render/math?math=\frac{dI(x,t,f)}{dt} = -\frac{dI(x,t,f)}{df} %2B I(x,t,f)ln(1-d(f)) %2B I(x,t,f)ln(1-s(f))">

<img src="https://render.githubusercontent.com/render/math?math=\frac{dH(x,t)}{dt} = -I(x,t,0)">

<img src="https://render.githubusercontent.com/render/math?math=\frac{dS(x,t)}{dt} = -<I(x,t,\cdot),ln(1-s(\cdot))>_{\mathbb{T}'}">

<img src="https://render.githubusercontent.com/render/math?math=\frac{dD(x,t)}{dt} = -<I(x,t,\cdot),ln(1-d(\cdot))>_{\mathbb{T}'}">

Note that common sense suggests that <img src="https://render.githubusercontent.com/render/math?math=\mathbb{T}'"> be a finite measure metric space (thus literally finite in implementation). In practice, this means assuming <img src="https://render.githubusercontent.com/render/math?math=d %2B s=1"> after a certain point.

This involves keeping track of how much people are f time along the disease in each point in space. The use of curves as parameters, then, allows for modeling things such as incubation periods. Note that "time along disease" is basically a shorthand for "disease state", so it is possible to go further and define a "disease state space" with a transfer map along this space and <img src="https://render.githubusercontent.com/render/math?math=i,s,d"> exactly like before. Notably, this makes computation more awkward.

- Along a demographic axis <img src="https://render.githubusercontent.com/render/math?math=\mathbb{D}">

Similarly to before, almost every function gets a new parameter for density along <img src="https://render.githubusercontent.com/render/math?math=\mathbb{D}">

<img src="https://render.githubusercontent.com/render/math?math=P:\mathbb{X}\times\mathbb{D}\rightarrow\mathbb{R},\quad H,I:\mathbb{X}\times\mathbb{T}\times\mathbb{D}\rightarrow\mathbb{R},\quad S,D:\mathbb{X}\times\mathbb{T}\rightarrow\mathbb{R},\quad i,s,d:\mathbb{D}\rightarrow\mathbb{R}">

Moreover, a new parameter is added, <img src="https://render.githubusercontent.com/render/math?math=w:\mathbb{D}\rightarrow\mathbb{R}">, for susceptibility to the disease. And thus,

<img src="https://render.githubusercontent.com/render/math?math=I_I(x,t) = <I(y,t,\cdot),i(\cdot)>_{\mathbb{D}}">  

<img src="https://render.githubusercontent.com/render/math?math=I_E(x,t) = \int_{y\in\mathbb{X}}V(x,y)I_I(x,t)"> 

<img src="https://render.githubusercontent.com/render/math?math=\frac{dI(x,t,v)}{dt} = I_E(x,t)w(v)H(x,v)  %2B I(x,t,v)ln(1-d(v)) %2B I(x,t,v)ln(1-s(v))"> 

<img src="https://render.githubusercontent.com/render/math?math=\frac{dH(x,t,v)}{dt} = -I_E(x,t)w(v)H(x,v)">

<img src="https://render.githubusercontent.com/render/math?math=\frac{dS(x,t)}{dt} = -<I(x,t,\cdot),ln(1-s(\cdot))>_{\mathbb{D}}">

<img src="https://render.githubusercontent.com/render/math?math=\frac{dD(x,t)}{dt} = -<I(x,t,\cdot),ln(1-d(\cdot))>_{\mathbb{D}}">

Essentially having a "demographic space", which a density along this space defined at each point in actual space, and each point in demographic space reacting differently to the disease (more susceptible, less infectious, etc)

- Policy

It would also be very useful to model policy factors - likely not in an "autonomous" way, as this would require modeling of awareness, but as options in some graphical interface that let us control travel restrictions, social distancing, etc. These restrictions in themselves would be very easy to implement in the model.

- Models as a format

Note that it is possible (though somewhat ill-defined) to map more general models to less general models and viceversa - for instance, given some disease-state-space curves <img src="https://render.githubusercontent.com/render/math?math=i,s,d">, one might find constants <img src="https://render.githubusercontent.com/render/math?math=i',s',d'"> such that a model without disease-state-space using constants <img src="https://render.githubusercontent.com/render/math?math=i',s',d'"> had the same expected infections per infected person, expected deaths, etc. This doesn't mean that the models would perform at all similarly, but it is in some sense a projection. This is useful because one might be interested in writing the disease parameters in one format but executing the model in another, faster format. When this is implemented, it will also be time to worry about the precise format of the data, i.e. the units used. 

### Considerations

#### About the model

- Starting conditions

Initial values of variables have not been given as the sensible ones are pretty easy to intuit. Notably, <img src="https://render.githubusercontent.com/render/math?math=I"> has to start **not** being 0 a.e., otherwise no infection would ever begin.

- Extraneous factors

There is an unspoken (and pretty dubious) assumption that the rest of the world stops in its tracks for the length of the epidemic - i.e. there are no natural deaths, births, aging, etc. It would be possible to include this in the model, but it probably won't be, as it is almost orthogonal to the concerns of the project.

- Symmetries

One might note that in all models proposed, <img src="https://render.githubusercontent.com/render/math?math=(d,D)"> and <img src="https://render.githubusercontent.com/render/math?math=(s,S)"> are symmetric, that is, their parameters can be switched up and they will behave exactly the same. It is obviously not the same for a person to survive a disease or just die from it, but if you squint hard enough it might be possible to convince yourself that this has the same effect on the spread of disease.

Nonetheless, this isn't ideal, as *amount of deaths* is surely one of the metrics one is interested in when running simulations of epidemics. Indeed, it is planned in the future to introduce factors that eliminate this symmetry: for instance, areas less affected by the epidemic could have a higher survival rate due to their medical resources being freed up.

<!---
Hi! Why are you looking at the source?

If you're curious about why this section is commented out, it's because I'm waiting for it to make sense. Essentially I planned to go in a direction of "what if really the diameter of X is like, super small, so actually spatial diffusion doesn't matter?" However this is obviously untrue, because things like air travel restrictions exist. However, it feels like the same reasoning might be applicable at a smaller scale, perhaps iteratively. Graph of graphs of graphs of... is another obvious idea for epidemiological modeling, isn't it?


- The ¿importance? of <img src="https://render.githubusercontent.com/render/math?math=\mathbb{X}">

My impression (which needs to be colored by the results of models taking into account demographics) is that space might be less relevant than I imagined. To explain:

Say you have the surface of earth, as a geodesic metric space. One may "collapse" any metric space by a finite weighted graph with nodes being part of this metric space: simply assert the distance (in the metric space) of any two points on the graph is the minimum of their distance on the metric space and the distance on the graph. Then, adjust the distance of every other pair of points in the metric space such that it obeys the triangle inequality. Evidently it takes a bit more effort to prove that this last step makes sense, but it is an easy concept to parse either way. Note that if all weights on the graph are 0, this corresponds to collapse by the set of vertices in the topological space induced by the metric space.

Then, as was alluded to before, it is sensible to, instead of understanding travel as diffusion by means of teleportation, rather understand the metric space that the epidemic lives in as the surface of the earth collapsed by air travel routes (and probably other means of fast transportation). It becomes relevant, then, to note that most humans out there live a remarkably short distance from each other: Indeed, if you had infinite money, you could in less than a day go to places our ancestors would've needed an entire life's journey to see. Taking into account that, in a loose sense, the behaviour of epidemics everywhere is shaped by the behaviour of epidemics where most people live, 
-->

#### About the implementation

There are two notes about the implementation that would be fairly difficult to talk about in a modeling context. Namely:

- Stochasticity

Implemented models have a boolean parameter, "stochastic". If this is enabled, at each simulation step <img src="https://render.githubusercontent.com/render/math?math=I"> is rounded to a nearby integer at every point in <img src="https://render.githubusercontent.com/render/math?math=\mathbb{X}">, which probability scaled by its proximity to that integer. This makes the simulations look a lot different in general, but its main purpose is for travel modeling: It makes infection over long distances a matter of chance, as opposed to the continuous model where as soon as there's an infection in New York, 2% of an infected person appears in Shanghai, eventually growing into a whole epidemic.

Note that, since infection numbers usually start small, stochastic rounding actually makes it significantly harder for infections to progress. It might be interesting to do some statistics to find out how one should adjust the parameters to get similar (in some sense) behaviour from a stochastic and a properly continuous model.

- Visualization

There are four variables to keep track of for every point in space (and disease space, and demographic space, but that's a whole other thing): Healthy people, infected people, deceased people, and people who survived the infection. Picking a representative color for each of these and interpolating for combinations by necessity yields a 3-dimensional color space, which leaves us with no spare dimensions to indicate population density. A possible fix to this is to apply a dithering algorithm with those four colors to obtain a loose representation of I:H:D:S, and then scaling their brightness by population. Note that for this to not look terrible we'd want the result of this dithering to be stable wrt. small changes in the continuous I:H:D:S map we're trying to approximate (there exist methods to accomplish this, though to my understanding they are not straight-forward). Another solution would be to substract the deceased from the population, as surely seeing cities fade into the background will convey the message. Note that applying both of the proposed solutions together would make it possible for people with certain types of colorblindness to properly read the model.

- Computation

Everything heavy is done with numpy, which performs well enough if one is conscetious about what parameters to use (i.e. convolution kernels with small radius, low-cardinality disease state/demographic spaces, etc). The simple models shown below, running with a 7x7 convolution matrix on a roughly 900x900 grid, and no disease state/demography run at roughly 10 iterations per second. There might be a significant performance gain to be achieved by using cupy or numba.

#### In general

I get the impression that this model is one of the most accurate one can get without using agent models. This isn't really meant as praise - it is not very surprising that a model with several parameters living in infinite-dimensional vector spaces would have the capacity of being accurate. Indeed, most models can overfit if given enough parameters. It is my impression that, while this model may never be useful at modeling actual real-world scenarios, simply because it is unfeasible to get all the data it demands (note, for instance, the diffusion map, which asks for information about the displacement habits of every single person on earth), it is worthwhile as a simulation tool, giving the user fine-tuned control over the epidemiological aspects of a certain disease. 

### Some simulations

Simulations are run on a 900x900-ish population density map of spain:

![](https://i.imgur.com/2wjHRzL.png)

For now, air travel is introduced by hand, so there is just a constant Madrid->Valencia->Barcelona->Madrid cycle. This is somewhat hacky, and some way to read air travel data from some database will be introduced later. The population density map itself is also just a blurred population density map off the internet - in the future, NASA's [publicly available population density](https://sedac.ciesin.columbia.edu/data/set/gpw-v4-population-density-rev11) maps will be used. Infections were started in Madrid. This isn't meant to be commentary on anything, it's just an interesting place to start infections by virtue of being a very populous city in the middle of a mostly empty expanse.

As mentioned, the models implemented for now are quite simple, yet there is already some behaviour worth noting. Letting i be the expected infections per infected person per healthy person, and s and d be the chance an infected person survives/dies during any one iteration. Then, a stochastic model with i,s,d = 0.01, 0.05, 0.025 takes roughly 1700 iterations to settle at

![](https://i.imgur.com/IEG1VIL.png)

Wherein green areas are unaffected by the infection, and the grayish blue means 2/3rds immunized, 1/3rd dead. In this particular simulation there was no infection by air(plane) - the red (now grayish blue) blob extended to the southeast from Madrid, through Albacete and into Murcia, and then along the coast in both directions. Without air travel, it gives the impression that this might be a better simulation of small-scale (in space *and* time) infection, or large-scale infection in the middle ages.

Doubling both s and d:

![](https://i.imgur.com/o6KE1N4.png)

This is common sense, but it's nice to see it arise on its own nonetheless. The faster people either overcome the disease or pass, the less the infection can spread.

As was mentioned before, the results are quite different with non-stochastic models. Using the same combination of parameters:

![](https://i.imgur.com/jkF5ql3.png)

![](https://i.imgur.com/79g2DKQ.png)

Indeed, the results are a lot more predictable: Infections take root only in the areas that (rather, in all areas that) have high enough population density to support them, and affect every area within a certain radius of these high-population areas. Note that, despite the lack of air travel, epidemics can more-or-less teleport across the country. This is because saying that "infections can only take root in such-and-such areas" is too naïve: in truth, the epidemic simply has a different saturation level at each point in the map, depending on the local density. Thus, while in the stochastic model any "maximum possible saturation" below one makes the epidemic incredibly unlikely, non-stochastic models basically fill out the map up to its (nonzero if the population is nonzero) saturation point everywhere.
