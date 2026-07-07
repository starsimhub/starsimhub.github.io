---
layout: base.njk
title: "Starsim: Agent-based disease modeling"
hero: A fast, flexible agent-based disease modeling framework
nav:
  - [What?, "#what"]
  - [Why?, "#why"]
  - [Install, "#installation"]
  - [Examples, "#examples"]
  - [Models, "#models"]
  - [Events, "#events"]
  - [Papers, "#publications"]
  - [Contact, "#contact"]
footer_left: |
  © 2024-2026 Gates Foundation

  Starsim is being developed by the [Institute for Disease Modeling](https://idmod.org), the [Burnet Institute](https://burnet.edu.au), and other collaborators.

  [Privacy & cookies](https://www.gatesfoundation.org/Privacy-and-Cookies-Notice) | [Terms of use](https://www.gatesfoundation.org/Terms-of-Use)
footer_right: |
  Starsim is distributed under the MIT License to provide others with a better understanding of our research and an opportunity to build upon it for their own work. We make no representations that the code works as intended or that we will provide support, address issues that are found, or accept pull requests. You are welcome to [create your own fork](https://github.com/starsimhub/starsim/fork) and modify the code to suit your own modeling needs as permitted under the MIT License.
---

{% section "what", "What is Starsim?" %}
Starsim is a framework for modeling the spread of diseases among agents via dynamic transmission networks. Starsim supports:

- **Co-transmission** of multiple diseases at once, capturing how they interact biologically and behaviorally
- **Non-infectious diseases**, either on their own or as factors affecting the transmission or mortality of infectious diseases
- Detailed modeling of **mother-child relationships** starting from conception, allowing investigation of infant and childhood diseases
- Multiple types of **transmission network**, including theoretical (e.g. Erdős–Rényi) and realistic (e.g. age-assortative sexual partnerships)
- Different **intervention types**, such as vaccines or treatments, and showing their impact through different delivery methods such as mass campaigns or targeted outreach
- Automated **calibration** to data, plus careful handling of random numbers to minimize variance between simulations
- Flexible **levels of detail**, including agent-based, metapopulation, and compartmental modeling
- **AI-accelerated development** via our dedicated [Starsim-AI](https://github.com/starsimhub/starsim_ai) tools (including MCP servers, skills, and plugins) that you can use with your favorite code editor

Starsim is available for both Python and R, and is fully open-source under the MIT license.
{% endsection %}

{% topbuttons %}
{% topbtn "Docs", "https://docs.starsim.org", "octicons/code" %}
{% topbtn "Tutorials", "https://docs.starsim.org/tutorials.html", "fontawesome/lightbulb-o", "tight" %}
{% topbtn "Code", "https://github.com/starsimhub/starsim", "octicons/mark-github" %}
{% topbtn "R Docs", "https://r.starsim.org", "octicons/graph" %}
{% topbtn "AI", "https://github.com/starsimhub/starsim_ai", "octicons/north-star" %}
{% endtopbuttons %}

{% cards "why", "Why Starsim?" %}
{% card "High performance", "flash" %}
Array computations and just-in-time [compilation](https://numba.pydata.org/) mean Starsim achieves C++ speeds from pure Python. Starsim runs on laptops, not supercomputers, via either R or Python.
{% endcard %}
{% card "Easy to use", "angellist" %}
Starsim's modular structure means you can reuse or adapt existing disease models, transmission networks, and demographics. Mix, match, and modify any module you want.
{% endcard %}
{% card "Global community", "globe" %}
Starsim is a community, not a product. We believe that diversity, transparency, and collaboration are essential for achieving real-world health outcomes.
{% endcard %}
{% endcards %}

{% section "installation", "Installation" %}
If you have Python, you can install Starsim:

```bash
> pip install starsim
```

Or from R:

```r
devtools::install_github("starsimhub/rstarsim")
library(starsim)
init_starsim()
```
{% endsection %}

{% examples %}
{% tab "Simple example", "assets/img/example-basic.png" %}
This is what an extremely simple Starsim simulation looks like:

1. Create a susceptible-infectious-recovered (SIR) disease model with default parameters.
2. Create a random transmission network between agents (also with default parameters).
3. Run the simulation and plot the results.

```python
import starsim as ss

sim = ss.Sim(diseases='sir', networks='random') # Create the sim
sim.run() # Run the sim
sim.plot() # Plot the results
```
{% endtab %}

{% tab "Running scenarios", "assets/img/example-scenarios.png" %}
You can easily customize model parameters, and run simulations in parallel:

1. Create a dictionary defining the parameters of the simulation.
2. Modify only those parameters you want to differ between scenarios.
3. Run the simulations in parallel, and plot the results you are interested in.

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
{% endtab %}

{% tab "Custom interventions", "assets/img/example-vaccine.png" %}
Everything in Starsim can be customized, including diseases, demographics, and interventions. This example shows how to write custom interventions, namely a vaccine product and vaccination campaign:

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
{% endtab %}

{% tab "R example", "assets/img/example-r.png" %}
Starsim can be run from R just as easily as from Python:

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
{% endtab %}
{% endexamples %}

{% section "models", "Models" %}
The Starsim ecosystem contains many different disease-specific models, for example:

<img src="assets/img/starsim-spokes.png" width="100%" class="card-top-shadow text-center" style="margin-bottom: 25px;">

Key models include [STIsim](https://stisim.org) (which includes HIVsim), [HPVsim](https://hpvsim.org), [FPsim](https://fpsim.org), [TBsim](https://starsim.org/tbsim), [Covasim](https://stisim.org), and [Gavi Outbreaks](https://www.medrxiv.org/content/10.1101/2024.06.02.24308241v1.full). A more detailed list of Starsim models is available [here](https://docs.starsim.org/user_guide/intro_models.html).
{% endsection %}

{% section "events", "Events" %}
{% eventlist "Upcoming events" %}
{% event "Talk @ SciPy 2026", "Jul. 13-19, 2026: Minneapolis, USA" %}
A talk on Starsim-AI performance will be given at the [SciPy 2026](https://www.scipy2026.scipy.org/) (Scientific Python) conference.
{% endevent %}
{% endeventlist %}

{% eventlist "Past events" %}
{% event "Talk @ EPIDEMICS 10", "Nov. 30-Dec. 3, 2025: San Diego, USA" %}
A talk on Starsim was given at the [EPIDEMICS 10](https://www.elsevier.com/events/conferences/all/international-conference-on-infectious-disease-dynamics) conference (10th International Conference on Infectious Disease Dynamics). Several other talks and posters using Starsim were also presented. Slides are available [here](https://docs.google.com/presentation/d/1-gwTMl1OElZNIYcLfpCemfkuo5VhU_hOWvt6YfH49Q8/edit?usp=sharing).
{% endevent %}
{% event "Talk @ MIDAS 2024", "Nov. 18, 2024: Silver Spring, USA" %}
An introductory talk on Starsim was given at the 2024 [MIDAS Conference](https://midasnetwork.us/midas-2024/). Slides are available [here](https://docs.google.com/presentation/d/160gNQ89wNaZf9XTjhj5-H3TMB--vX5FnnnqQz2QgdL8/edit).
{% endevent %}
{% event "Talk @ IDM Conference 2024", "Nov. 8, 2024: Bangkok, Thailand" %}
A talk introducing Starsim was given at the 2024 [Infectious Disease Modelling Conference](https://idmconference.net). Slides are available [here](https://docs.google.com/presentation/d/1bVG_HJxoT07UG6YqR5vaH8jDtt2VsgsSOHkuEpVvww0/edit).
{% endevent %}
{% event "Starsim Learning Day @ IDM Symposium", "Oct. 3, 2024: Seattle, USA" %}
We conducted a full-day information and training session on Starsim as part of the 2024 IDM Symposium. Course content is available [here](https://learningday2024.starsim.org).
{% endevent %}
{% event "Poster @ AIDS 2024", "Jul. 25, 2024: Munich, Germany" %}
A poster on using Starsim to model HIV-STI coinfection was presented at the [AIDS 2024](https://www.iasociety.org/conferences/aids2024) conference. The poster is available [here](https://docs.google.com/presentation/d/1ObX11ExrtueXWAsPqPhV01SRoRLXDr5dB2AtKKhcZuk/edit).
{% endevent %}
{% event "Starsim Launch @ SciPy 2024", "Jul. 10, 2024: Tacoma, USA" %}
Starsim v1.0 was officially launched at the [SciPy 2024](https://www.scipy2024.scipy.org/) conference. The slides from the talk are available [here](https://docs.google.com/presentation/d/13kWAiYRiPvlWXDitE5UVNlsrxOMPjG1sSPd2gsMqoQU/edit).
{% endevent %}
{% event "Agent-Based Modelling Training", "Apr. 8-19, 2024: Nairobi, Kenya" %}
In collaboration with the [African Population & Health Research Center](https://aphrc.org/) (APHRC) and the [Center for Epidemiological Modelling and Analysis](https://cema.africa/) (CEMA), we conducted a workshop on agent-based modeling, including Starsim. The brochure is available [here](https://drive.google.com/file/d/1Ya1S7RvRI3U_EQscRWpmpF7cILTELgAC/view); other materials are available upon request.
{% endevent %}
{% endeventlist %}
{% endsection %}

{% section "publications", "Publications", "wide" %}
Starsim has not yet been published. But if you want to cite it, please use:

{% cite %}
Kerr CC, Stuart RM, Abeysuriya R, Cohen JA, Sanz-Leon P, Klein DJ (2026). _Starsim: A fast, flexible framework for agent-based modeling of health and disease._ In preparation.
{% endcite %}

However, several other papers have been published that have used Starsim:

{% cite %}
Stuart R, Theopold N, Miall N, Kobayashi E, Vernam S, Taskin T, Dull PM (2026). _[The role of HPV single-dose vaccination in expanding access in GAVI-supported countries during a period of supply constraints.](https://www.sciencedirect.com/science/article/abs/pii/S0264410X25014859)_ Vaccine, 75: 128187.
{% endcite %}

{% cite %}
Stuart RM, Newman LM, Manguro G, Dziva Chikwari C, Marks M, Peters RPH, Klein D, Snyder L, Kerr C, Rao DW (2026). _[Reduction in overtreatment of gonorrhoea and chlamydia through point-of-care testing compared with syndromic management for vaginal discharge: A modelling study for Zimbabwe.](https://sti.bmj.com/content/early/2026/02/05/sextrans-2025-056646)_ Sexually Transmitted Infections.
{% endcite %}

{% cite %}
Sturman F, Swallow B, Kerr C, Stuart RM, Panovska-Griffiths J (2025). _[Can pruning improve agent-based models' calibration? An application to HPVsim.](https://www.sciencedirect.com/science/article/pii/S0022519325000967)_ Journal of Theoretical Biology, 611: 112130.
{% endcite %}

{% cite %}
Stuart RM, Cohen JA, Kerr CC, Mathur P, National Disease Modelling Consortium of India, Abeysuriya RG, Zimmermann M, Rao DW, Boudreau MC, Lee S, Yang L, Klein DJ (2024). _[HPVsim: An agent-based model of HPV transmission and cervical disease.](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012181)_ PLOS Computational Biology, 20(7): e1012181.
{% endcite %}

{% cite %}
Klein DJ, Abeysuriya RG, Stuart RM, Kerr CC (2024). _[Noise-free comparison of stochastic agent-based simulations using common random numbers.](https://arxiv.org/abs/2409.02086)_ arXiv:2409.02086.
{% endcite %}

{% cite %}
Kerr CC, Stuart RM, Mistry D, Abeysuriya RG, Cohen JA, George L, Jastrzebski M, Famulare M, Wenger E, Klein DJ (2022). _[Python vs. the pandemic: A case study in high-stakes software development.](https://proceedings.scipy.org/articles/majora-212e5952-00e)_ SciPy Proceedings.
{% endcite %}
{% endsection %}

{% section "contact", "Contact", "wide" %}
<p class="text-center">Have questions? Want to collaborate? We'd love to hear from you!</p>

<ul id="icons-links" class="text-center" style="margin-top:10px;">
  <a href="mailto:info@starsim.org"><button class="btn btn-primary" style="font-weight:normal;"> info@starsim.org<div class="ripple-container"></div></button></a>
</ul>

<img src="assets/img/starsim-team.png" width="100%" class="text-center">
{% endsection %}
