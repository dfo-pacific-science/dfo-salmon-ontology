C S A S

S C C S

Canadian Science Advisory Secretariat

Secrétariat canadien de consultation scientifique

Research Document  2009/059

Document de recherche  2009/059

Evaluation of Benchmarks for
Conservation Units in Canada's Wild
Salmon Policy: Technical
Documentation

Évaluation des points de repère servant
à évaluer les unités de conservation
définis dans la Politique concernant le
saumon sauvage du Canada

Carrie A. Holt

Fisheries and Oceans Canada
Pacific Biological Station
3190 Hammond Bay Road
Nanaimo, BC  V9T 6N7

in

This  series  documents  the  scientific  basis  for  the
evaluation of aquatic resources and ecosystems in
Canada.    As  such,  it  addresses  the  issues  of  the
the
frames
day
documents
intended  as
it  contains  are  not
definitive  statements  on  the  subjects  addressed
but
reports  on  ongoing
investigations.

rather  as  progress

required  and

time

the

La  présente  série  documente  les  fondements
scientifiques  des  évaluations  des  ressources  et
des  écosystèmes  aquatiques  du  Canada.    Elle
les
traite  des  problèmes  courants  selon
échéanciers  dictés.
  Les  documents  qu’elle
contient  ne  doivent  pas  être  considérés  comme
des énoncés définitifs sur les sujets traités, mais
plutôt  comme  des  rapports  d’étape  sur  les
études en cours.

Research  documents  are  produced  in  the  official
language  in  which  they  are  provided  to  the
Secretariat.

Les  documents  de  recherche  sont  publiés  dans
la  langue  officielle  utilisée  dans  le  manuscrit
envoyé au Secrétariat.

This document is available on the Internet at:

Ce document est disponible sur l’Internet à:

http://www.dfo-mpo.gc.ca/csas/

ISSN 1499-3848 (Printed / Imprimé)
ISSN 1919-5044 (Online / En ligne)
© Her Majesty the Queen in Right of Canada, 2009
© Sa Majesté la Reine du Chef du Canada, 2009

TABLE OF CONTENTS

1.

2.1

1.1
1.2
1.3

Introduction................................................................................................................. 1
Uncertainties ....................................................................................................... 2
Candidate lower benchmarks.............................................................................. 3
Performance criteria............................................................................................ 4
2.  Methods....................................................................................................................... 6
Simulation models to evaluate lower benchmarks.............................................. 6
Population dynamics sub-model ................................................................. 9
2.1.1
2.1.2
Observation sub-model ............................................................................. 13
2.1.3  Management sub-model............................................................................ 14
Performance module ................................................................................. 15
2.1.4
Differences between Models 1 and 2........................................................ 15
2.1.5
2.2  Model parameterization .................................................................................... 15
3.  Results....................................................................................................................... 16
3.1  Model 1: Probability of extirpation over the long term .................................... 16
Lower benchmarks on spawner abundances............................................. 16
Lower benchmarks on fishing mortality ................................................... 25
3.2  Model 2: Probability of recovery to SMSY in one (or three) generations........... 32
Lower benchmarks on spawner abundances............................................. 32
Lower benchmarks on fishing mortality ................................................... 40
4.  Recommendations..................................................................................................... 48
5.  Literature cited .......................................................................................................... 49

3.1.1
3.1.2

3.2.1
3.2.2

iii

iv

TABLE OF FIGURES

Figure 1. Simulation modelling framework used to evaluate the probability of extirpation

over the long term (a) and probability of recovery to SMSY (b, next page) for lower
benchmarks on spawner abundances. Sy is the spawner abundance in brood year y, R
is recruitment, t is year of recruitment, R0 is observed recruitment, h is target harvest
rate derived from target spawner abundances, Starget, and observed recruitment, and
h' is the realized harvest rate (i.e., harvest with outcome uncertainty). Note, panel (b)
does not include an "Observation sub-model" because for that model evaluated
probability of recovery under a scenario of no directed fishing, and so observations
of abundance were not required.................................................................................. 8

Figure 2. Probabilities of extirpation over the long term (100 years) for simulated

populations of Pacific salmon under a constant escapement policy equal to the lower
benchmarks derived from spawner abundances at various percentages of RMSY
(black lines) over a gradient in equilibrium stock sizes (X-axis).  Three other lower
benchmarks are shown: spawner abundances, S, at 50% of RMAX (red line), 40% of
SMSY (blue line), and spawner abundance resulting in recovery to SMSY in one
generation without fishing under equilibrium conditions, Sgen (green line). ............ 17

Figure 3. Probabilities of extirpation, p, over the long term (100 years) for unproductive

(mean Ricker "a" parameter = 0.5, or 1.7 recruits/spawner at low spawner
abundances) (a), moderately productive (mean Ricker "a" parameter = 1.5, or 4.5
recruits/spawner at low spawner abundances) (b), and highly productive (mean
Ricker "a" parameter = 2.0, or 7.4 recruits/spawner at low spawner abundances) (c)
simulated populations of Pacific salmon under a constant escapement policy equal to
the lower benchmarks derived from spawner abundances at various percentages of
RMSY (black lines, ranging from 10% (top line) to 90% (bottom line)) over a gradient
in equilibrium stock sizes (X-axis). Three other lower benchmarks are shown, as
described in the caption to Fig.2: S at 50% of RMAX (red line), 40% of SMSY (blue
line), and Sgen (green line). ........................................................................................ 18

Figure 4. Probabilities of extirpation over the long term (10  0 years) for simulated

populations of Pacific salmon under a constant escapement policy equal to the lower
benchmark derived from Sgen (spawner abundances that will result in recovery to
SMSY in one generation under equilibrium conditions) and four assumptions about
the trends in stock productivity (Ricker "a" parameter): no trend (thick solid line);
linear increase over time (thin solid line); linear decline over time (dashed line); and
cyclic pattern (dotted line), over a gradient in equilibrium stock sizes (X-axis)...... 19

Figure 5. Probabilities of extirpation over the long term (100 years) for simulated

populations of Pacific salmon under a constant escapement policy equal to the lower
benchmark derived from Sgen (spawner abundances that will result in recovery to
SMSY in one generation under equilibrium conditions) and four assumptions about
the stock-recruitment model: Ricker model (thin solid line),   Ricker model with
autocorrelation and depensatory mortality at low spawner abundances (thick solid
line), Beverton-Holt model (dashed line), and Larkin model (dotted line), over a
gradient in equilibrium stock sizes (X-axis). ............................................................ 20

Figure 6. Probabilities of extirpation over the long term (100 years) for simulated

populations of Pacific salmon under a constant escapement policy equal to the lower

v

benchmark derived from Sgen (spawner abundances that will result in recovery to
SMSY in one generation under equilibrium conditions) and three assumptions about
the spawner abundance below which depensatory mortality occurs: 500 fish (thick
solid line); 1000 fish (thin solid line); 7000 (dashed line), over a gradient in
equilibrium stock sizes (X-axis). .............................................................................. 21

Figure 7. Probabilities of extirpation over the long term (100 years) for simulated

populations of Pacific salmon under a constant escapement policy equal to the lower
benchmark derived from Sgen (spawner abundances that will result in recovery to
SMSY in one generation under equilibrium conditions) and two assumptions about the
magnitude of observation errors: standard deviation between actual and observed
abundance = 0.19 (thin solid line) and 0.38 (thick solid line), over a gradient in
equilibrium stock sizes (X-axis). .............................................................................. 22

Figure 8. Probabilities of extirpation over the long term (100 years) for simulated

populations of Pacific salmon under a constant escapement policy equal to the lower
benchmark derived from Sgen (spawner abundances that will result in recovery to
SMSY in one generation under equilibrium conditions) and three assumptions about
the number of years of historical data used to estimate RMSY when deriving the lower
benchmark (corresponding to the magnitude of assessment uncertainty): 30 years
(low assessment uncertainty, thin solid line), 20 years (moderate assessment
uncertainty, thick solid line), and 15 years (high assessment uncertainty, dashed
line), over a gradient in equilibrium stock sizes (X-axis)......................................... 23

Figure 9. Probabilities of extirpation over the long term (100 years) for simulated

populations of Pacific salmon under a constant escapement policy equal to the lower
benchmark derived from Sgen (spawner abundances that will result in recovery to
SMSY in one generation under equilibrium conditions) and two assumptions about the
magnitude of outcome uncertainty: standard deviation between realized harvest rates
and targets = 0.097 (thin solid line) and 0.19 (thick solid line), over a gradient in
equilibrium stock sizes (X-axis). .............................................................................. 24

Figure 10. Probabilities of extirpation over the long term (100 years) for simulated

populations of Pacific salmon under a constant escapement policy equal to the lower
benchmark derived from Sgen (spawner abundances that will result in recovery to
SMSY in one generation under equilibrium conditions) and three assumptions about
the lower limit on harvest rate, ht, (due to non-target fishing mortality, e.g., test-
fishery and by-catch): low ht = 0.02 (thin solid line), moderate ht = 0.1 (thick solid
line), and high ht = 0.2 (dashed line), over a gradient in equilibrium stock sizes (X-
axis)........................................................................................................................... 25

Figure 11. Probabilities of extirpation over the long term (100 years) for simulated

populations of Pacific salmon under a constant fishing mortality rate policy equal to
the lower benchmarks derived from various percentages of FMSY (black lines) over a
gradient in equilibrium stock sizes (X-axis).  Three other lower benchmarks are
shown: FMSY (red line, equivalent to 100% FMSY), the maximum
loge(recruits/spawner) at low spawner abundances (i.e., Ricker "a" parameter)
(FMAX, blue line), and the median loge(recruits/spawner) (FMED, green line). ......... 26
Figure 12. Probabilities of extirpation, p, over the long term (100 years) for unproductive

(mean Ricker "a" parameter = 0.5, or 1.7 recruits/spawner at low spawner
abundances) (a), moderately productive (mean Ricker "a" parameter = 1.5, or 4.5

vi

recruits/spawner at low spawner abundances) (b), and highly productive (mean
Ricker "a" parameter = 2.0, or 7.4 recruits/spawner at low spawner abundances) (c)
simulated populations of Pacific salmon under a constant escapement policy equal to
the lower benchmarks derived from various percentages of FMSY (black lines,
ranging from 150% (top line) to 50% (bottom line)) over a gradient in equilibrium
stock sizes (X-axis). Three other lower benchmarks are shown, as described in the
caption to Fig.11: FMSY (red line), FMAX (blue line), and FMED (green line). ........... 27

Figure 13. Probabilities of extirpation over the long term (100 years) for simulated

populations of Pacific salmon under a constant fishing mortality rate policy equal to
the lower benchmarks, FMSY, and four assumptions about the trends in stock
productivity (Ricker "a" parameter): no trend (thick solid line); linear increase over
time (thin solid line); linear decline over time (dashed line); and cyclic pattern
(dotted line), over a gradient in equilibrium stock sizes (X-axis)............................. 28

Figure 14. Probabilities of extirpation over the long term (100 years) for simulated

populations of Pacific salmon under a constant fishing mortality rate policy equal to
the lower benchmarks, FMSY, and four assumptions about the stock-recruitment
model: Ricker model (thin solid line),   Ricker model with autocorrelation and
depensatory mortality at low spawner abundances (thick solid line), Beverton-Holt
model (dashed line), and Larkin model (dotted line), over a gradient in equilibrium
stock sizes (X-axis). Lines for the Ricker, Beverton-Holt, and Larkin models lie
almost on top of each other near the bottom X-axis. ................................................ 29

Figure 15. Probabilities of extirpation over the long term (100 years) for simulated

populations of Pacific salmon under a constant fishing mortality rate policy equal to
the lower benchmarks, FMSY, and three assumptions about the spawner abundance
below which depensatory mortality occurs: 500 fish (thick solid line); 1000 fish
(thin solid line); 7000 (dashed line), over a gradient in equilibrium stock sizes (X-
axis)........................................................................................................................... 30

Figure 16. Probabilities of extirpation over the long term (100 years) for simulated

populations of Pacific salmon under a constant fishing mortality rate policy equal to
the lower benchmarks, FMSY, and three assumptions about the number of years of
historical data used to estimate FMSY when deriving the lower benchmark
(corresponding to the magnitude of assessment uncertainty): 30 years (thin solid
line), 20 years (thick solid line), and 15 years (dashed line), over a gradient in
equilibrium stock sizes (X-axis). .............................................................................. 31

Figure 17. Probabilities of extirpation over the long term (100 years) for simulated

populations of Pacific salmon under a constant fishing mortality rate policy equal to
the lower benchmarks, FMSY, and two assumptions about the magnitude of outcome
uncertainty: standard deviation between realized harvest rates and targets = 0.097
(thin solid line) and 0.19 (thick solid line), over a gradient in equilibrium stock sizes
(X-axis). .................................................................................................................... 32
Figure 18. Probabilities of recovery over one (a) and three (b) generation(s) for simulated
populations of Pacific salmon from lower benchmark on spawner abundances listed
on the X-axis, in the absence of commercial and recreational fishing. Lower
benchmarks derived from spawner abundances at various percentages of RMSY
(black solid circles) are compared with three other lower benchmarks: spawner
abundances at 50% of RMAX (red circle), 40% of SMSY (blue circle), and spawner

vii

abundance resulting in recovery to SMSY in one generation without fishing under
equilibrium conditions, Sgen (green circle)................................................................ 33

Figure 19. Probabilities of recovery over one generation for unproductive (hollow grey
and coloured circles), moderately productive (solid grey and coloured circles), and
highly productive (solid black and coloured circles with black outline) simulated
populations of Pacific salmon from lower benchmarks on spawner abundances listed
on the X-axis in the absence of commercial and recreational fishing. Lower
benchmarks are the same as described in the caption to Fig. 18. ............................. 34

Figure 20. Probabilities of recovery over one generation for simulated populations of
Pacific salmon that have constant productivity (Ricker "a" parameter) over time
(hollow grey and coloured circles), linearly increasing productivity (solid grey and
coloured circles), linearly declining productivity (solid black and coloured circles
with black outline), and cyclic patterns in productivity (black and coloured
asterisks), from lower benchmarks on spawner abundances listed on the X-axis in
the absence of commercial and recreational fishing. Note, points are almost
coincident because magnitudes of the changes in productivity are small over one
generation. Lower benchmarks are the same as described in the caption to Fig. 18.35

Figure 21. Probabilities of recovery over one generation for simulated populations of
Pacific salmon that recruit according to a Ricker model (solid grey and coloured
circles), a Ricker model with autocorrelation and depensation (solid black and
coloured circles with black outline), a Beverton-Holt model (hollow grey and
coloured circles), and a Larkin model (black and coloured asterisks), from lower
benchmarks on spawner abundances listed on the X-axis in the absence of
commercial and recreational fishing. Lower benchmarks are the same as described
in the caption to Fig. 18. ........................................................................................... 36

