# Examples

<div class="profile-tabs" style="margin:0px;">

<div class="nav-tabs-navigation  col-md-12 ml-auto mr-auto">
<div class="nav-tabs-wrapper">
<ul id="tabs" class="nav nav-tabs" role="tablist">
<li class="nav-item ">
<a class="nav-link nav-link-narrow active" href="#code_basic" data-toggle="tab" role="tab" aria-selected="true"><span class="tablist-text">Simple example</span></a>
</li>
<li class="nav-item ">
<a class="nav-link nav-link-narrow" href="#code_scenarios" data-toggle="tab" role="tab" aria-selected="false"><span class="tablist-text">Running scenarios</span></a>
</li>
<li class="nav-item ">
<a class="nav-link nav-link-narrow" href="#code_vaccine" data-toggle="tab" role="tab" aria-selected="false"><span class="tablist-text">Custom interventions</span></a>
</li>
<li class="nav-item ">
<a class="nav-link nav-link-narrow" href="#code_r" data-toggle="tab" role="tab" aria-selected="false"><span class="tablist-text">R example</span></a>
</li>
</ul>
</div>
</div>

<div class="tab-content col-md-9 ml-auto mr-auto" style="padding-left:3px; padding-right:3px;">
<div class="tab-pane active" id="code_basic" role="tabpanel">
<div class="row">
<div class="col-md-12">
<p class="space-top text-left" style="padding-top:0px;">
<p class="space-top" style="margin-top:0px;">This is what an extremely simple Starsim simulation looks like:</p>
<ol>
<li>Create a susceptible-infectious-recovered (SIR) disease model with default parameters.</li>
<li>Create a random transmission network between agents (also with default parameters).</li>
<li>Run the simulation and plot the results.</li>
</ol>

```python
import starsim as ss

sim = ss.Sim(diseases='sir', networks='random') # Create the sim
sim.run() # Run the sim
sim.plot() # Plot the results
```

<img src="../assets/img/example-basic.png" width="100%" class="card-top-shadow text-center">
</div>
</div>
</div>

<div class="tab-pane" id="code_scenarios" role="tabpanel">
<div class="row">
<div class="col-md-12">
<p class="space-top text-left" style="padding-top:0px;">
You can easily customize model parameters, and run simulations in parallel:<br/>
<ol>
<li>Create a dictionary defining the parameters of the simulation.</li>
<li>Modify only those parameters you want to differ between scenarios.</li>
<li>Run the simulations in parallel, and plot the results you are interested in.</li>
</ol>

```python
import starsim as ss
import sciris as sc

# Set the parameters for the baseline simulation
pars1 = sc.objdict( # Note: can also use regular Python dictionary
    n_agents = 10_000,     # Number of agents to simulate
    networks = sc.objdict( # *Networks* add detail on how the agents interact with each other
        type = 'random',   # Here, we use a 'random' network
        n_contacts = 4     # Each person has an average of 4 contacts with other people
    ),
    diseases = sc.objdict( # *Diseases* add detail on what diseases to model
        type = 'sis',      # Here, we're creating an SIS disease
        init_prev = 0.1,   # Proportion of the population initially infected
        beta = 0.1,        # Probability of transmission between contacts
    )
)

# Make a modified version of the parameters for the scenario
pars2 = pars1.copy(deep=True)
pars2.diseases.beta = 0.2

# Create the simulations
s1 = ss.Sim(pars1, label='Low transmission')
s2 = ss.Sim(pars2, label='High transmission')

# Run and plot the simulations
msim = ss.parallel(s1, s2)
msim.plot('sis_n_infected')
```

<img src="../assets/img/example-scenarios.png" width="100%" class="card-top-shadow text-center">
</div>
</div>
</div>

<div class="tab-pane" id="code_vaccine" role="tabpanel">
<div class="row">
<div class="col-md-12">
<p class="space-top text-left" style="padding-top:0px;">
Everything in Starsim can be customized, including diseases, demographics, and intervention. This example shows how to write custom interventions, namely a vaccine product and vaccination campaign:<br/>

```python
import starsim as ss
import matplotlib.pyplot as plt

# Define the simulation parameters
pars = dict(
    n_agents = 20_000,
    birth_rate = 20,
    death_rate = 15,
    networks = dict(
        type = 'random',
        n_contacts = 4
    ),
    diseases = dict(
        type = 'sir',
        dur_inf = 10,
        beta = 0.1,
    )
)

# Create the product: a vaccine with 50% efficacy
my_vaccine = ss.sir_vaccine(efficacy=0.5)

# Create the vaccine campaign
campaign = ss.routine_vx(
    start_year = 2015,    # Begin vaccination in 2015
    prob = 0.2,           # 20% coverage
    product = my_vaccine  # Use the MyVaccine product
)

# Now create two sims: a baseline sim and one with the intervention
sim_base = ss.Sim(pars=pars)
sim_intv = ss.Sim(pars=pars, interventions=campaign)

# Run sims in parallel
sims = ss.parallel(sim_base, sim_intv).sims
base = sims[0].results
vax = sims[1].results

# Plot
plt.figure()
plt.plot(base.yearvec, base.sir.prevalence, label='Baseline')
plt.plot(vax.yearvec, vax.sir.prevalence, label='Vaccine')
plt.axvline(x=2015, color='k', ls='--')
plt.title('Vaccine impact')
plt.xlabel('Year')
plt.ylabel('Prevalence')
plt.legend()
```

<img src="../assets/img/example-vaccine.png" width="100%" class="card-top-shadow text-center">
</div>
</div>
</div>

<div class="tab-pane" id="code_r" role="tabpanel">
<div class="row">
<div class="col-md-12">
<p class="space-top text-left" style="padding-top:0px;">
<p class="space-top" style="margin-top:0px;">Starsim can be run from R just as easily as from Python:</p>

```r
# Load Starsim
library(starsim)
load_starsim()

# Set the simulation parameters
pars <- list(
    n_agents = 10000,
    birth_rate = 20,
    death_rate = 15,
    networks = list(
        type = 'randomnet',
        n_contacts = 4
    ),
    diseases = list(
        type = 'sir',
        dur_inf = 10,
        beta = 0.1
    )
)

# Create, run, and plot the simulation
sim <- ss$Sim(pars)
sim$run()
sim$diseases$sir$plot()
```

<img src="../assets/img/example-r.png" width="100%" class="card-top-shadow text-center">
</div>
</div>
</div>

</div> <!-- end tab-content -->
</div> <!-- end profile-tabs --> 