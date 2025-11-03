GUIDE TO THE WSP STATUS DASHBOARDS

V4 2025-05-28

Introduction

The WSP status dashboards are a  condensed summary of information to support the WSP rapid
status process.. The dashboards have been effective once a Working Group has become
comfortable with the WSP status assessment framework. This requires familiarity with the WSP-
specific technical jargon, details of the established methods, and interpretation of the dashboard
figures (Holt 2009; Holt et al. 2009; Pestal et al. 2023; DFO 2024).

Key points:

•  WSP status assessments focus on 4 standard metrics: relative abundance, absolute

abundance, long-term trend, and percent change.

•  Annual metric values are compared to metric-specific upper and lower benchmarks to

assign a status category for each individual metric.

•  A decision tree (DFO 2024) is used to combine information across available metrics. The
structure and threshold values of the decision tree are designed to capture the expert
consensus from a series of previously completed status assessment workshops. Note that
threshold values used in the decision tree do not always align with the metric benchmarks
because they represent how the metrics are interpreted and applied by experts when
determining statuses.

The dashboards show (1) details for the four standard metrics and their benchmarks, and (2) a
summary of the annual status categories of the individual metrics and the annual WSP status
results determined by the decision tree.

For more information refer to the following online resources:

•  The WSPMetrics R Package has functions to calculate the standard WSP metrics and apply

the status decision tree.

•  The WSP Rapid Status Worked Examples repository has a step-by-step implementation,

showing source data, metric specifications, R script to calculate the metrics and apply the
decision tree, and resulting status dashboards. This repository also has a description of the
decision tree and provides links to all of the technical documentation.

For question and feedback, please contact:

•  Sue Grant (Sue.Grant@dfo-mpo.gc.ca)
•  Gottfried Pestal (gottfried.pestal@solv.ca)
•  Bronwyn MacDonald (Bronwyn.MacDonald@dfo-mpo.gc.ca)

1

Field Code Changed

Identifying Information: Species, CU
Name, Stock Management Unit, Type of data
(absolute abundance or relative index)

Parts of the Dashboard

Panel 1 – Relative Abundance
Metric
Plot shows all available
spawner estimates (blue) and
the running generational
average (red) compared to
biological benchmarks
(generally Sgen and 80% Smsy
from SR model fits).
Benchmarks for this metric are
specific to each CU, reflecting
its capacity and productivity.
The relative abundance metric
is calculated using the
generational average (red line).
The vertical dashed line marks
the start of the retrospective
evaluation – i.e. the start year for
the metric statuses shown in
the lower panel. Note that the
year axis is the same for all CUs
to facilitate comparisons.
Earlier years are cut off in the
display for a few CUs, but are
used in the metric calculations

Panel 3 – Long-term Trend
Metric
The plotted blue line shows the
value of the long-term trend
metric in each year, i.e. the
ratio of the recent generational
average to the long-term
generational average.
Benchmarks for this metric are
standard across CUs. Long-
term-trend is shown only for
the retrospective evaluation
years.

Metric Summary: Summary of the
annual metric status zones for the
retrospective period (the first year
matches the vertical dashed lines
in the panels above). Status zones
are determined using the same
data and metric-specific
benchmarks shown in the 4 panels
above.

Status Summary (bottom 3 rows of the table): Results of
applying the decision tree to the available metrics for each
retrospective year. Results include a status designation
(Red/Amber/Green) and a confidence rating
(High/Moderate/Low) which reflects the type of information used
to assign status (i.e., higher confidence is assigned to statuses
that are determined using the abundance relative to biological
benchmarks than to statuses that are assigned based solely on
trends). Where available, the bottom row shows results from
completed integrated status assessment workshops.

Panel 2 - Absolute Abundance
Metric.
Plot shows all available spawner
estimates (blue) and the running
generational average (red). This
is the same data shown in panel
1, but (1) it is being plotted on a
log-scale to highlight low
abundance years, and (2) it is
being compared to different
benchmarks, i.e. the absolute
abundance benchmarks.  The
generational average (red line) is
used to calculate this metric.
Benchmarks for this metric are
standard across CUs, regardless
of species or life history type, but
the metric is only used if
estimates of total spawner
abundance are available, as
determined by CU experts. The
vertical dashed line marks the
start of the retrospective
evaluation - i.e. the start year for
the metric statuses shown in the
lower panel.

