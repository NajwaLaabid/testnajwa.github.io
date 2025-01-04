
# Different views on diffusion models
## vs generative models: latent variable, likelihood-based estimation
- this is the view that was originally called 'diffusion probabilistic model' by sohl-dickstein
  - this is also where elbo was proposed as a loss => from song's article again '... and learn a variational decoder to reverse a discrete diffusion process that perturbs data to noise.'
- perspective directly connects to VAEs, lossy compression, and can be directly incorporated with variational probabilistic inference
- a latent variable model where latents are of the same dimension as the true data + the encoding process/procedure is fixed
- we can get the likelihood from the connection between normalizing flows and diffusion models, also from the probability flow ODE (?)
  - what does likelihood-based model mean in this context? like are we actually directly optimizing the likelihood somehow?
  
## score matchig view
- score-matching methods were later shown to be equivalent to diffusion probabilistic models
  - probably best to describe these as separate methods then show their connection to dpms and other generative models (think paper showing equivalence between all of them)
  - the connection was first drawn by Ho et al. when they were trying to improve the performance of diffusion probabilistic methods:
    - they showed the the elbo and this weighted loss used by score matching are equivalent
    - they also used a 'score-based decoder with a u-net architecture' and improved the performance of dpms to sota
- this type of model is 'directly connected to schrodinger bridges and optimal transport' => how?
- 'train the score matching model on the noisy data'
  - is it training the score matching on nosiy data though? how are we learning a score model in diffusion anyway? how is that learning affected by the noising process?
    - we try to match 'noised' scores now
      - denoising score matching
    - how is score matching involved in diffusion models anyway?
- Also has a connection to SDEs by 'generalizing the number of noise levels/scales to infinity' 
  - noise perturbation = a 'continuous time stochastic process' 
    - formal definition of a stochastic process? 
      - diffusion process is a subcategory
      - many are solutions to SDEs: SDE offers a concise description/definition of the process
        - made of drift and diffusion coefficients
      - Brownian motion as an example of a stochastic process
    - example of discrete time stochastic process?
  - advantages of SDE view/continuous time perturbation:
    - higher quality samples => why? just a 'finer' / more refined version of the same process?
    - is this what's considered 'continuous time' diffusion models?
    - exact log-likelihood computation => only possible in the infinite noise setup?  
    - controllable generation for inverse problem solving 
      - but since then controllable generation has been developped for discrete time diffusion models too right?
      - also what advantages do discrete time models have over continuous time? or why were they invented in the first place?
      - what is 'inverse problem solving'? how does it relate to controllable generation?
  - analogy between SDE and discrete-time process:
    - dx = e^t dw => equivalent to add discrete noise with variance forming a geometric progression
      - connection between geometric progression and exponentially growing variance
      - connection between SDE and 'noise schedule'? is the noise schedule basically the variance of the normal distribution or can it be smthg else too?
  - properties of the various SDEs/noise schedules and what can be done there
  
# Forward process
- explain the forward process equation: $q(x_t|x_{t-1}) = \mathcal{N}(x_t; \sqrt{1 - \beta_t} x_t, \beta_t \mathcal{I})$
  - what does it look like for a discrete process?
  - what are the requirements for a noising process in general?
- effect of Song's recommendations: 
  - why geometric progression of variance/std (and does it matter which)? 
  - why maximum variance comparable to the maximum pairwise distance between all pairs of data points?
- one intuition behind noising is easy to see though: adding noise would populate low density regions
  - at the extreme a totally noised out data point is a sample from a Gaussian (or whatever the stationary distribution is)
  - hmm is it correct to say that we replace the data density with Gaussian densities of different moments?
  - also not clear to me how someone would think 'adding noise should help here' aren't we learning incorrect scores now?
    - apparently the idea has been used in multiple other domains/methods, like annealing importance sampling, simulated annealing, etc
    - 