Figure 22. Probabilities of recovery over one generation for simulated populations of
Pacific salmon that recruit according to a Ricker model with autocorrelation and
depensatory mortality at low spawner abundances, i.e., below 500 spawners, 1000
spawners, and 7000 spawners, from lower benchmarks on spawner abundances
listed on the X-axis, in the absence of commercial and recreational fishing. Note,
points for different threshold levels below which depensation occurs are exactly
coincident (i.e., the probability of recovery is insensitive to threshold level).  Lower
benchmarks are the same as described in the caption to Fig. 18. ............................. 37

Figure 23. Probabilities of recovery over one generation for simulated populations of

Pacific salmon from lower benchmarks on spawner abundances listed on the X-axis,
derived from historical time series of length 15 years (hollow grey and coloured
circles), 20 years (solid grey and coloured circles), and 30 years (solid black and
coloured circles with black outline), in the absence of commercial and recreational
fishing. Lower benchmarks are the same as described in the caption to Fig. 18...... 38

Figure 24. Probabilities of recovery over one generation for simulated populations of

Pacific salmon with low outcome uncertainties (solid grey and coloured circles) and
high outcome uncertainties (solid black and coloured circles with black outline),
from lower benchmarks on spawner abundances listed on the X-axis, in the absence
of commercial and recreational fishing. Lower benchmarks are the same as
described in the caption to Fig. 18. ........................................................................... 39

viii

Figure 25. Probabilities of recovery over one generation for simulated populations of

Pacific salmon from lower benchmarks on spawner abundances listed on the X-axis,
in the absence of commercial and recreational fishing but with non-targeted harvest
rate (e.g., from a test fishery and by-catch) of ht = 0.02 (hollow grey and coloured
circles), ht = 0.1 (solid grey and coloured circles) and ht = 0.2 ((solid black and
coloured circles with black outline). Lower benchmarks are the same as described in
the caption to Fig. 18. ............................................................................................... 40
Figure 26. Probabilities of recovery over one (a) and three (b) generation(s) for simulated
populations of Pacific salmon managed according to the lower benchmark on fishing
mortality listed on the X-axis, in the absence of commercial and recreational fishing.
Lower benchmarks derived from fishing mortality at various percentages of FMSY
(black solid circles) are compared with three other lower benchmarks: FMSY (red
circle), maximum loge(R/S) at low spawner abundances, FMAX (blue circle), and
median loge(R/S), FMED (green circle). ..................................................................... 41

Figure 27. Probabilities of recovery over one generation for unproductive (hollow grey
and coloured circles), moderately productive (solid grey and coloured circles), and
highly productive (solid black and coloured circles with black outline) simulated
populations of Pacific salmon managed according to the lower benchmarks on
fishing mortality listed on the X-axis, in the absence of commercial and recreational
fishing. Lower benchmarks are the same as described in the caption to Fig. 26...... 42

Figure 28. Probabilities of recovery over one generation for simulated populations of
Pacific salmon that have constant productivity (Ricker "a" parameter) over time
(hollow grey and coloured circles), linearly increasing productivity (solid grey and
coloured circles), linearly declining productivity (solid black and coloured circles
with black outline), and cyclic patterns in productivity (black and coloured
asterisks), managed according to the lower benchmarks on fishing mortality listed
on the X-axis in the absence of commercial and recreational fishing. Note, points are
almost coincident because magnitude of the changes in productivity are small over
one generation. Lower benchmarks are the same as described in the caption to Fig.
26............................................................................................................................... 43

Figure 29. Probabilities of recovery over one generation for simulated populations of
Pacific salmon that recruit according to a Ricker model (solid grey and coloured
circles), a Ricker model with autocorrelation and depensation (solid black and
coloured circles with black outline), a Beverton-Holt model (hollow grey and
coloured circles), and a Larkin model (black and coloured asterisks), managed
according to the lower benchmarks on fishing mortality listed on the X-axis in the
absence of commercial and recreational fishing. Lower benchmarks are the same as
described in the caption to Fig. 26. ........................................................................... 44

Figure 30. Probabilities of recovery over one generation for simulated populations of
Pacific salmon that recruit according to a Ricker model with autocorrelation and
depensatory mortality at low spawner abundances, i.e., below 500 spawners, 1000
spawners, and 7000 spawners, managed according to the lower benchmarks on
fishing mortality listed on the X-axis, in the absence of commercial and recreational
fishing. Note, points for different threshold levels below which depensation occurs
are exactly coincident (i.e., the probability of recovery is insensitive to threshold
level).  Lower benchmarks are the same as described in the caption to Fig. 26....... 45

ix

Figure 31. Probabilities of recovery over one generation for simulated populations of
Pacific salmon managed according to the lower benchmarks on fishing mortality
listed on the X-axis, derived from historical time series of length 15 years (hollow
grey and coloured circles), 20 years (solid grey and coloured circles), and 30 years
(solid black and coloured circles with black outline), in the absence of commercial
and recreational fishing. Lower benchmarks are the same as described in the caption
to Fig. 26. .................................................................................................................. 46

Figure 32. Probabilities of recovery over one generation for simulated populations of

Pacific salmon with low outcome uncertainties (solid grey and coloured circles) and
high outcome uncertainties (solid black and coloured circles with black outline),
managed according to the lower benchmarks on fishing mortality listed on the X-
axis, in the absence of commercial and recreational fishing. Lower benchmarks are
the same as described in the caption to Fig. 26......................................................... 47

x

Correct citation for this publication:

Holt, C. A.  2009. Evaluation of benchmarks for conservation units in Canada’s Wild

Salmon Policy: Technical Documentation.  DFO Can. Sci. Advis. Sec. Res. Doc.
2009/059. x + 50 p.

ABSTRACT

Canada's Wild Salmon Policy  requires that quantifiable metrics of biological status and
benchmarks along those metrics that delineate Red, Amber, and Green zones of status be
established  for  all  Conservation  Units.  Although  candidate  benchmarks  have  been
identified  from  the  scientific  literature  and previous  management  experience,  they  have
not been evaluated in terms of their ability to meet the goals of the Wild Salmon Policy.
Using a simulation model, we evaluated lower benchmarks on two classes of indicators
(abundances and fishing mortality relative to productivity) on two performance metrics:
the  probability  of  extirpation  over  the  long  term  and  the  probability  of  recovery  to  a
target. This technical document provides the methodology and results for those analyses
and  is  a  companion  document  to  the  overall  synthesis  paper  "Indicators  of  Status  and
Benchmarks for Conservation Units in Canada's Wild Salmon Policy" (Holt et al. 2009).
We  considered  the  "worst-case"  management  scenario,  with  management  decisions
corresponding  to  CUs  being  depleted  to  the  lower  benchmark  each  year.  Although
unrealistic, this assumption provides an upper limit on the probability of extirpation and
lower  limit  on  the  probability  of  recovery.  We  found  that  for  metrics  of  spawner
abundances, the lower benchmark, spawner abundance that will result in recovery to SMSY
(spawner  abundance  at  maximum  sustained  yield)  in  one  generation  under  equilibrium
conditions  (Sgen),  was  associated  with  a  relatively  low  probability  of  extirpation
(probability  <25%)  over  100  years  (for  populations  with  equilibrium  abundances  >  15
000  spawners)  and  high  probability  of  recovery  to  SMSY  within  three  generations
(probability  >75%)  when  uncertainties  in  all  major  components  of  the  fishery  system
were accounted for. Furthermore, the probability of extirpation for Sgen was more robust
to  variability  in  stock  productivity  compared  with  benchmarks  calculated  from
proportions of SMSY. For metrics of fishing mortality, the lower benchmark FMSY (fishing
mortality at maximum sustained yield) was associated with a relatively low probability of
extirpation  (probability  <25%)  over  100  years  for  populations  with  equilibrium
abundances  >  30  000  spawners,  and  high  probability  of  recovery  to  SMSY  within  three
generations  (probability  >75%),  and  its  performance  was  more  robust  to  variability  in
stock productivity than other benchmarks on fishing mortality derived from the scientific
literature.  Based  on  those  results  and  a  risk  classification  scheme  developed  in  DFO's
Fishery Decision-Making Framework Incorporating the Precautionary Approach (2009),
we  suggest  deriving  lower  benchmarks  on  spawner  abundances  from  Sgen  and  lower
benchmarks  on  fishing  mortality  from  FMSY.  Further  work  will  be  required  to  identify
specific  risk  tolerances  of  stakeholders  in  order  to  better  inform  the  choice  of  lower
benchmarks.

xi

RÉSUMÉ

La  Politique  concernant  le  saumon  sauvage  du  Canada  exige  que  des  paramètres
quantifiables pour évaluer l’état biologique ainsi que des points de repère pour délimiter
les  trois  zones  d’état  (rouge,  ambre  et  vert)  soient  établis  pour  toutes  les  unités  de
conservation.  Bien  que  des  points  de  repère  probables  aient  été  déterminés  à  partir  de
l’examen de la documentation scientifique et d’une expérience de gestion précédente, ils
n’ont pas fait l’objet d’une évaluation sur le plan de leur capacité à atteindre les objectifs
visés  par  la  Politique  concernant  le  saumon  sauvage.  Au  moyen  d’un  modèle  de
simulation,  on  a  évalué  les  points  de  repère  inférieurs  de  deux  catégories  d’indicateurs
(l’abondance  et  la  mortalité  par  pêche  relativement  à  la  productivité)  pour  deux
paramètres liés à la performance : la probabilité de disparition d’un endroit donné à long
terme  et  la  probabilité  de  rétablissement  correspondant  à  un  objectif.  Ce  document
technique  présente  la  méthode  et  les  résultats  de  ces  analyses  et  est  un  document
d’accompagnement  à  l’ouvrage  de  synthèse  générale  intitulé « Indicators  of  Status  and
Benchmarks  for  Conservation  Units  in  Canada's  Wild  Salmon  Policy »  (Holt  et  coll.,
2009).  On  a  envisagé  le  pire  scénario  de  gestion  avec  des  décisions  de  gestion
correspondant  aux  unités  de  conservation  étant  appauvries  au  point  de  repère  inférieur
chaque  année.  Bien  qu’elle  soit  peu  réaliste,  cette  hypothèse  procure  un  seuil  supérieur
relatif  à  la  probabilité  de  disparition  et  un  seuil  inférieur  relatif  à  la  probabilité  de
rétablissement. En ce qui concerne les paramètres de l’abondance de reproducteurs, on a
découvert que le point de repère le plus bas, l’abondance de reproducteurs qui se traduira
par  le  rétablissement  à  SMSY  (abondance  de  reproducteurs  au  rendement  maximal
soutenable) en une génération dans des conditions d’équilibre (Sgen), était associé à une
probabilité  relativement  faible  de  disparition  (probabilité < 25 %)  sur  100 ans  (pour  les
populations  affichant  un  niveau  d’abondance  équilibré  >  15 000  reproducteurs)  et  une
forte  probabilité  de  rétablissement  à  SMSY  en  trois  générations  (probabilité > 75 %),
lorsqu’on  tenait  compte  des  incertitudes  liées  à  toutes  les  composantes  principales  du
système de pêche. De plus, la probabilité de disparition pour Sgen était davantage liée à
la  variabilité  de  productivité  du  stock  comparativement  aux  points  de  repère  calculés  à
partir des proportions de SMSY. Quant aux paramètres relatifs à la mortalité par pêche, le
point de repère inférieur FMSY (mortalité par pêche au rendement maximal soutenable)
était associé à une probabilité relativement faible de disparition (probabilité < 25 %) sur
plus de 100 ans pour des populations affichant un niveau d’abondance équilibré > 30 000
reproducteurs,  et  une  forte  probabilité  de  rétablissement  à  SMSY  en  trois  générations
(probabilité > 75 %), et sa performance était davantage liée à la variabilité de productivité
du  stock  que  les  autres  points  de  repère  relatifs  à  la  mortalité  par  pêche  issus  des
documents scientifiques. À partir de ces résultats et d’un schéma de classification fondée
sur le risque élaboré en vertu du cadre décisionnel pour les pêches intégrant l’approche de
précaution  (2009)  du  MPO,  on  suggère  de  calculer  les  points  de  repère  inférieurs  pour
l’abondance  de  reproducteurs  à  partir  de  Sgen  et  les  points  de  repère  inférieurs  pour  la
mortalité par pêche à partir de FMSY. Des études supplémentaires seront nécessaires afin
de déterminer la tolérance particulière à l’égard des risques des intervenants dans le but
de mieux définir le choix des points de repère inférieurs.

xii

1.

INTRODUCTION

Numerous  lower  benchmarks  have  been  proposed  to  assess  status  of  Conservation
Units  for  the  Wild  Salmon  Policy,  but  those  benchmarks  have  not  been  evaluated  in  a
consistent, probabilistic way (i.e., incorporating uncertainties). To evaluate the performance
of  lower  benchmarks,  we  adapted  the  nine  steps  identified  in  the  idealized  assessment
framework for identifying benchmarks (Table 1). Specifically, using a simulation modelling
approach, we compared the performances of benchmarks on two criteria derived from the
Wild  Salmon  Policy,  the  probability  of  extirpation  over  the  long  term  and  the  probability
that the CU will rebuild to levels where harvest can provide, on an average annual basis, the
maximum  annual  catch,  given  existing  environmental  conditions  (i.e.,  probability  of
recovery to SMSY). We did this by developing an operating model, which is a mathematical
abstraction  of  the  true  fisheries  system  accounting  for  all  known  uncertainties.  In  the
operating  model,  we  assumed  the  most  aggressive  harvest  strategy  possible  that  still
recognized  the  lower  benchmark  (i.e.,  that  was  associated  with  the  highest  possible
probability of extirpation and lowest possible probability of recovery). In other words, the
harvest  strategy  was  associated  with  the  worst-case  performance.  For  the  benchmarks  on
fishing mortality, that harvest strategy was a constant fishing mortality policy equivalent to
the  lower  benchmark  (see  Section  1.3  for  more  details).  For  benchmarks  on  spawner
abundances, the harvest strategy was a constant escapement policy equivalent to the lower
benchmark, with one exception when evaluating the probability of recovery to a target (as
described  in  Section  1.3).  All  other  possible  harvest  strategies  that  recognize  those  lower
benchmarks but adapt escapement or fishing mortality according to observed abundances or
catches above that benchmark, will result in improved performance (a lower probability of
extirpation  and  higher  probability  of  recovery).  Although  these  harvest  strategies  may  be
unrealistic, they demonstrate the long-term properties of the benchmarks under pessimistic
assumptions  about  the  ability  of  fishery  management  to  restrict  effort.  Therefore,  the
simulation  model  results  represent  a  lower  limit  on  possible  performance.  Evaluating  all
possible harvest strategies in a simulation model is beyond the scope of this report, but will
be a necessary step before implementing those rules in the fishery.