Panel 4 – Percent Change Metric
The plotted blue line shows the
value of the percent change
metric in each year, i.e. the
percent change over 3
generations (slope). This metric is
also called the short-term trend.
Depending on species, life-
history, and data availability, data
used to calculate the percent
change metric may be log-
transformed and/or smoothed.
Benchmarks for this metric are
standard across CUs. Percent
change is shown only for the
retrospective evaluation years.

2

Special Case: Reference Line Only

There are some instances where the relative abundance metric is not usable for a CU, but the
expert review process identified CU-specific biological benchmarks that are considered interesting
as contextual information. Examples include South Thompson Summer 1.3 Chinook and Middle
Fraser  Summer 1.3 Chinook.

In these cases, Panel 1 of the dashboard shows the spawner abundance time series (blue line) with
dashed horizontal reference lines that indicate the CU-specific benchmarks. The panel is not
shaded into corresponding status zones, the status of the relative abundance metric is not
determined, and the relative abundance metric row of the metric summary is left blank. The relative
abundance metric is not used to determine status in these cases.

Special Case: Highly Cyclic CUs

The relative abundance metric is applied differently for highly cyclic CUs, following how this metric
was interpreted and used in previously-completed status assessment workshops. Examples
include Takla-Trembleur-Early Stuart Sockeye and Shuswap Late Sockeye. The relative abundance
metric is determined using the most recent dominant cycle abundance in each year instead of the
recent generational average. This is reflected in the Panel 1 plots for highly cyclic CUs, which
highlight the dominant cycle years with a red circle and do not show the recent generational
average. Key references (Grant et al. 2011, 2020; Grant and Pestal 2013; Pestal et al. 2023).

3

Key references

DFO. 2024. Rapid status approximations for Pacific salmon derived from integrated status

assessments under DFO’s Wild Salmon Policy. CSAS Sci. Resp. 2024/004: 42 p. Available
from https://waves-vagues.dfo-mpo.gc.ca/library-bibliotheque/41207890.pdf.

Grant, S.C.H., Holt, C.A., Pestal, G., Davis, B.M., and MacDonald, B.L. 2020. The 2017 Fraser

Sockeye salmon (Oncorhynchus nerka) integrated biological status re-assessments under the
Wild Salmon Policy using standardized metrics and expert judgement. Can. Sci. Advis. Sec.
Res. Doc. 2020/038: vii+ 211. Available from http://www.dfo-mpo.gc.ca/csas-
sccs/Publications/ResDocs-DocRech/2020/2020_038-eng.pdf.

Grant, S.C.H., MacDonald, B.L., Cone, T.E., Holt, C.A., Cass, A., Porszt, E.J., Hume, J.M.B., and
Pon, L.B. 2011. Evaluation of uncertainty in Fraser sockeye (Oncorhynchus nerka) Wild
Salmon Policy status using abundance and trends in abundance metrics. Can. Sci. Advis. Sec.
Res. Doc. 2011/087: viii + 183 pp. Available from
https://publications.gc.ca/collections/collection_2019/mpo-dfo/fs70-5/Fs70-5-2019-011-
eng.pdf.

Grant, S.C.H., and Pestal, G. 2013. Integrated biological status assessments under the Wild

Salmon Policy using standardized metrics and expert judgement: Fraser River sockeye salmon
(Oncorhynchus nerka) case studies. Can. Sci. Advis. Sec. Res. Doc. 2012/106: v + 132 pp.
Available from https://waves-vagues.dfo-mpo.gc.ca/Library/349637.pdf.

Holt, C.A. 2009. Evaluation of benchmarks for conservation units in Canada’s Wild Salmon Policy:
technical documentation. Can. Sci. Advis. Sec. Res. Doc. 2009/059: x + 50 pp. Available from
https://www.dfo-mpo.gc.ca/csas-sccs/publications/resdocs-docrech/2009/2009_059-
eng.htm.

Holt, C.A., Cass, A., Holtby, B., and Riddell, B. 2009. Indicators of status and benchmarks for
Conservation Units in Canada’s Wild Salmon Policy. Can. Sci. Advis. Sec. Res. Doc.
2009/058: viii + 74 pp. Available from https://www.dfo-mpo.gc.ca/csas-
sccs/publications/resdocs-docrech/2009/2009_058-eng.htm.

Pestal, G., MacDonald, B.L., Grant, S.C.H., and Holt, C.A. 2023. State of The Salmon: rapid status
assessment approach for Pacific salmon under Canada’s Wild Salmon Policy. Can. Tech.
Rep. Fish. Aquat. Sci. 3570. : xiv + 200 pp. Available from https://waves-vagues.dfo-
mpo.gc.ca/library-bibliotheque/41207890.pdf.

4

5