- noising mathematically: 
  - there is this equaiton: p_{\sigma_i}(x) = \int p(y) \mathcal{N}(x;y, \sigma_i^2 \mathcal{I}) dy (from song's [blog](https://yang-song.net/blog/2021/score/) about score matching)
  - how does it relate to adding a sample from a Gaussian: x_{\sigma_i} = x + e, e \sim N(0; \sigma_i^2 I)
    - is this how you sample from p_{\sigma_i}(x)? 
    - is it the same as: x_{\sigma_i} = x + \sigma_i^2 e, e \sim N(0; \sigma_i^2 I)

# Reverse/denoising process
- why are U-net skip connections recommended?
- apply exponential moving average (ema) on the weights of the score-based model when it's used at test time?
    
# Losses
- Fisher divergence
  - what is it? what does it mean intuitively?
  - why do we use a weighted sum of fisher divergences of noisy scores? what effect does choosing the weight as the noise variance have on the training/loss?
  - in the time-continuous case, how does the specific choice of $\lambda(t)$ 'balance the magnitude of different score matching losses over time'?
    - and why is that helpful/important?
  - again on the choice of the weighting function: 
    - why does $\lambda(t) = g(t)^2$ lead to a connection to KL between approximate target distribution p_{\theta} and true data distribution $p_0$ (pbbly need to look into derivations for this)?
    - also connection to likelihood maximization from this: I understand likelihood max = KL min, but is this also related somehow to diffusion models being likelihood-based? and to the probability flow ODE? and to any other way to estimate the likelihood using a diffusion model (if any others exist)?
  - on the pros and cons of choosing \lambda(t):
    - so far I know that: $\lambda(t) =  g^2(t)$ is the likelihood weighting function
      - using this weighting function maximizes the likelihood specifically
    - $\lambda(t) = ... balances out the magnitude of different score matching losses over time
    - hmm so when do we choose which actually? and if we want to maximize the likelihood, does it hurt to not be balancing ou the magnitudes of score matching losses?
  - how does fisher divergence optimization relate to elbo optimization? and to CE? also any other losses in general?
    - elbo and this weighted loss are equivalent, it was shown by Ho et al 2020 when they were trying to improve the performance of diffusion probabilistic methods
    - the connectio
- methods to optimize the loss: denoising score matching and sliced score matching

# Sampling
- Annealed Langevin dynamics: 
  - vs regular Langevin dynamics? 
  - what is the effect of annealing in this context?
  - is seen as the reverse of the noise perturbation process
  - how are we sampling 'from each noisy distribution'? I find the concept of denoising easier to understand in this context
- equivalent of Langevin dynamics in continuous time models: reverse SDE
  - how is it derived (and where/by whom)? what does it mean intuitively for the stochastic process?
  - why solved backwards in time?
- the special solver for reverse-time SDEs proposed by Song
- also adaptive step-size solvers which can generate samples faster with better quality
- conceptual requirement for sampling: we just need to sample from the marginals $p_t(x)$, we do not care about the correlations between random $x_t$ samples, i.e. they can form an arbitrary trajectory
- "apply MCMC to fine-tune the trajectories obtained by regular solvers"
  - what is MCMC actually :D? and how does it apply?
  - and why do we want to 'fine-tune' the trajectories if we don't care about the trajectories? Does it increase computational efficiency? or lead to better samples in the end?
  - method is called 'predictor-corrector': predictor is the equation solver for the next time step, corrector uses only score function with 'an mcmc method like langevin dynamics and hmc'
    - hmm so langevin dynamics is an mcmc method? 
    - how else can we improve the trajectories of existing models?
    - also when we solve the sde, do we do it iteratively for each time step? or is this just when we want to apply this predictor-corrector thing?
    - hmm so the approach means combining the continuous time and discrete time sampling methods leads to the best results?
    - what does this mean "we first use the predictor to choose a proper step size $\delta t < 0$

# Likelihood estimation
- do autoregressive models have SOTA on likelihood estimation in particular? why?
  - is it because their estimation of the likelihood is the truest mathematically? p(x_1, ..., x_d) = p(x_d|x_1, ...,x_{d-1}) * p(x_2 | x_1)* ... * p(x_1)?
- soo predictor-corrector samplers + SDE solvers do not compute the exact log-likelihood of samples
    - but can they give some lower bound based on the KL divergence? 
- sampler based on ordinary differential equations allows for computing the LL 
  - based on the idea of converting any SDE to an ODE with the same marginals $p_t(x)$ => essentially replacing the stochastic trajectories with smthg more stable
  - how does the probability flow ODE/using ODE defined trajectories relate to flow-matching/flow-based models?
    - so here we're talking about an SDE based forward process and replacing the reverse process/SDE with an equivalent ODE 
    - can we have a model that is all ODEs?
    - probability flow ODE with a neural network for the score model = normalizing flow model
      - so is it invertible and all?
        - apparently yes, dunno what's the proof yet
      - are the equations/model literally exactly the same?
  - using the change of variable formula + ODE solver = an estimate for p_0 from p_T
- 'variational dequantization to obtain likelihood on discrete images' => what does this mean?

# Inverse problems/conditional or guided generation
- Apparently they're the same thing! if we have a way to estimate p(y|x) we would like to estimate p(x|y)