1

Table 1 Steps for determining a precautionary lower benchmark in an idealized assessment
framework  for  an  example  reference  frame  (biological  yield)  and  goal
(maintenance  of  maximum  yield).  The  providers  are  either  Fisheries
Management, FM, or Science

Step
1. Reference frame

Provider
FM (WSP)

Input
Policy specification

2. Goal or endpoint

FM (WSP)

Policy specification

3. Time frame to achieve
goal or endpoint
4. Fishery management
actions
5. Model relating current
state to a future state
6. Deterministic upper
benchmark
7. Deterministic lower
benchmark
8. Incorporate uncertainty
into lower benchmark

FM

FM

Science

Science

Science

Science

9. Choice of risk
tolerance

FM

1.1  Uncertainties

Unspecified

Unspecified

Production model

WSP specification

Outputs of steps 2, 3, 4,
&  6
Quantification of known
uncertainties including
model choice, parameter
estimation, current state,
future state of modifiers
(environment), and
outcome/implementation
uncertainty
Output of step 8

Output
Specified as biological
production (i.e., yield)
Maintenance of maximum
yield adjusted for current
environmental conditions
Number of years

Actions such as 10% total
exploitation rate
Ricker stock-recruitment
model
Example, MSY

Lower benchmark

Function relating possible
values of the lower
benchmark to the
probability of achieving
the goal within the time
allowed

Selected lower benchmark

By  incorporating  uncertainties  in  all  major  components  of  the  fisheries  system
(population dynamics, observations of abundances, and management) the operating model
provides a basis for evaluating lower benchmarks on probabilistic criteria and for assessing
risks associated with those benchmarks. Uncertainties were incorporated in two ways. First,
the  simulation  model  was  iterated  over  Monte  Carlo  trials  to  generate  distributions  of
abundances in each year instead of point values. Second, the "base-case" simulation model
was  rerun  according  to  different  assumptions  about  parameter  values  and  model  structure
(including  assumptions  about  relationship  between  spawner  abundances  and  recruitment,
degree  of  depensatory  mortality  at  low  spawner  abundances,  trends  in  productivity,
magnitude  of  observation  errors,  length  of  historical  time  series  used  to  estimate
benchmarks,  and  deviations  between  target  and  realized  harvest  rates).  In  this  way,  we
evaluated how robust the performances of the lower benchmarks were to violations in the
base-case assumptions.

2

1.2  Candidate lower benchmarks

We  evaluated  lower  benchmarks  derived  from  previous  management  experience  and
the  scientific  literature  (see  Holt  et  al.  2009)  on  two  classes  of  indicators:  spawner
abundances  and  fishing  mortality  relative  to  productivity.  The  benchmarks  reflected  a
gradient  in  size  from  less  precautionary  (e.g.,  at  low  spawner  abundances  or  high  fishing
mortality,  where  only  very  depleted  CUs  were  classified  in  the  red  zone)  to  more
precautionary (e.g., at high spawner abundances or low fishing mortality, where moderately
depleted CUs were classified in the red zone) (Table 2).

Table  2.  List  of  lower  benchmarks  evaluated  in  the  simulation  model  for  indicators  on
spawner  abundances  (left  side)  and  fishing  mortality  (right  side).  Continued  on
next page.

Class of indicator: spawner abundances

Class of indicator: fishing mortality

Lower benchmark

Label

Lower benchmark

Label

Spawner
abundance at a
% of
recruitment
MSY

10%

20%

30%

40%

50%

60%

70%

80%

90%

Spawner abundance at
50% of maximum
recruitment

40% of spawner
abundance at MSY

S at 10% of
RMSY

S at 20% of
RMSY

S at 30% of
RMSY

S at 40% of
RMSY

S at 50% of
RMSY

S at 60% of
RMSY

S at 70% of
RMSY

S at 80% of
RMSY

S at 90% of
RMSY

S at 50% of
RMAX

Fishing
mortality at a
% of FMSY

50%

50% FMSY

60%

60% FMSY

70%

70% FMSY

80%

80% FMSY

90%

90% FMSY

100%

FMSY

110%

110% FMSY

120%

120% FMSY

130%

130% FMSY

140%

140% FMSY

40% of SMSY

150%

150% FMSY

3

Class of indicator: spawner abundances

Class of indicator: fishing mortality

Label

Sgen

Lower benchmark

Spawner abundance that
will result in recovery to
SMSY in one generation in
the absence of fishing
under equilibrium
conditions

1.3  Performance criteria

Lower benchmark

Maximum
ln(recruits/spawner)

Median
ln(recruits/spawner)

Label

FMAX

FMED

To  evaluate  performance  of  benchmarks  according  to  the  idealized  assessment
framework,  we  made  assumptions  about  the  information  required  at  steps  1-4  (reference
frame,  goal/endpoint,  time  frame,  and  management  action),  which  in  reality  should  be
provided  by  fisheries  management  (Table  1).  For  example,  for  lower  benchmarks  on
spawner abundances, to estimate the probability of extirpation over the long term (the first
performance  criteria),  we  assumed  a  constant  escapement  policy  equivalent  to  the  lower
benchmark and ran the simulation over 100 years. Similarly, to estimate the probability of
extirpation for lower benchmarks on fishing mortality, we assumed a constant harvest rate
policy equivalent to the benchmark over 100 years. To evaluate the probability of recovery
to a target (the second performance criteria) for benchmarks on spawner abundances, we set
population  abundances  to  the  lower  benchmark  at  the  beginning  of  the  simulation,  and
instead of a constant escapement policy, we assumed no commercial or recreational fishing
(e.g., fishing from test fisheries and by-catch from other fisheries only) over one (or three)
generations  (the  constant  escapement  policy  resulted  in  almost  no  recovery  and  therefore
gave  non-informative  comparisons  among  benchmarks).  To  evaluate  the  probability  of
recovery  to  a  target  for  benchmarks  on  fishing  mortality,  we  assumed  fishing  mortality
equivalent to the lower benchmark over the same time period.

4

 Table  3  Information  required  to  evaluate  lower  benchmarks  in  the  idealized  assessment
framework  (described  in  Table  1)  on  two  criteria:  probability  of  extirpation
(columns  2  and  3)  and  probability  of  recovery  (columns  4  and  5),  and  for  two
classes of indicators: those based on spawner abundances (columns 2 and 4) and
based on fishing mortality relative to productivity (columns 3 and 5). Although
information
the
responsibility  of  management,  we  provide  examples  here  to  demonstrate  the
properties of candidate benchmarks.

idealized  assessment  framework  are

items  1-4

the

in

Criteria to evaluate benchmark

Probability of extirpation
Benchmark on
spawner
abundances

Benchmarks on
fishing mortality

Probability of recovery
Benchmark on
spawner abundances

Benchmarks
on fishing
mortality

Biological production

Biological production

Information
required to
evaluate
benchmark

1. Reference
frame

2. Goal or
endpoint

Extirpation (<100 for each year in
one generation)

SMSY

3. Time frame to
achieve goal or
endpoint

4. Fishery
management
actions

5. Model relating
current state to a
future state

100 years

1 (or 3) generations

Constant
escapement
policy
equivalent to
the lower
benchmark

Constant harvest
rate policy
equivalent to the
lower benchmark

Spawner abundances
initialized at the
lower benchmark. No
targeted fishing in
subsequent years

Constant
harvest rate
policy
equivalent to
the lower
benchmark

As described in the "operating"
model

As described in the "operating"
model

6. Deterministic
upper benchmark

NA

NA

7. Deterministic
lower benchmark

8. Incorporate
uncertainty into
lower benchmark

9. Choice of risk
tolerance

As described in Table 2

As described in Table 2

As described in the "operating"
model

As described in the "operating"
model

A risk classification scheme was adapted from DFO's Fishery Decision-
Making Framework Incorporating the Precautionary Approach (2009).
Further work is required to identify risk tolerances from stakeholders.

5

2.1  Simulation models to evaluate lower benchmarks

2.  METHODS

We  developed  two  simulation  models  to  evaluate  candidate  lower  benchmarks  on
the two  performance criteria:  one model that evaluated the probability of extirpation over
the  long  term  (100  years)  (Model  1),  and  one  model  that  evaluated  the  probability  of
recovery  to  a  target  over  one  (or  three)  generations  (Model  2).  We  describe  Model  1  in
Sections  2.1.1  to  2.1.4,  and  then  describe  how  Model  2  differs  from  Model  1  in  Section
2.1.5. All variables and parameters are defined in Table 4. Model 1 had four components: a
population dynamics sub-model (Box 1 of Figure 1a), an observation sub-model (Box 2), a
management  sub-model  (Box  3),  and  a  performance  module  (Box  4).    The  population
dynamics, observation, and management sub-models were repeated over 100 years and 500
Monte Carlo trials (the number required to stabilize output metrics).

Table 4. Parameters and variables used to simulate population dynamics, observations, and

management for the base case model.

Equation
where
parameter
or
variable is
first
introduced
1

Definition

Parameter
or
variable

y

R

S

a

b







Brood year

Abundance of recruitment

Abundance of spawners

Productivity parameter of Ricker model

Capacity parameter of Ricker model

Autocorrelated stochastic variability in
recruitment

Autocorrelation coefficient

Stochastic deviations in recruitment

2

Variance in residual error of spawner-
recruitment relationship

Value (for
estimated
parameters
only)

0.37

0.68

6

Equation
where
parameter
or
variable is
first
introduced
2

6

7

8

9

10

In text

Definition

Parameter
or
variable

Value (for
estimated
parameters
only)

Rdep

S*

G

g

t

pg,t

xg,t

gp





RO

t



2


ht

Et

FL

Recruitment at low spawner abundances
accounting for depensatory mortality

Threshold in spawner abundances below which
depensatory mortality occurs

Total number of classes of age-at-maturity

3

Age-at-maturity

Return year

Proportion of recruits that return at a given age
in a given year

Dummy variable calculated in Eqn. 4

Average proportion of recruits that return at age
g

Standard deviation in the multivariate logistic
distribution of proportions at age

Standard normal deviates

p1 = 0.003,
p2 = 0.917,
p3 = 0.081

0.1

Observed recruitment

Return year

Normally distributed random variability

Variance in 

0.19

Target harvest rate in return year t

Escapement goal in year t

Lower benchmark on fishing mortality

Standard deviation between realized and target
harvest rate

0.19

7

(a)
(a)

(1a)
(1a)

(1b)
(1b)

Initialize spawner abundances
Initialize spawner abundances

Population
Population
dynamics sub-
dynamics sub-
model
model

Sample
Sample
recruitment
recruitment
from Sy
from Sy

Ry
Ry

Sy
Sy

(1c)
(1c)

Proportion
Proportion
of Ry by BY
of Ry by BY

3 4 5
3 4 5
3 4 5
Age-at-return
Age-at-return

+
+
multivariate
multivariate
logistic
logistic
variation
variation

Observation
Observation
sub-model
sub-model

(2)
(2)
Sample
Sample
observed R0,t
observed R0,t

Rt
Rt

R0,t
R0,t

Management
Management
sub-model
sub-model

(3b)
(3b)

Target harvest rate ht
Target harvest rate ht
ht= R0,t -Starget
ht= R0,t -Starget

R0,t
R0,t

(3c)
(3c)

Outcome uncertainty
Outcome uncertainty

ht
ht

Realized harvest rate h't
Realized harvest rate h't

(3d)
(3d)

