"""
Generate figures for website
"""

import sciris as sc

#%% Basic example

# import starsim as ss

# sim = ss.Sim(diseases='sir', networks='random') # Create the sim
# sim.run() # Run the sim
# sim.plot() # Plot the results


# sc.savefig('example-basic.png')


#%% Scenarios

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


sc.savefig('example-scenarios.png')



#%% Vaccination

# import starsim as ss
# import matplotlib.pyplot as plt

# pars = dict(
#     n_agents = 20_000,
#     birth_rate = 20,
#     death_rate = 15,
#     networks = dict(
#         type = 'random',
#         n_contacts = 4
#     ),
#     diseases = dict(
#         type = 'sir',
#         dur_inf = 10,
#         beta = 0.1,
#     )
# )

# # Create the product - a vaccine with 50% efficacy
# my_vaccine = ss.sir_vaccine(efficacy=0.5)

# # Create the vaccine campaign
# campaign = ss.routine_vx(
#     start_year = 2015,    # Begin vaccination in 2015
#     prob = 0.2,           # 20% coverage
#     product = my_vaccine  # Use the MyVaccine product
# )

# # Now create two sims: a baseline sim and one with the intervention
# sim_base = ss.Sim(pars=pars)
# sim_intv = ss.Sim(pars=pars, interventions=campaign)

# # Run sims in parallel
# sims = ss.parallel(sim_base, sim_intv).sims
# base = sims[0].results
# vax = sims[1].results

# # Plot
# plt.figure()
# plt.plot(base.yearvec, base.sir.prevalence, label='Baseline')
# plt.plot(vax.yearvec, vax.sir.prevalence, label='Vaccine')
# plt.axvline(x=2015, color='k', ls='--')
# plt.title('Vaccine impact')
# plt.xlabel('Year')
# plt.ylabel('Prevalence')
# plt.legend()


# sc.savefig('example-vaccine.png')