"""
Generate fancy figure for the IDM website
"""

import numpy as np
import sciris as sc
import starsim as ss
import matplotlib.pyplot as plt

sc.options(dpi=200)
n = 5
beta_var = 0.1

# Set the parameters for the baseline simulation
pars1 = sc.objdict( # Note: can also use regular Python dictionary
    n_agents = 2_000,     # Number of agents to simulate
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

# Create the sims
plist = []
for i in range(2):
    for j in range(n):
        thisbv = (1+np.random.randn()*beta_var)
        thisp = pars1.copy(deep=True)
        if i == 0:
            label = 'Low transmission'
            beta = 0.1
        else:
            label = 'High transmission'
            beta = 0.2
        thisp.label = label
        thisp.diseases.beta = beta*thisbv
        plist.append(thisp)

slist = [ss.Sim(**p) for p in plist]

# Run and merge the simulations
msim = ss.parallel(slist)
m1 = ss.MultiSim(msim.sims[:n])
m2 = ss.MultiSim(msim.sims[n:])
m1.reduce()
m2.reduce()

# Plot the simulations
fig,axs = plt.subplots(figsize=(6,4))
m1.plot('sis_n_infected', fig=fig)
m2.plot('sis_n_infected', fig=fig)

# Configure the plot
ax = plt.gca()
ax.set_ylabel('Infections')
ax.set_title('')
sc.boxoff()
sc.commaticks()
plt.legend(fig.axes[0].lines, ['Low transmission', 'High transmission'], frameon=False)

sc.savefig('fancy-scenarios.png')