Escapement
Escapement
Sy=(1-h't ) · Rt
Sy=(1-h't ) · Rt

(3a)
(3a)
Management
Management
target (Starget)
target (Starget)
derived from the
derived from the
lower benchmark,
lower benchmark,
which is
which is
estimated from
estimated from
simulated
simulated
historical data in
historical data in
a separate sub-
a separate sub-
model
model

Repeat over 100
Repeat over 100
years
years

Performance
Performance
module
module

(4)
(4)

Was the population extirpated?
Was the population extirpated?

Repeat over 500 Monte
Repeat over 500 Monte
Carlo trials
Carlo trials

Figure  1.  Simulation  modelling  framework  used  to  evaluate  the  probability  of  extirpation
over  the  long  term  (a)  and  probability  of  recovery  to  SMSY  (b,  next  page)  for
lower benchmarks on spawner abundances. Sy is the spawner abundance in brood
year y, R is recruitment, t is year of recruitment, R0 is observed recruitment, h is
target harvest rate derived from target spawner abundances, Starget, and observed
recruitment,  and  h'  is  the  realized  harvest  rate  (i.e.,  harvest  with  outcome

8

uncertainty).  Note,  panel  (b)  does  not  include  an  "Observation  sub-model"
because for that model evaluated probability of recovery under a scenario of no
directed fishing, and so observations of abundance were not required.

(b)
(b)

Population
Population
dynamics sub-
dynamics sub-
model
model

Management
Management
sub-model
sub-model

(3a)
(3a)
Initial spawner
Initial spawner
abundance
abundance
derived from the
derived from the
lower benchmark,
lower benchmark,
which was
which was
estimated from
estimated from
simulated
simulated
historical data in
historical data in
a separate sub-
a separate sub-
model
model

(1a)
(1a)

Initialize spawner abundances
Initialize spawner abundances

(1b)
(1b)
Sample
Sample
recruitment
recruitment
from Sy
from Sy

Ry
Ry

Sy
Sy

(1c)
(1c)

Proportion
Proportion
of Ry by BY
of Ry by BY

3 4 5
3 4 5
3 4 5
Age-at-return
Age-at-return

+
+
multivariate
multivariate
logistic
logistic
variation
variation

(3b)
(3b)

Harvest rate ht =0.1
Harvest rate ht =0.1
(no commercial or
(no commercial or
recreational fishing)
recreational fishing)

(3c)
(3c)

Outcome uncertainty
Outcome uncertainty

ht
ht

Realized harvest rate h't
Realized harvest rate h't

(3d)
(3d)

Escapement
Escapement
Sy=(1-ht ) · Rt
Sy=(1-ht ) · Rt

Performance
Performance
module
module

(4)
(4)

Did the population recover to SMSY?
Did the population recover to SMSY?

Repeat over 1-3
Repeat over 1-3
generations
generations

Repeat over 500 Monte
Repeat over 500 Monte
Carlo trials
Carlo trials

2.1.1  Population dynamics sub-model

In  the  population  dynamics  sub-model,  we  simulated  numerous  hypothetical
sockeye salmon populations, incorporating stochastic variability in recruitment and age-at-
maturity.    Specifically,  spawner  abundance  in  brood  year  y,  Sy,  was  used  to  calculate

9

recruitment  resulting  from  that  spawning,  Ry,  using  a  Ricker  model  with  lognormally
distributed random variation, and autocorrelation in residuals with a one-year time lag:

(Eqn. 1)

R

y



eS
y

a

1(



S

/
y b

)


y

,



y

y

1



y

,

v


,0N~

2
 ,
v

where a is the productivity parameter (loge (recruits/spawner) at low spawner abundances),
b  is  spawner  abundances  at  replacement  (or  equilibrium),   describes  autocorrelated
variability in recruitment,  is the autocorrelation coefficient, and describes the stochastic
deviations in recruitment.

We included depensatory mortality at low abundances as described in Holt (2007).
Below a lower threshold (S* = 500 spawners), recruitment that accounted for depensation
(Rdep,y)  declined  more  rapidly  as  spawner  abundances  declined  than  if  depensation  was
ignored (i.e., when Ry was derived from Eqn. 1):

(Eqn. 2)

R

dep

,

y



R

y



1








S

*



S

y

S

*






, for Sy < S*

Those reductions in recruitment were curvilinear with steepest rates of change immediately
below  S*  and  an  asymptote  near  zero  spawners  (of  zero  recruits).  Although  evidence  for
depensatory  mortality  at  low  abundances  is  weak  for  most  species  and  stocks  of  Pacific
salmon, it has been documented at abundances higher than 500 spawners (our threshold, S*)
in some cases (e.g., 7000 spawners, Cultus Lake sockeye salmon, M. Bradford, pers. comm.
Cooperative Resource Management Institute, Simon Fraser University, Burnaby, B.C.). We
therefore  varied  the  lower  threshold  below  which  depensation  occurred  in  a  sensitivity
analysis.  An  alternative  approach  to  modelling  depensation  is  to  offset  the  spawner-
recruitment  model  to  the  right  by  the  abundance  of  spawners  below  which  depensatory
mortality  results  in  zero  recruitment  (Chen  et  al.,  2002).  However,  in  contrast  to  the
approach described in Eqns. (1) and (2), for the method of Chen et al. (2002), the predicted
recruitment  above  the  depensation  threshold  (or  offset  amount)  varies  depending  on
whether depensation at low spawner abundances is accounted for or ignored. To isolate the
effects of depensation at low spawners only, we used the method described in Eqns. (1) and
(2). The assumptions associated with the base case and all sensitivity analyses are described
in Table 5.

10

Table 5. Assumptions of the "base-case" model, and variations to those assumptions applied
in  the  sensitivity  analyses.  "Sub-model"  pertains  to  where  that  assumption  is
made  in  the  operating  model,  as  described  in  Figure  1.  Note,  some  sensitivity
analyses  were  performed  on  only  a  subset  of  model  scenarios  (e.g.,  the  last
sensitivity analysis was performed only on benchmarks of spawner abundances,
because  for  benchmarks  based  on  fishing  mortality,  management  actions  were
derived from pre-specified F values). Continued on next page.

Assumption

Threshold in
spawner
abundance below
which depensatory
mortality occurs

Form of the stock-
recruitment model

Productivity
(Ricker a
parameter =
loge(R/S) at low S)

Time trends in
productivity
(Ricker a
parameter=
loge(R/S) at low S)

Sub-model
(Eqn.)
Population
dynamics
sub-model
(Eqn. 2)

Population
dynamics
sub-model
(Eqns. 1-5)
Population
dynamics
sub-model
(Eqn. 1)

Population
dynamics
sub-model
(Eqn. 1)

"Base case"

500

Variations applied to
sensitivity analyses
1000, 7000

Ricker with
autocorrelation
and depensation

Ricker without autocorrelation
and depensation, Beverton-Holt,
Larkin

Moderate (a =
1.5, 4.5 R/S at
low S)

Constant
productivity
over time

Low (a = 0.5, or 1.6 R/S), High
(a = 2.0, or 7.4 R/S)

Linear increase in productivity
equivalent to 0.01 loge(R/S) per
year, linear decline in
productivity equivalent to 0.015
loge(R/S) per year, cyclic trend
in productivity with a period of
20 years and amplitude of 0.5
loge(R/S)

Magnitude of
observation errors
()

Observation
sub-model
(Eqn. 8)

Low (= 0.19)  High (= 0.38)

Management
sub-model

20

15, 30

Length of time
series used to
estimate stock-
recruitment model
parameters and
benchmarks

11

Sub-model
(Eqn.)
Management
sub-model

"Base case"

High (standard
deviation =
0.19)

Variations applied to
sensitivity analyses
Low (standard deviation =
0.097)

Management
sub-model

0.1

0.02, 0.2

Assumption

Magnitude of
outcome
uncertainties

Lower limit on
fishing mortality
(due to non-
commercial
harvest, such as
by-catch)

For  some  stocks  and  species,  alternative  formulations  of  the  spawner-recruitment
relationship may be appropriate (e.g., Ricker without depensation or autocorrelation, (Eqn.
3),  Beverton-Holt  (Eqn.  4),  or  Larkin  models  (Eqn.  5)).  We  therefore  varied  the  stock-
recruitment model in a sensitivity analysis.

(Eqn. 3)

R

y



eS
y


1
(a


v)b/S

y

y

,

v


,0N~

2

v

(Eqn. 4)

R

y



S

Sa
b

v



e

,

v


,0N~

2

v

(Eqn. 5)

R

y



eS
y


a


Sb
1

y


Sb
2


Sb
3

y

1


y



2




v

y


,0N~

2

v

,

v

where a', b', a", b", a"', b1"', b2"', and b3"' are parameters. The values of those parameters
were selected so that SMSY and harvest rate at MSY for each model were equivalent to those
for the base-case Ricker model.

We  assumed  the  productivity  parameter  of  the  stock-recruitment  relationship  was
constant  over  time,  but  included  normally  distributed  variability  in  that  parameter  over
Monte  Carlo  trials (mean a=1.5, equivalent to approximately 4.5 recruits/spawners at low
spawners,  sd  =0.3).  In  a  sensitivity  analyses,  we  investigated  the  effects  of  constant  low
productivity (mean a = 0.5, or 1.6 recruits/spawner) and high productivity (mean a = 2.0, or
7.4  recruits/spawner)  on  the  relative  performance  of  benchmarks.  We  further  investigated
the  effects  of  three  time  trends  in  productivity:  a  linear  increase,  a  linear  decrease,  and  a
sinusoidal pattern with a period of 20 years and amplitude of 1.0 loge(recruits/spawner). We
varied  the  spawner  abundances  at  equilibrium  (b  parameter)  in  fixed  intervals  of  1000
spawners between 1000 and 100 000 fish (i.e., the model was run separately for populations
of  different  carrying  capacities).  This  allowed  us  to  compare  results  under  various
combinations  ((3+3)    100  =  600)  of  productivity  (a)  and  spawner  abundances  at
equilibrium (b).

12

Natural variation in the proportion at each age-at-maturity pg, in return year t, was
incorporated into the population dynamics model using a multivariate logistic distribution
(Schnute and Richards, 1995):

x

,
tg

e
G
 

g

1

,

x

,
tg

e

(Eqn. 6)

p

tg
,



where,

(Eqn. 7)

x

tg
,



log

(

p

g

e

)





tg
,



1
G

G



g

1



log

(

p

g

e

)





tg
,



,

G is the oldest age class,

gp is the mean proportions at age,    is the standard deviation in
the  multivariate  logistic  distribution  of  proportions  at  age,  and  g,t  are  standard  normal
gp and     were  estimated  from  historical  data  (described  in  the  Model
deviates.  Both
Parameterization  sub-section  below).  Spawner  abundances  were  initialized  at  1000
spawners.

2.1.2  Observation sub-model

Uncertainty  in  observations  of  recruitment  come  from  many  sources,  including
errors in  visual observations of  spawner abundance (e.g.,  visual observations from stream
walks or aerial surveys), sampling  variability of spawners and catches, and uncertainty in
non-harvest mortality during return migration. The observed number of recruits, R0, in year
t,  was  calculated  from  the  true  number  of  recruits,  Rt,  with  multiplicative,  lognormally
distributed random variability, as in (Cass et al., 2003),

(Eqn. 8)

R

,0
t


teR
t

,




,0N~

2


,

where  is normally distributed random variability with a standard deviation, .

To properly parameterize natural process variation in recruitment () (Eqn. 1) and
observation  error  ()  (Eqn.  8),  we  needed  to  partition  variability  from  those  two  specific
sources from the total observed variability in recruitment. Historical recruitment data used
to  estimate  parameters  in  equation  1  contained  both  natural  process  variation  and
observation error; hence recruitment calculated from these equations also contained both 
and . To separate the various contributors to total variability, we used a simple simulation
model to estimate the standard deviations of the natural process variation,  (equations 1),
which, in combination with observation errors (), resulted in standard deviations in total
recruitment  equal  to  those  observed  historically  ().    Note  that  those  variances  were  not
  indicating  that  the  sources  of  variability  were  not
additive  (i.e.,  
independent.  We  found  that  the  total  combined  uncertainty  ()  was  swamped  by  large
natural  variability  in  recruitment.    Specifically,  the  standard  deviation  in  natural  process

≠  



13

variation was equal to 94% of the standard deviation in total combined recruitment for both
stocks (i.e., = 0.94).

2.1.3  Management sub-model

Management actions were simulated in two parts, (1) the selection of a management
target  based  on  a  constant  escapement  policy  equivalent  to  the  lower  benchmark  on
spawner abundances or constant harvest rate equivalent to the lower benchmark on fishing
mortality  (Table  2),  and  (2)  the  implementation  of  that  target  including  outcome
uncertainty, i.e., uncertainty in the outcomes of implementing a harvest strategy (Holt and
Peterman, 2006).

Benchmarks related to SMSY or FMSY cannot be estimated exactly due to observation
errors  in  abundances,  sampling  variability,  and  model  misspecification,  among  other
factors.  To  account  for  those  uncertainties,  we  identified  benchmarks  using  parameter
estimates  of  the  spawner-recruitment  relationship  derived  from  simulated  historical  data.
Specifically, for every Monte Carlo trial in the overall simulation model, we simulated 20
years  of  historical  data  in  a  separate  sub-model  (i.e.,  separate  from  the  models  used  to
evaluate  lower  benchmarks)  assuming  a  Ricker  spawner-recruitment  with  the  same
parameters  used  in  the  population  dynamics  sub-model  for  that  Monte  Carlo  trial,  and  a
harvest rate of 70% (to represent a heavily exploited stock) with beta-distributed variability
in outcomes (Box 3a, Fig. 1). Maximum likelihood techniques were then used to estimate
parameters  of  the  Ricker  spawner-recruitment  relationship  (a,  b  and  
),  as  well  as  the
lower benchmark. By using short time-series of simulated data to estimate parameters, we
were  able  to  produce  the  commonly  observed  positive  bias  in  productivity  (Walters  and
Martell,  2004).    In  a  sensitivity  analysis,  we  increased  the  number  of  years  of  data
simulated to estimate parameters from 20 to 30 in order to evaluate the effects of increased
historical information on the performance of benchmarks.

To  improve  estimation  of  the  capacity  parameter  ("b"  of  the  stock-recruitment
relationship),  we  included  prior  information  on  that  parameter,  which,  in  practice,  can  be
generated from freshwater capacity studies or landscape characteristics (Parken et al., 2006;
Shortreed et al., 2001). Specifically, a penalty was added to the likelihood function, which
was  drawn  from  a  log-normal  distribution  with  a  mean  equal  to  the  true  value  and  a
standard  deviation  of  0.6,  in  units  of  loge(1000  spawners).  Estimates  of  "b"  that  were  far
from the true value were penalized inversely proportional to that distribution.

For lower benchmarks on spawner abundances, target harvest rates in return year t,

ht, were calculated from observed recruitment, RO,t, and the escapement goal, Et,

(Eqn. 9)

h
t

1 

/
RE
t

,
tO

.

For  lower  benchmarks  on  fishing  mortality,  FL,  target  harvest  rates  were  calculated  using
the standard equation to convert natural logarithms (F) to a proportion between 0 and 1 (h):
(Eqn. 10)

 1
e

.

LF

h
t

14

Target  harvest  rates  are  rarely  achieved  exactly  because  of  variability  in  the
catchability of fish, non-compliance to fishing regulations, and management pressures that
cause decisions to deviate from those that achieve targets, among other factors (Holt et al.
2006). To account for those uncertainties, we included random variation in the outcomes of
harvest  rates  assuming  a  beta-distribution  of  errors  (as  described  in  Holt  and  Peterman
(2008)).

2.1.4  Performance module

In  the  performance  module,  we  evaluated  the  probability  of  extirpation  (i.e.,
populations where spawner abundances < 100 fish in four consecutive years) by computing
the proportion of Monte Carlo trials where populations met that criterion.

2.1.5  Differences between Models 1 and 2

The model used to evaluate probability of recovery to a target (Model 2) differed from
Model  1  in  four  ways.  First,  the  spawner  abundances  at  equilibrium  was  set  to  a  single
value,  10,000  spawners  instead  of  multiple  values  between  1000  and  100,000,  because
preliminary  results  suggested  that  probability  of  recovery  was  independent  of  spawner
abundances  at  equilibrium.  Second,  for  candidate  benchmarks  on  spawner  abundances,
spawners were initialized at the lower benchmark instead of 1000 fish so that the recovery
from  the  lower  benchmark  could  be  evaluated.  For  candidate  benchmarks  on  fishing
mortality, spawners were instead initialized at 10% of spawner abundances at equilibrium.
Third,  for  candidate  benchmarks  on  spawner  abundances,  we  assumed  no  commercial  or
recreational fishing. We assumed the unavoidable harvest (e.g., due to test fisheries and by-
catch from other fisheries, among other sources), ht, was 0.1, but this value was varied in a
sensitivity analysis, ht= 0.02 and ht= 0.2. Although those harvest rates are not management
targets, we included outcome uncertainty in those values to simulate interannual variability
in  non-commercial,  non-recreational  harvest.  For  candidate  benchmarks  on  fishing
mortality, the target harvest rate was set to the lower benchmark on  fishing mortality and
also  included  outcome  uncertainty.  Fourth,  in  the  performance  module,  we  evaluated  the
probability  of  recovery  to  SMSY  in  one  and  three  generation(s),  instead  probability  of
extirpation  over  100  years,  by  computing  the  proportion  of  Monte  Carlo  trials  where
populations rebuilt to above SMSY in at least one year over that time period.

2.2  Model parameterization

The  parameters  in  Equations  1,  6,  and  7  were  estimated  from  historical  data  on
Early Stuart sockeye salmon (K. Benner, pers. comm., Fisheries and Oceans Canada, 985
McGill Place, Kamloops, B.C., V2C 6X6) (Table 4), with the exception of the productivity
and  capacity  parameters  ("a"  and  "b")  in  Equation  1,  which  are  as  described  in  the
"Population dynamics sub-model" and "Observation sub-model" sub-sections. Although our
base-case  represents  one  species  in  one  region  (sockeye  salmon  in  the  Fraser  River)  our
extensive  sensitivity  analyses  cover  characteristics  of  stocks  and  species  with  alternative
stock-recruitment  relationships  (e.g.,  models  with  and  without  depensation  and

15

autocorrelation, Beverton-Holt model, and Larkin model) and scenarios about observations,
assessments, and management.

The  magnitude  of  observation  errors  was  derived  from  mark-recapture  studies  on
sockeye spawner abundances in Chilko Lake between 2001 and 2004 (T. Whitehouse pers.
comm.  Fisheries  and  Oceans  Canada,  985  McGill  Place,  Kamloops,  B.C.,  V2C  6X6)
(standard  deviation  in  observation  error,  ,  =  0.19).    Although  uncertainties  in  catch
estimates and non-harvest mortality are not included in that estimate, we increased  in a
sensitivity analysis to twice that value ( = 0.38), a rough upper estimate of the magnitude
of the total observation errors in recruitment.

Parameters describing outcome uncertainty were for Summer-Run sockeye salmon on
the  Fraser  River,  as  estimated  by  Holt  and  Peterman  (2006)  (standard  deviation  between
realized  and  target  mortality  rates  =  0.097).  In  a  sensitivity  analysis,  we  increased  the
magnitude of those uncertainties to those observed for Late-Summer run sockeye (standard
deviation  =  0.19)  (Holt  and  Peterman,  2006),  a  stock  with  relatively  large  deviations
between target and realized mortality rates.

3.  RESULTS

First  we  present  results  on  Model  1  (the  probability  of  extirpation  over  the  long
term)  and  then  Model  2  (the  probability  of  recovery  to  SMSY  within  one  (or  three)
generations).  Within  each  model,  we  first  evaluate  lower  benchmarks  on  spawner
abundances, and then lower benchmarks on fishing mortality.

3.1  Model 1: Probability of extirpation over the long term

3.1.1  Lower benchmarks on spawner abundances

When  populations  were  projected  forward  under  constant  escapement  policies
equivalent to lower benchmarks derived from S at 40-90% of RMSY (black lines labeled 40-
90% Figure 2), S at 50% of RMAX (red line), 40% of SMSY (blue line), and Sgen (green line),
probabilities of extirpation were low or very low (probabilities <25% or <5%, respectively,
definitions  adapted  from  DFO's  "Fishery  decision-making  framework  incorporating  the
Precautionary  Approach"(2009))  when  equilibrium  abundances  were  >  15,000  fish  (right
side of Figure 2). Below that equilibrium abundance (left side of Figure 2), probabilities of
extirpation were higher or rose steeply for all benchmarks. When we assumed populations
were highly productive (mean Ricker "a" value = 2.0, equivalent to 7.4 recruits/spawner at
low  spawner  abundances),  probabilities  of  extirpation  tended  to  be  lower  for  most
benchmarks (Figure 3c) compared with the moderate productivity case (Figure 3b). In other
words,  highly  productive  populations  were  better  able  to  rebound  from  occasional  poor
recruitment  years  than  less-productive  populations.  In  contrast,  when  we  assumed
populations  were  relatively  unproductive  (mean  Ricker  "a"  value  =  0.5,  equivalent  to  1.6
recruits/spawner  and  low  spawner  abundances),  probabilities  of  extirpation  tended  to  be
higher for most benchmarks. The differences among productivity scenarios were relatively

16

minor for the benchmark based on Sgen, spawner abundances that will result in recovery to
SMSY  in  one  generation  under  equilibrium  conditions  (green  line;  i.e.,  performance  of  Sgen
was  relatively  insensitive  to  variability  in  productivity  levels).  Those  differences  were
relatively large for benchmarks based on RMSY (black lines) and SMSY (blue line).  For the
remaining  sensitivity  analyses,  we  show  results  for  only  a  single  benchmark,  Sgen.  The
trends in results (direction of change and rank sensitivity of performance to the assumption)
were similar among benchmarks.

S at 50% of RMAX
S at 50% of RMAX
40% of SMSY
40% of SMSY
Sgen
Sgen

1
1
0
0
%
%

1.0
1.0

0.8
0.8

0.6
0.6

0.4
0.4

0.2
0.2

0.0
0.0

n
n
o
o

i
i
t
t

a
a
p
p
r
r
i
i
t
t
x
x
e
e

f
f

o
o
y
y
t
t
i
i
l
l
i
i

b
b
a
a
b
b
o
o
r
r
P
P

2
2
0
0
%
%

3
3
0
0
%
%

60%
60%

70%
70%

80%
80%

5
5
0
0
%
%

9
9
0
0
%
%

40%
40%

0
0

10 20 30 40 50 60 70 80 90
10 20 30 40 50 60 70 80 90

Spawner abundance at equilibruim (1000s of fish)
Spawner abundance at equilibruim (1000s of fish)

Figure  2.  Probabilities  of  extirpation  over  the  long  term  (100  years)  for  simulated
populations  of  Pacific  salmon  under  a  constant  escapement  policy  equal  to  the
lower  benchmarks  derived  from  spawner  abundances  at  various  percentages  of
RMSY  (black  lines)  over  a  gradient  in  equilibrium  stock  sizes  (X-axis).    Three
other lower benchmarks are shown: spawner abundances, S, at 50% of RMAX (red
line),  40%  of  SMSY  (blue  line),  and  spawner  abundance  resulting  in  recovery  to
SMSY in one generation without fishing under equilibrium conditions, Sgen (green
line).

17

n
n
o
o
i
i
t
t
a
a
p
p
r
r
i
i
t
t
x
x
e
e

f
f
o
o
y
y
t
t
i
i
l
l
i
i

b
b
a
a
b
b
o
o
r
r
P
P

1.0
1.0

0.8
0.8

0.6
0.6

0.4
0.4

0.2
0.2

0.0
0.0

(a)
(a)

(b)
(b)

(c)
(c)

1.0
1.0

0.8
0.8

0.6
0.6

0.4
0.4

0.2
0.2

0.0
0.0

1.0
1.0

0.8
0.8

0.6
0.6

0.4
0.4

0.2
0.2

0.0
0.0

0
0

20
20

40
40

60
60

80
80

100
100

0
0

20
20

40
40

60
60

80
80

100
100

0
0

20
20

40
40

60
60

80
80

100
100

Spawner abundance at equilibrium (1000s of fish)
Spawner abundance at equilibrium (1000s of fish)
Figure  3.  Probabilities  of  extirpation,  p,  over  the  long  term  (100  years)  for  unproductive
(mean  Ricker  "a"  parameter  =  0.5,  or  1.7  recruits/spawner  at  low  spawner
abundances) (a), moderately productive (mean Ricker "a" parameter = 1.5, or 4.5
recruits/spawner  at  low  spawner  abundances)  (b),  and  highly  productive  (mean
Ricker "a" parameter = 2.0, or 7.4 recruits/spawner at low spawner abundances)
(c) simulated populations of Pacific salmon under a constant escapement policy
equal  to  the  lower  benchmarks  derived  from  spawner  abundances  at  various
percentages  of  RMSY  (black  lines,  ranging  from  10%  (top  line)  to  90%  (bottom
line))  over  a  gradient  in  equilibrium  stock  sizes  (X-axis).  Three  other  lower
benchmarks  are  shown,  as  described  in  the  caption  to  Fig.2:  S  at  50%  of  RMAX
(red line), 40% of SMSY (blue line), and Sgen (green line).

Similar to the results from different constant levels of productivity, when productivity
increased over time, the probability of extirpation declined, and vice versa (Figure 4). When
cyclic patterns in recruitment were introduced into the operating model (with mean Ricker
"a" parameter = 1.5), probability of extirpation declined only marginally.

18

n
o
i
t
a
p
r
i
t
x
e

f
o
y
t
i
l
i

b
a
b
o
r

P

No trend
Linear increase
Linear decline
Cyclic pattern

1.0

0.8

0.6

0.4

0.2

0.0

0

100
Spawner abundance at equilibrium (1000s of fish)

60

80

20

40

Figure 4. Probabilities of extirpation over the long term (10 0

years)

simulated
populations  of  Pacific  salmon  under  a  constant  escapement  policy  equal  to  the
lower  benchmark  derived  from  Sgen  (spawner  abundances  that  will  result  in
recovery  to  SMSY  in  one  generation  under  equilibrium  conditions)  and  four
assumptions  about  the  trends  in  stock  productivity  (Ricker  "a"  parameter):  no
trend (thick solid line); linear increase over time (thin solid line); linear decline
over  time  (dashed  line);  and  cyclic  pattern  (dotted  line),  over  a  gradient  in
equilibrium stock sizes (X-axis).

for

Probabilities of extirpation were higher for the Ricker model with autocorrelated errors
and  depensatory  mortality  than  for  the  remaining  models:  standard  Ricker  without
autocorrelation  and  depensation,  Beverton-Holt,  and  Larkin  (Figure  5).  We  assumed
recruitment followed a Ricker model with autocorrelation and depensation for the base case
because of empirical evidence for those phenomena (Chen et al., 2002; Korman et al., 1995;
Wood,  1987),  and  to  generate  a  precautionary  evaluation  of  performance  (i.e.,  an  upper
estimate  of  probability  of  extirpation).  When  we  increased  the  threshold  below  which
depensation  occurred  to  7000,  the  probabilities  of  extirpation  increased  to  near  100%
(Figure 6). Populations were initialized at 1000 spawners in our simulation model and were
unable to rebuild from low abundances under that scenario.

19

n
o
i
t
a
p
r
i
t
x
e

f
o
y
t
i
l
i

b
a
b
o
r

P

Ricker
Ricker w ith AR(1) and dep.
Beverton-Holt
Larkin

1.0

0.8

0.6

0.4

0.2

0.0

0

100
Spawner abundance at equilibrium (1000s of fish)

60

40

20

80

Figure  5.  Probabilities  of  extirpation  over  the  long  term  (100  years)  for  simulated
populations  of  Pacific  salmon  under  a  constant  escapement  policy  equal  to  the
lower  benchmark  derived  from  Sgen  (spawner  abundances  that  will  result  in
recovery  to  SMSY  in  one  generation  under  equilibrium  conditions)  and  four
assumptions  about  the  stock-recruitment  model:  Ricker  model  (thin  solid  line),
Ricker  model  with  autocorrelation  and  depensatory  mortality  at  low  spawner
abundances  (thick  solid  line),  Beverton-Holt  model  (dashed  line),  and  Larkin
model (dotted line), over a gradient in equilibrium stock sizes (X-axis).

20

n
o
i
t
a
p
r
i
t
x
e

f
o
y
t
i
l
i

b
a
b
o
r

P

1.0

0.8

0.6

0.4

0.2

0.0

Low  depensation
Moderate depensation
High depenstation

0

100
Spawner abundance at equilibrium (1000s of fish)

60

80

40

20

Figure  6.  Probabilities  of  extirpation  over  the  long  term  (100  years)  for  simulated
populations  of  Pacific  salmon  under  a  constant  escapement  policy  equal  to  the
lower  benchmark  derived  from  Sgen  (spawner  abundances  that  will  result  in
recovery  to  SMSY  in  one  generation  under  equilibrium  conditions)  and  three
assumptions  about  the  spawner  abundance  below  which  depensatory  mortality
occurs: 500 fish (thick solid line); 1000 fish (thin solid line); 7000 (dashed line),
over a gradient in equilibrium stock sizes (X-axis).

Probabilities of extirpation were less sensitive to variability in management parameters
(the  magnitude  of  observation  errors  and  outcome  uncertainties,  the  number  of  years  of
historical data available to estimate benchmarks, and the lower limit on harvest rates due to
non-commercial and non-recreational catch) than to biological parameters on productivity.
In  general,  increasing  uncertainty  and  harvest  resulted  in  increasing  probability  of
extirpation (Figure 7, Figure 8, Figure 9, and Figure 10).

21

n
o
i
t
a
p
r
i
t
x
e

f
o
y
t
i
l
i

b
a
b
o
r

P

Low  observation error
High observation error

1.0

0.8

0.6

0.4

0.2

0.0

0

100
Spawner abundance at equilibrium (1000s of fish)

60

80

40

20

Figure  7.  Probabilities  of  extirpation  over  the  long  term  (100  years)  for  simulated
populations  of  Pacific  salmon  under  a  constant  escapement  policy  equal  to  the
lower  benchmark  derived  from  Sgen  (spawner  abundances  that  will  result  in
recovery  to  SMSY  in  one  generation  under  equilibrium  conditions)  and  two
assumptions  about  the  magnitude  of  observation  errors:  standard  deviation
between actual and observed abundance = 0.19 (thin solid line) and 0.38 (thick
solid line), over a gradient in equilibrium stock sizes (X-axis).

22

n
o
i
t
a
p
r
i
t
x
e

f
o
y
t
i
l
i

b
a
b
o
r

P

30 years of historical data
20 years of historical data
15 years of historical data

1.0

0.8

0.6

0.4

0.2

0.0

0

100
Spawner abundance at equilibrium (1000s of fish)

60

20

40

80

Figure  8.  Probabilities  of  extirpation  over  the  long  term  (100  years)  for  simulated
populations  of  Pacific  salmon  under  a  constant  escapement  policy  equal  to  the
lower  benchmark  derived  from  Sgen  (spawner  abundances  that  will  result  in
recovery  to  SMSY  in  one  generation  under  equilibrium  conditions)  and  three
assumptions about the number of years of historical data used to estimate RMSY
when  deriving  the  lower  benchmark  (corresponding  to  the  magnitude  of
assessment  uncertainty):  30  years  (low  assessment  uncertainty,  thin  solid  line),
20 years (moderate assessment uncertainty, thick solid line), and 15 years (high
assessment  uncertainty,  dashed  line),  over  a  gradient  in  equilibrium  stock  sizes
(X-axis).

23

n
o
i
t
a
p
r
i
t
x
e

f
o
y
t
i
l
i

b
a
b
o
r

P

Low  outcome uncertainty
High outcome uncertainty

1.0

0.8

0.6

0.4

0.2

0.0

0

100
Spawner abundance at equilibrium (1000s of fish)

60

80

40

20

Figure  9.  Probabilities  of  extirpation  over  the  long  term  (100  years)  for  simulated
populations  of  Pacific  salmon  under  a  constant  escapement  policy  equal  to  the
lower  benchmark  derived  from  Sgen  (spawner  abundances  that  will  result  in
recovery  to  SMSY  in  one  generation  under  equilibrium  conditions)  and  two
assumptions  about  the  magnitude  of  outcome  uncertainty:  standard  deviation
between realized harvest rates and targets = 0.097 (thin solid line) and 0.19 (thick
solid line), over a gradient in equilibrium stock sizes (X-axis).

24

n
o
i
t
a
p
r
i
t
x
e

f
o
y
t
i
l
i

b
a
b
o
r

P

Low  harvest rate
Moderate harvest rate
High harvest rate

1.0

0.8

0.6

0.4

0.2

0.0

0

100
Spawner abundance at equilibrium (1000s of fish)

60

80

40

20

Figure  10.  Probabilities  of  extirpation  over  the  long  term  (100  years)  for  simulated
populations  of  Pacific  salmon  under  a  constant  escapement  policy  equal  to  the
lower  benchmark  derived  from  Sgen  (spawner  abundances  that  will  result  in
recovery  to  SMSY  in  one  generation  under  equilibrium  conditions)  and  three
assumptions about the lower limit on harvest rate, ht, (due to non-target fishing
mortality,  e.g.,  test-fishery  and  by-catch):  low  ht  =  0.02  (thin  solid  line),
moderate  ht  =  0.1  (thick  solid  line),  and  high  ht  =  0.2  (dashed  line),  over  a
gradient in equilibrium stock sizes (X-axis).

3.1.2  Lower benchmarks on fishing mortality

When  populations  were  subjected  to  fishing  mortalities  equivalent  to  lower
benchmarks on F that were between 50-110% of FMSY, the probabilities of extirpation were
low or very low (probabilities <25% or <5%, respectively) for populations with equilibrium
abundances greater than 30,000 spawners. In contrast, when fishing mortality was equal to
benchmarks  derived  from  120-150%  of  FMSY,  FMAX,  and  FMED,  the  probabilities  of
extirpation  were  moderately  low  (probabilities  25-50%)  or  moderately  high  (probabilities
>50%). Performances of benchmarks near FMSY (90%-110% of FMSY) (red line, and black
lines directly above and below red line) were least sensitive to variability in productivity;
performances  of  benchmarks  derived  from  FMAX  and  FMED,  (blue  and  green  lines,
respectively) were most sensitive (Figure 12). For subsequent sensitivity analyses, we show
results for the lower benchmark, FMSY, only. The trends in results (direction of change and
rank sensitivity of performance to the assumption) were similar among benchmarks.

25

FMSY
FMSY
FMSY
FMSY
FMAX
FMAX
FMAX
FMAX
FMED
FMED
FMED
FMED

1.0
1.0
1.0

0.8
0.8
0.8

0.6
0.6
0.6

0.4
0.4
0.4

0.2
0.2
0.2

0.0
0.0
0.0

n
n
o
o
i
i
t
t
a
a
p
p
r
r
i
i
t
t
x
x
e
e

f
f
o
o
y
y
t
t
i
i
l
l
i
i

b
b
a
a
b
b
o
o
r
r
P
P

150%
150%
150%
150%

140%
140%
140%
140%

130%
130%
130%
130%
120%
120%
120%
120%

110%
110%
110%
110%

9
9
9
9
0
0
0
0
%
%
%
%

8
8
8
8
0
0
0
0
%
%
%
%
70%
70%
70%
70%

60%
60%
60%
60%
50%
50%
50%
50%

0
0
0

10 20 30 40 50 60 70 80 90
10 20 30 40 50 60 70 80 90
10 20 30 40 50 60 70 80 90

Spawner abundance at equilbrium (1000s of fish)
Spawner abundance at equilbrium (1000s of fish)
Spawner abundance at equilbrium (1000s of fish)

Figure  11.  Probabilities  of  extirpation  over  the  long  term  (100  years)  for  simulated
populations of Pacific salmon under a constant fishing mortality rate policy equal
to the lower benchmarks derived from various percentages of FMSY (black lines)
over  a  gradient  in  equilibrium  stock  sizes  (X-axis).    Three  other  lower
benchmarks are shown: FMSY (red line, equivalent to 100% FMSY), the maximum
loge(recruits/spawner)  at  low  spawner  abundances  (i.e.,  Ricker  "a"  parameter)
(FMAX, blue line), and the median loge(recruits/spawner) (FMED, green line).

26

(a)

(b)

(c)

n
n
o
o

i
i
t
t

a
a
p
p
r
r
i
i
t
t
x
x
e
e

f
f

o
o
y
y
t
t
i
i
l
l
i
i

b
b
a
a
b
b
o
o
r
r
P
P

1.0
1.0

0.8
0.8

0.6
0.6

0.4
0.4

0.2
0.2

0.0
0.0

0
0

20
20

40
40

60
60

80
80

1.0
1.0

0.8
0.8

0.6
0.6

0.4
0.4

0.2
0.2

0.0
0.0

1.0
1.0

0.8
0.8

0.6
0.6

0.4
0.4

0.2
0.2

0.0
0.0

100
40
40
100
Spawner abundance at equilibrium (1000s of fish)
Spawner abundance at equilibrium (1000s of fish)

100
100

80
80

20
20

60
60

0
0

0
0

20
20

40
40

60
60

80
80

100
100

Figure 12. Probabilities of extirpation, p, over the long term (100 years) for unproductive
(mean  Ricker  "a"  parameter  =  0.5,  or  1.7  recruits/spawner  at  low  spawner
abundances) (a), moderately productive (mean Ricker "a" parameter = 1.5, or 4.5
recruits/spawner  at  low  spawner  abundances)  (b),  and  highly  productive  (mean
Ricker "a" parameter = 2.0, or 7.4 recruits/spawner at low spawner abundances)
(c) simulated populations of Pacific salmon under a constant escapement policy
equal to the lower benchmarks derived from various percentages of FMSY (black
lines,  ranging  from  150%  (top  line)  to  50%  (bottom  line))  over  a  gradient  in
equilibrium  stock  sizes  (X-axis).  Three  other  lower  benchmarks  are  shown,  as
described  in  the  caption  to  Fig.11:  FMSY  (red  line),  FMAX  (blue  line),  and  FMED
(green line).

Similar  to  the  results  for  benchmarks  on  spawner  abundances,  probabilities  of
extirpation  for  benchmarks  on  fishing  mortality  were  less  sensitive  to  variability  in
management parameters (the magnitude of outcome uncertainties and the number of years
of  historical  data  available  to  estimate  benchmarks)  than  to  biological  parameters  on
productivity (e.g., especially large increases and declines over time) (Figure 13, Figure 14,
and  Figure  15).  In  general,  increasing  uncertainty  and  harvest  resulted  in  increasing
probability of extirpation (Figure 16 and Figure 17).

27

n
o
i
t
a
p
r
i
t
x
e

f
o
y
t
i
l
i

b
a
b
o
r

P

1.0

0.8

0.6

0.4

0.2

0.0

No trend
Linear increase
Linear decline
Cyclic pattern

0

100
Spawner abundance at equilibrium (1000s of fish)

60

20

40

80

Figure  13.  Probabilities  of  extirpation  over  the  long  term  (100  years)  for  simulated
populations of Pacific salmon under a constant fishing mortality rate policy equal
to the lower benchmarks,  FMSY, and four assumptions about the trends in stock
productivity  (Ricker  "a"  parameter):  no  trend  (thick  solid  line);  linear  increase
over  time  (thin  solid  line);  linear  decline  over  time  (dashed  line);  and  cyclic
pattern (dotted line), over a gradient in equilibrium stock sizes (X-axis).

28

n
o

i
t

a
p
r
i
t
x
e

f

o
y
t
i
l
i

b
a
b
o
r

P

Ricker
Ricker w ith AR(1) and dep.
Beverton-Holt
Larkin

1.0

0.8

0.6

0.4

0.2

0.0

0

100
Spawner abundance at equilibrium (1000s of fish)

40

20

80

60

Figure  14.  Probabilities  of  extirpation  over  the  long  term  (100  years)  for  simulated
populations of Pacific salmon under a constant fishing mortality rate policy equal
to  the  lower  benchmarks,  FMSY,  and  four  assumptions  about  the  stock-
recruitment  model:  Ricker  model  (thin  solid  line),      Ricker  model  with
autocorrelation  and  depensatory  mortality  at  low  spawner  abundances  (thick
solid  line),  Beverton-Holt  model  (dashed  line),  and  Larkin  model  (dotted  line),
over  a  gradient  in  equilibrium  stock  sizes  (X-axis).  Lines  for  the  Ricker,
Beverton-Holt,  and  Larkin  models  lie  almost  on  top  of  each  other  near  the
bottom X-axis.

29

n
o
i
t
a
p
r
i
t
x
e

f
o
y
t
i
l
i

b
a
b
o
r

P

Low  depensation
Moderate depensation
High depenstation

1.0

0.8

0.6

0.4

0.2

0.0

0

100
Spawner abundance at equilibrium (1000s of fish)

60

80

40

20

Figure  15.  Probabilities  of  extirpation  over  the  long  term  (100  years)  for  simulated
populations of Pacific salmon under a constant fishing mortality rate policy equal
to  the  lower  benchmarks,  FMSY,  and  three  assumptions  about  the  spawner
abundance below which depensatory mortality occurs: 500 fish (thick solid line);
1000  fish  (thin  solid  line);  7000  (dashed  line),  over  a  gradient  in  equilibrium
stock sizes (X-axis).

30

n
o
i
t
a
p
r
i
t
x
e

f
o
y
t
i
l
i

b
a
b
o
r

P

30 years of historical data
20 years of historical data
15 years of historical data

1.0

0.8

0.6

0.4

0.2

0.0

0

100
Spawner abundance at equilibrium (1000s of fish)

60

40

80

20

Figure  16.  Probabilities  of  extirpation  over  the  long  term  (100  years)  for  simulated
populations of Pacific salmon under a constant fishing mortality rate policy equal
to the lower benchmarks, FMSY, and three assumptions about the number of years
of  historical  data  used  to  estimate  FMSY  when  deriving  the  lower  benchmark
(corresponding to the magnitude of assessment uncertainty): 30 years (thin solid
line),  20  years  (thick  solid  line),  and  15  years  (dashed  line),  over  a  gradient  in
equilibrium stock sizes (X-axis).

31

n
o

i
t

a
p
r
i
t
x
e

f

o
y
t
i
l
i

b
a
b
o
r

P

Low  outcome uncertainty
High outcome uncertainty

1.0

0.8

0.6

0.4

0.2

0.0

0

100
Spawner abundance at equilibrium (1000s of fish)

40

60

80

20

Figure  17.  Probabilities  of  extirpation  over  the  long  term  (100  years)  for  simulated
populations of Pacific salmon under a constant fishing mortality rate policy equal
to  the  lower  benchmarks,  FMSY,  and  two  assumptions  about  the  magnitude  of
outcome  uncertainty:  standard  deviation  between  realized  harvest  rates  and
targets  =  0.097  (thin  solid  line)  and  0.19  (thick  solid  line),  over  a  gradient  in
equilibrium stock sizes (X-axis).

3.2  Model 2: Probability of recovery to SMSY in one (or three) generations

3.2.1  Lower benchmarks on spawner abundances

Populations  with  initial  spawner  abundances  equivalent  to  the  lower  benchmarks
derived from S at 50-90% of RMSY (black circles labeled 50-90% of RMSY, Figure 18a), S at
50% of RMAX (red circle), and 40% of SMSY (blue circle) had high probabilities of recovery
to SMSY within one generation in the absence of commercial and recreational fishing (>75%
probability,  definition  adapted  from  DFO's  "Fishery  decision-making  framework
incorporating  the  Precautionary  Approach"  (2009))  (Figure  18a).  Populations  that  were
initialized at Sgen (green circle, Figure 18a) and S at 30-40% of RMSY (black circles labeled
30-40%  of  RMSY,  Figure  18a)  had  moderately  high  probabilities  of  recovery  within  one
generation  (50-75%).  Probability  of  recovery  within  three  generations  were  high  or  very
high (>75% or >95% probability, respectively) for all benchmarks (Figure 18b).

32

Y
S
M
S
o
t

y
r
e
v
o
c
e
r

f
o
y
t
i
l
i

b
a
b
o
r
P

1.0

0.8

0.6

0.4

0.2

0.0

(a)

(b)

1.0

0.8

0.6

0.4

0.2

0.0

%
0
1

%
0
2

%
0
3

%
0
4

%
0
5

%
0
6

%
0
7

%
0
8

%
0
9

X
A
M
R

Y
S
M
S

n
e
g
S

%
%
0
0
1
1

%
%
0
0
2
2

%
%
0
0
3
3

%
%
0
0
4
4

%
%
0
0
5
5

%
%
0
0
6
6

%
%
0
0
7
7

%
%
0
0
8
8

%
%
0
0
9
9

X
X
A
A
M
M
R
R

Y
Y
S
S
M
M
S
S

n
n
e
e
g
g
S
S

Spawner abundance
at percentage of
RMSY

f

o
%
0
4

f

o
%
0
5

t

a
S

Spawner abundance
Spawner abundance
at percentage of
at percentage of
RMSY
RMSY

f
f

o
o
%
%
0
0
4
4

f
f

o
o
%
%
0
0
5
5

t
t

a
a
S
S

Figure 18. Probabilities of recovery over one (a) and three (b) generation(s) for simulated
populations  of  Pacific  salmon  from  lower  benchmark  on  spawner  abundances
listed  on  the  X-axis,  in  the  absence  of  commercial  and  recreational  fishing.
Lower benchmarks derived from spawner abundances at various percentages of
RMSY  (black  solid  circles)  are  compared  with  three  other  lower  benchmarks:
spawner abundances at 50% of RMAX (red circle), 40% of SMSY (blue circle), and
spawner  abundance  resulting  in  recovery  to  SMSY  in  one  generation  without
fishing under equilibrium conditions, Sgen (green circle).

When we assumed populations were highly productive (mean Ricker "a" value = 2.0,
equivalent  to  7.4  recruits/spawner  at  low  spawner  abundances),  probabilities  of  recovery
within one generation were high (>75% probability) for all benchmarks except for S at 10-
20%  of  RMSY  (Figure  19).  In  contrast,  when  we  assumed  populations  were  relatively
unproductive  (mean  "a"  value  =  0.5,  equivalent  to  1.6  recruits/spawner  at  low  spawner
abundances), probabilities of recovery were moderately high (50-75%) for S at 50-90% of
RMSY,  S  at  50%  of  RMAX  and  Sgen,  and  low  for  the  remaining  benchmarks.  Similar  to  the
results  for  probability  of  extirpation  over  the  long  term,  those  differences  were  relatively
minor  for  the  benchmark  based  on  Sgen  (green  circles;  i.e.,  performance  of  Sgen  was
relatively  insensitive  to  variability  in  productivity  levels),  and  relatively  large  for
benchmarks based on RMSY (black circles) and SMSY (blue circles).

33

Y
S
M
S
o
t

y
r
e
v
o
c
e
r

f
o
y
t
i
l
i

b
a
b
o
r
P

1.0

0.8

0.6

0.4

0.2

0.0

%
%
0
0
1
1

%
%
0
0
2
2

%
%
0
0
3
3

%
%
0
0
4
4

%
%
0
0
5
5

%
%
0
0
6
6

%
%
0
0
7
7

%
%
0
0
8
8

%
%
0
0
9
9

Spawner abundance at
Spawner abundance at
percentage of RMSY
percentage of RMSY

n
n
e
e
g
g
S
S

Y
Y
S
S
M
M
S
S

f
f

o
o
%
%
0
0
4
4

X
X
A
A
M
M
R
R

f
f

o
o
%
%
0
0
5
5

t
t

a
a
S
S

Figure 19. Probabilities of recovery over one generation for unproductive (hollow grey and
coloured  circles),  moderately  productive  (solid  grey  and  coloured  circles),  and
highly productive (solid black and coloured circles with black outline) simulated
populations  of  Pacific  salmon  from  lower  benchmarks  on  spawner  abundances
listed on the X-axis in the absence of commercial and recreational fishing. Lower
benchmarks are the same as described in the caption to Fig. 18.

Probabilities  of  recovery  to  SMSY  were  relatively  insensitive  to  variability  in
assumptions  about  temporal  trends  in  productivity  (Figure  20),  the  form  of  the  stock-
recruitment relationship (Figure 21), the threshold below which depensation occurs (Figure
22),  number  of  years  used  to  estimate  benchmarks  (Figure  23),  magnitude  of  outcome
uncertainties  (Figure  24),  and  the  lower  limit  on  harvest  rates  (Figure  25).  In  general,
increasing uncertainty and harvest resulted in reduced probability of recovery to SMSY.

34

Y
S
M
S
o
t

y
r
e
v
o
c
e
r

f
o
y
t
i
l
i

b
a
b
o
r
P

1.0

0.8

0.6

0.4

0.2

0.0

%
%
0
0
1
1

%
%
0
0
2
2

%
%
0
0
3
3

%
%
0
0
4
4

%
%
0
0
5
5

%
%
0
0
6
6

%
%
0
0
7
7

%
%
0
0
8
8

%
%
0
0
9
9

Spawner abundance at
Spawner abundance at
percentage of RMSY
percentage of RMSY

n
n
e
e
g
g
S
S

Y
Y
S
S
M
M
S
S

f
f

o
o
%
%
0
0
4
4

X
X
A
A
M
M
R
R

f
f

o
o
%
%
0
0
5
5

t
t

a
a
S
S

Figure  20.  Probabilities  of  recovery  over  one  generation  for  simulated  populations  of
Pacific salmon that have constant productivity (Ricker "a" parameter) over time
(hollow  grey  and  coloured  circles),  linearly  increasing  productivity  (solid  grey
and  coloured  circles),  linearly  declining  productivity  (solid  black  and  coloured
circles  with  black  outline),  and  cyclic  patterns  in  productivity  (black  and
coloured asterisks), from lower benchmarks on spawner abundances listed on the
X-axis  in  the  absence  of  commercial  and  recreational  fishing.  Note,  points  are
almost  coincident  because  magnitudes  of  the  changes  in  productivity  are  small
over one generation. Lower benchmarks are the same as described in the caption
to Fig. 18.

35

Y
S
M
S
o
t

y
r
e
v
o
c
e
r

f
o
y
t
i
l
i

b
a
b
o
r
P

1.0

0.8

0.6

0.4

0.2

0.0

%
%
0
0
1
1

%
%
0
0
2
2

%
%
0
0
3
3

%
%
0
0
4
4

%
%
0
0
5
5

%
%
0
0
6
6

%
%
0
0
7
7

%
%
0
0
8
8

%
%
0
0
9
9

Spawner abundance at
Spawner abundance at
percentage of RMSY
percentage of RMSY

n
n
e
e
g
g
S
S

Y
Y
S
S
M
M
S
S

f
f

o
o
%
%
0
0
4
4

X
X
A
A
M
M
R
R

f
f

o
o
%
%
0
0
5
5

t
t

a
a
S
S

Figure  21.  Probabilities  of  recovery  over  one  generation  for  simulated  populations  of
Pacific salmon that recruit according to a Ricker model (solid grey and coloured
circles),  a  Ricker  model  with  autocorrelation  and  depensation  (solid  black  and
coloured  circles  with  black  outline),  a  Beverton-Holt  model  (hollow  grey  and
coloured circles), and a Larkin model (black and coloured asterisks), from lower
benchmarks  on  spawner  abundances  listed  on  the  X-axis  in  the  absence  of
commercial  and  recreational  fishing.  Lower  benchmarks  are  the  same  as
described in the caption to Fig. 18.

36

Y
S
M
S
o
t

y
r
e
v
o
c
e
r

f
o
y
t
i
l
i

b
a
b
o
r
P

1.0

0.8

0.6

0.4

0.2

0.0

%
%
0
0
1
1

%
%
0
0
2
2

%
%
0
0
3
3

%
%
0
0
4
4

%
%
0
0
5
5

%
%
0
0
6
6

%
%
0
0
7
7

%
%
0
0
8
8

%
%
0
0
9
9

Spawner abundance at
Spawner abundance at
percentage of RMSY
percentage of RMSY

n
n
e
e
g
g
S
S

Y
Y
S
S
M
M
S
S

f
f

o
o
%
%
0
0
4
4

X
X
A
A
M
M
R
R

f
f

o
o
%
%
0
0
5
5

t
t

a
a
S
S

Figure  22.  Probabilities  of  recovery  over  one  generation  for  simulated  populations  of
Pacific salmon that recruit according to a Ricker model with autocorrelation and
depensatory  mortality  at  low  spawner  abundances,  i.e.,  below  500  spawners,
1000  spawners,  and  7000  spawners,  from  lower  benchmarks  on  spawner
abundances listed on the X-axis, in the  absence of commercial and recreational
fishing.  Note,  points  for  different  threshold  levels  below  which  depensation
occurs  are  exactly  coincident  (i.e.,  the  probability  of  recovery  is  insensitive  to
threshold level).  Lower benchmarks are the same as described in the caption to
Fig. 18.

37

Y
S
M
S
o
t

y
r
e
v
o
c
e
r

f
o
y
t
i
l
i

b
a
b
o
r
P

1.0

0.8

0.6

0.4

0.2

0.0

%
%
0
0
1
1

%
%
0
0
2
2

%
%
0
0
3
3

%
%
0
0
4
4

%
%
0
0
5
5

%
%
0
0
6
6

%
%
0
0
7
7

%
%
0
0
8
8

%
%
0
0
9
9

Spawner abundance at
Spawner abundance at
percentage of RMSY
percentage of RMSY

n
n
e
e
g
g
S
S

Y
Y
S
S
M
M
S
S

f
f

o
o
%
%
0
0
4
4

X
X
A
A
M
M
R
R

f
f

o
o
%
%
0
0
5
5

t
t

a
a
S
S

Figure  23.  Probabilities  of  recovery  over  one  generation  for  simulated  populations  of
Pacific salmon from lower benchmarks on spawner abundances listed on the X-
axis,  derived  from  historical  time  series  of  length  15  years  (solid  black  and
coloured  circles  with  black  outline),  20  years  (solid  grey  and  coloured  circles),
and  30  years  (hollow  grey  and  coloured  circles),  in  the  absence  of  commercial
and  recreational  fishing.  Lower  benchmarks  are  the  same  as  described  in  the
caption to Fig. 18.

38

Y
S
M
S
o
t

y
r
e
v
o
c
e
r

f
o
y
t
i
l
i

b
a
b
o
r
P

1.0

0.8

0.6

0.4

0.2

0.0

%
%
0
0
1
1

%
%
0
0
2
2

%
%
0
0
3
3

%
%
0
0
4
4

%
%
0
0
5
5

%
%
0
0
6
6

%
%
0
0
7
7

%
%
0
0
8
8

%
%
0
0
9
9

Spawner abundance at
Spawner abundance at
percentage of RMSY
percentage of RMSY

n
n
e
e
g
g
S
S

Y
Y
S
S
M
M
S
S

f
f

o
o
%
%
0
0
4
4

X
X
A
A
M
M
R
R

f
f

o
o
%
%
0
0
5
5

t
t

a
a
S
S

Figure  24.  Probabilities  of  recovery  over  one  generation  for  simulated  populations  of
Pacific salmon with low outcome uncertainties (solid grey and coloured circles)
and  high  outcome  uncertainties  (solid  black  and  coloured  circles  with  black
outline), from lower benchmarks on spawner abundances listed on the X-axis, in
the  absence  of  commercial  and  recreational  fishing.  Lower  benchmarks  are  the
same as described in the caption to Fig. 18.

39

Y
S
M
S
o
t

y
r
e
v
o
c
e
r

f
o
y
t
i
l
i

b
a
b
o
r
P

1.0

0.8

0.6

0.4

0.2

0.0

%
%
0
0
1
1

%
%
0
0
2
2

%
%
0
0
3
3

%
%
0
0
4
4

%
%
0
0
5
5

%
%
0
0
6
6

%
%
0
0
7
7

%
%
0
0
8
8

%
%
0
0
9
9

Spawner abundance at
Spawner abundance at
percentage of RMSY
percentage of RMSY

n
n
e
e
g
g
S
S

Y
Y
S
S
M
M
S
S

f
f

o
o
%
%
0
0
4
4

X
X
A
A
M
M
R
R

f
f

o
o
%
%
0
0
5
5

t
t

a
a
S
S

Figure  25.  Probabilities  of  recovery  over  one  generation  for  simulated  populations  of
Pacific salmon from lower benchmarks on spawner abundances listed on the X-
axis, in the absence of commercial and recreational fishing but with non-targeted
harvest rate (e.g., from a test fishery and by-catch) of ht = 0.02 (hollow grey and
coloured  circles),  ht  =  0.1  (solid  grey  and  coloured  circles)  and  ht  =  0.2  ((solid
black and coloured circles with black outline). Lower benchmarks are the same
as described in the caption to Fig. 18.

3.2.2  Lower benchmarks on fishing mortality

When populations were subjected to fishing mortalities equal to the lower benchmarks,
70-150%  of  FMSY,  FMAX,  and  FMED,  the  probabilities  of  recovery  to  SMSY  within  one
generation  were  moderately  low  or  low  (probabilities  <50%  (Figure  26a).  Only  lower
benchmarks,  40-50%  of  FMSY  had  probabilities  of  recovery  to  SMSY  >  50%  within  one
generation.  However,  when  the  time  frame  of  recovery  was  extended  from  one  to  three
generations,  probabilities  of  recovery  were  high  (>75%  probability)  for  the  benchmarks,
50-100% FMSY, and moderately high (50-75% probability) for benchmarks, 110-140% FMSY

40

and FMED (Figure 26b). When we assumed that the population was highly productive, (mean
Ricker "a" = 2.0), probabilities of  recovery within one generation increased to > 50% for
benchmarks, 50-90% FMSY, but remained low for the other benchmarks (Figure 27). When
we assumed the population was unproductive (mean Ricker "a" = 0.5), the probabilities of
recovery within one generation were low for all benchmarks (probabilities <25%) (Figure
27).

Y
S
M
S
o
t

1.0

0.8

y
r
e
v
o
c
e
r

f

o
y
t
i
l
i

b
a
b
o
r
P

0.6

0.4

0.2

0.0

(a)

%
%
0
0
5
5

%
%
0
0
6
6

%
%
0
0
7
7

%
%
0
0
8
8

%
%
0
0
9
9

%
%
0
0
0
0
1
1

%
%
0
0
1
1
1
1

%
%
0
0
2
2
1
1

%
%
0
0
3
3
1
1

%
%
0
0
4
4
1
1

%
%
0
0
5
5
1
1

Fishing mortality at
Fishing mortality at
percentage of FMSY
percentage of FMSY

Y
Y
S
S
M
M
F
F

X
X
A
A
M
M
F
F

D
D
E
E
M
M
F
F

1.0

0.8

0.6

0.4

0.2

0.0

(b)

%
%
0
0
5
5

%
%
0
0
6
6

%
%
0
0
7
7

%
%
0
0
8
8

%
%
0
0
9
9

%
%
0
0
0
0
1
1

%
%
0
0
1
1
1
1

%
%
0
0
2
2
1
1

%
%
0
0
3
3
1
1

%
%
0
0
4
4
1
1

%
%
0
0
5
5
1
1

Fishing mortality at
Fishing mortality at
percentage of FMSY
percentage of FMSY

Y
Y
S
S
M
M
F
F

X
X
A
A
M
M
F
F

D
D
E
E
M
M
F
F

Figure 26. Probabilities of recovery over one (a) and three (b) generation(s) for simulated
populations  of  Pacific  salmon  managed  according  to  the  lower  benchmark  on
fishing  mortality  listed  on  the  X-axis,  in  the  absence  of  commercial  and
recreational fishing. Lower benchmarks derived from fishing mortality at various
percentages  of  FMSY  (black  solid  circles)  are  compared  with  three  other  lower
benchmarks: FMSY (red circle), maximum loge(R/S) at low spawner abundances,
FMAX (blue circle), and median loge(R/S), FMED (green circle).

41

Y
S
M
S
o
t

y
r
e
v
o
c
e
r

f
o
y
t
i
l
i

b
a
b
o
r
P

1.0

0.8

0.6

0.4

0.2

0.0

%
%
0
0
5
5

%
%
0
0
6
6

%
%
0
0
7
7

%
%
0
0
8
8

%
%
0
0
9
9

%
%
0
0
0
0
1
1

%
%
0
0
1
1
1
1

%
%
0
0
2
2
1
1

%
%
0
0
3
3
1
1

%
%
0
0
4
4
1
1

%
%
0
0
5
5
1
1

Y
Y
S
S
M
M
F
F

X
X
A
A
M
M
F
F

D
D
E
E
M
M
F
F

Fishing mortality at
Fishing mortality at
percentage of FMSY
percentage of FMSY

Figure 27. Probabilities of recovery over one generation for unproductive (hollow grey and
coloured  circles),  moderately  productive  (solid  grey  and  coloured  circles),  and
highly productive (solid black and coloured circles with black outline) simulated
populations  of  Pacific  salmon  managed  according  to  the  lower  benchmarks  on
fishing  mortality  listed  on  the  X-axis,  in  the  absence  of  commercial  and
recreational fishing. Lower benchmarks are the same as described in the caption
to Fig. 26.

Similar  to  the  results  for  benchmarks  on  spawner  abundances,  probabilities  of
recovery for benchmarks on fishing  mortality  were  relatively  insensitive  to  time  trends  in
productivity  (Figure  28),  the  form  of  the  stock-recruitment  model  (Figure  29),  threshold
level in spawner abundances below which depensation occurs (Figure 30), number of years
of historical data used to estimate benchmarks (Figure 31), and the magnitude of outcome
uncertainties (Figure 32). In general, increasing uncertainty and harvest resulted in reduced
probability  of  recovery.  For  one  exception,  increasing  outcome  uncertainty  resulted  in  a
higher  probability  of  recovery  because  occasional  low  harvest  rates  (below  targets)
improved  performance  (increased  probability  of  recovery)  more  than  high  harvest  rates
reduced performance.

42

Y
S
M
S
o
t

y
r
e
v
o
c
e
r

f
o
y
t
i
l
i

b
a
b
o
r
P

1.0

0.8

0.6

0.4

0.2

0.0

%
%
0
0
5
5

%
%
0
0
6
6

%
%
0
0
7
7

%
%
0
0
8
8

%
%
0
0
9
9

%
%
0
0
0
0
1
1

%
%
0
0
1
1
1
1

%
%
0
0
2
2
1
1

%
%
0
0
3
3
1
1

%
%
0
0
4
4
1
1

%
%
0
0
5
5
1
1

Y
Y
S
S
M
M
F
F

X
X
A
A
M
M
F
F

D
D
E
E
M
M
F
F

Fishing mortality at
Fishing mortality at
percentage of FMSY
percentage of FMSY

Figure  28.  Probabilities  of  recovery  over  one  generation  for  simulated  populations  of
Pacific salmon that have constant productivity (Ricker "a" parameter) over time
(hollow  grey  and  coloured  circles),  linearly  increasing  productivity  (solid  grey
and  coloured  circles),  linearly  declining  productivity  (solid  black  and  coloured
circles  with  black  outline),  and  cyclic  patterns  in  productivity  (black  and
coloured  asterisks),  managed  according  to  the  lower  benchmarks  on  fishing
mortality  listed  on  the  X-axis  in  the  absence  of  commercial  and  recreational
fishing. Note, points are almost coincident because magnitude of the changes in
productivity  are  small  over  one  generation.  Lower  benchmarks  are  the  same  as
described in the caption to Fig. 26.

43

Y
S
M
S
o
t

y
r
e
v
o
c
e
r

f
o
y
t
i
l
i

b
a
b
o
r
P

1.0

0.8

0.6

0.4

0.2

0.0

%
%
0
0
5
5

%
%
0
0
6
6

%
%
0
0
7
7

%
%
0
0
8
8

%
%
0
0
9
9

%
%
0
0
0
0
1
1

%
%
0
0
1
1
1
1

%
%
0
0
2
2
1
1

%
%
0
0
3
3
1
1

%
%
0
0
4
4
1
1

%
%
0
0
5
5
1
1

Y
Y
S
S
M
M
F
F

X
X
A
A
M
M
F
F

D
D
E
E
M
M
F
F

Fishing mortality at
Fishing mortality at
percentage of FMSY
percentage of FMSY

Figure  29.  Probabilities  of  recovery  over  one  generation  for  simulated  populations  of
Pacific  salmon  that  recruit  according  to  a  Ricker  model  (hollow  grey  and
coloured  circles),  a  Ricker  model  with  autocorrelation  and  depensation  (solid
grey  and  coloured  circles),  a  Beverton-Holt  model  (solid  black  and  coloured
circles  with  black  outline),  and  a  Larkin  model  (black  and  coloured  asterisks),
managed according to the lower benchmarks on fishing mortality listed on the X-
axis  in  the  absence  of  commercial  and  recreational  fishing.  Lower  benchmarks
are the same as described in the caption to Fig. 26.

44

Y
S
M
S
o
t

y
r
e
v
o
c
e
r

f
o
y
t
i
l
i

b
a
b
o
r
P

1.0

0.8

0.6

0.4

0.2

0.0

%
%
0
0
5
5

%
%
0
0
6
6

%
%
0
0
7
7

%
%
0
0
8
8

%
%
0
0
9
9

%
%
0
0
0
0
1
1

%
%
0
0
1
1
1
1

%
%
0
0
2
2
1
1

%
%
0
0
3
3
1
1

%
%
0
0
4
4
1
1

%
%
0
0
5
5
1
1

Y
Y
S
S
M
M
F
F

X
X
A
A
M
M
F
F

D
D
E
E
M
M
F
F

Fishing mortality at
Fishing mortality at
percentage of FMSY
percentage of FMSY

Figure  30.  Probabilities  of  recovery  over  one  generation  for  simulated  populations  of
Pacific salmon that recruit according to a Ricker model with autocorrelation and
depensatory  mortality  at  low  spawner  abundances,  i.e.,  below  500  spawners,
1000 spawners, and 7000 spawners, managed according to the lower benchmarks
on  fishing  mortality  listed  on  the  X-axis,  in  the  absence  of  commercial  and
recreational  fishing.  Note,  points  for  different  threshold  levels  below  which
depensation  occurs  are  exactly  coincident  (i.e.,  the  probability  of  recovery  is
insensitive to threshold level).  Lower benchmarks are the same as described in
the caption to Fig. 26.

45

Y
S
M
S
o
t

y
r
e
v
o
c
e
r

f
o
y
t
i
l
i

b
a
b
o
r
P

1.0

0.8

0.6

0.4

0.2

0.0

%
%
0
0
5
5

%
%
0
0
6
6

%
%
0
0
7
7

%
%
0
0
8
8

%
%
0
0
9
9

%
%
0
0
0
0
1
1

%
%
0
0
1
1
1
1

%
%
0
0
2
2
1
1

%
%
0
0
3
3
1
1

%
%
0
0
4
4
1
1

%
%
0
0
5
5
1
1

Y
Y
S
S
M
M
F
F

X
X
A
A
M
M
F
F

D
D
E
E
M
M
F
F

Fishing mortality at
Fishing mortality at
percentage of FMSY
percentage of FMSY

Figure  31.  Probabilities  of  recovery  over  one  generation  for  simulated  populations  of
Pacific salmon managed according to the lower benchmarks on fishing mortality
listed on the X-axis, derived from historical time series of length 15 years (solid
black and coloured circles with black outline), 20 years (solid grey and coloured
circles),  and  30  years  (hollow  grey  and  coloured  circles),  in  the  absence  of
commercial  and  recreational  fishing.  Lower  benchmarks  are  the  same  as
described in the caption to Fig. 26.

46

Y
S
M
S
o
t

y
r
e
v
o
c
e
r

f
o
y
t
i
l
i

b
a
b
o
r
P

1.0

0.8

0.6

0.4

0.2

0.0

%
%
0
0
5
5

%
%
0
0
6
6

%
%
0
0
7
7

%
%
0
0
8
8

%
%
0
0
9
9

%
%
0
0
0
0
1
1

%
%
0
0
1
1
1
1

%
%
0
0
2
2
1
1

%
%
0
0
3
3
1
1

%
%
0
0
4
4
1
1

%
%
0
0
5
5
1
1

Y
Y
S
S
M
M
F
F

X
X
A
A
M
M
F
F

D
D
E
E
M
M
F
F

Fishing mortality at
Fishing mortality at
percentage of FMSY
percentage of FMSY

Figure  32.  Probabilities  of  recovery  over  one  generation  for  simulated  populations  of
Pacific salmon with low outcome uncertainties (solid grey and coloured circles)
and  high  outcome  uncertainties  (solid  black  and  coloured  circles  with  black
outline), managed according to the lower benchmarks on fishing mortality listed
on  the  X-axis,  in  the  absence  of  commercial  and  recreational  fishing.  Lower
benchmarks are the same as described in the caption to Fig. 26.

47

4.  RECOMMENDATIONS

Although results from simulation models such as the one described here are typically
highly  sensitive  to  assumptions  about  model  structure  and  parameterization  (Dulvy  et  al.,
2004), the relative performance of candidate management decisions (or lower benchmarks
for status assessment) and their sensitivities to alternative model assumptions can provide
useful information when evaluating management options (Mace et al., 2008).  For metrics
of spawner abundances, we suggest deriving a lower benchmark from Sgen, the abundance
of spawner that will result in rebuilding to SMSY under equilibrium conditions in the absence
of fishing, because in our simulation model, the performance of Sgen (i.e., the probabilities
of extirpation and recovery to a target) was more robust to variability in stock productivity
than  benchmarks  calculated  from  proportions  of  SMSY,  SMAX,  or  S  at  proportions  of  RMSY.
Sgen  was  also  associated  with  a  relatively  low  probability  of  extirpation  over  100  years
(probability <25%) for populations with equilibrium spawner abundances >15 000 fish, and
high probability of recovery within three generations (probability >75%). Sgen was chosen
by  the  BC  Ministry  of  the  Environment  as  a  limit  reference  point  (a  level  of  abundance
"that  defines  a  highly  undesired  state"  (Johnston  et  al.,  2002,  p.4))  for  steelhead,
Oncorhynchus mykiss, based on the results of a similar simulation modelling exercise. They
further suggested that in the absence of data on stock productivity to calculate Sgen, 15% of
carrying capacity (or between 10% and 20%) be used as a proxy lower reference point.

For  metrics  of  fishing  mortality,  we  suggest  deriving  a  lower  benchmark  from  FMSY
(fishing mortality at maximum sustained yield) because the probability of recovery for that
benchmark was more robust to variability in stock productivity than benchmarks calculated
from proportions of FMSY, FMAX, or FMED. In addition, FMSY was associated with a relatively
low  probability  of  extirpation  over  100  years  (probability  <25%)  when  equilibrium
abundances were > 30,000 fish, and high probability of recovery within three generations
(probability  >75%).  Furthermore,  that  choice  is  consistent  with  the  recommendation  of
FMSY as a "limit reference point" by the UN Straddling Fish Stocks and Highly Migratory
Fish Stocks Agreement (1995).

48

5.  LITERATURE CITED

Cass, A., Folkes, M., Pestal, G., 2003. Methods for assessing harvest rules for Fraser River

sockeye salmon. DFO Can. Sci. Advis. Sec. Res. Doc. 2004/025.

Chen, D.G., Irvine, J.R., Cass, A.J., 2002. Incorporating allee effects in fish stock-

recruitment models and applications for determining reference points. Canadian
Journal of Fisheries and Aquatic Sciences 59, 242-249.

Dulvy, N.K., Ellis, J.R., Goodwin, N.B., Grant, A., Reynolds, J.D., Jennings, S., 2004.

Methods of assessing extinction risk in marine fishes. Fish & Fisheries 5, 255-276.

Fisheries and Oceans Canada, 2009. Fishery decision-making framework incorporating the

precautionary approach. Available at: http://www.dfo-mpo.gc.ca/fm-gp/peches-
fisheries/fish-ren-peche/sff-cpd/precaution-eng.htm.

Holt, C.A., 2007. Characterizing and Accounting for Uncertainties in Pacific Salmon
Fisheries. School of Resource and Environmental Management. Simon Fraser
University, Burnaby, British Columbia, p. 227.

Holt, C.A., Cass, A., Holtby, B. and Riddell, B. 2009. Indicators of Status and Benchmarks

for Conservations Units in Canada's Wild Salmon Policy. DFO. Can. Sci. Advis.
Sec. Res. Doc. 2009/058

Holt, C.A., Peterman, R.M., 2006. Missing the target: implementation uncertainties in

fisheries on Fraser River, British Columbia, sockeye salmon (Oncorhynchus nerka).
Canadian Journal of Fisheries and Aquatic Sciences 63, 2722-2733.

Holt, C.A., Peterman, R.M., 2008. Uncertainties in population dynamics and outcomes of

regulations in sockeye salmon (Oncorhynchus nerka) fisheries: implications for
management. Canadian Journal of Fisheries and Aquatic Science 65, 1459-1474.

Johnston, N.T., Parkinson, E.A., Tautz, A.F., Ward, B.R., 2002. A Conceptual Framework
for the Management of Steelhead, Oncorhynchus mykiss. Fisheries Project Report
No. RD101. Ministry of Water, Land, and Air Protection, BC Fisheries Branch,
Vancouver, British Columbia.

Korman, J., Peterman, R.M., Walters, C.J., 1995. Empirical and theoretical analyses of

correction of time series bias in stock-recruitment  relationships of sockeye salmon.
Canadian Journal of Fisheries and Aquatic Sciences 52, 2174-2189.

Mace, G.M., Collar, N.J., Gaston, K.J., Hilton-Taylor, C., Akçakaya, H.R., Leader-

Williams, N., Milner-Gulland, E.J., Stuart, S.N., 2008. Quantification of Extinction
Risk: IUCN's System for Classifying Threatened Species. Conservation Biology 22,
1424-1442.

49

Parken, C.K., McNicol, R.E., Irvine, J.R., 2006. Habitat-based methods to estimate

escapement goals for data limited Chinook salmon stocks in British Columbia,
2004. DFO Can. Sci. Advis. Sec. Res. Doc. 2006/083.

Schnute, J.T., Richards, L.J., 1995. The influence of error on population estimates from
catch-age models. Canadian Journal of Fisheries and Aquatic Sciences 52, 2063-
2077.

Shortreed, K.S., Morton, K.F., Malange, K., Hume, J.M.B., 2001. Factors Limiting Juvenile

Sockeye Production and Enhancement Potential for Selected B.C. Nursery Lakes.
DFO Can. Sci. Advis. Sec. Res. Doc 2001/098.

UN. 1995. Straddling Fish Stocks and Highly Migratory Fish Stocks Agreement.

Walters, C.J., Martell, S.J.D., 2004. Fisheries Ecology and Management. Princeton

University Press, Princeton.

Wood, C.C., 1987. Predation of juvenile Pacific salmon by the common merganser (Mergus
merganser) on eastern Vancouver Island. I: predation during the seaward migration.
Canadian Journal of Fisheries and Aquatic Sciences 44, 941-949.

50


