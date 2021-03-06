# -*- coding: utf-8 -*-
"""Let's Infer Statistically: State Of Indian Birds.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_mSWlhPua3tc15qGLpwlM2npXM_Z5Vwy

In statistics,  Levene's test is an inferential statistic used to assess the equality of variances for a variable calculated for two or more groups.

Классический непараметрический критерий согласия Андерсона — Дарлинга  предназначен для проверки простых гипотез о принадлежности анализируемой выборки полностью известному закону (о согласии эмпирического распределения  и теоретического закона

Источник - https://www.kaggle.com/code/shreyasajal/let-s-infer-statistically-state-of-indian-birds#Long-term-Trend-(%)

Плотли в колабе
"""

import plotly
plotly.io.renderers.default = 'colab'

# Commented out IPython magic to ensure Python compatibility.
!pip install chart_studio
!pip install openpyxl
import warnings
warnings.filterwarnings('ignore')
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
# %matplotlib inline
import matplotlib.pyplot as plt  # Matlab-style plotting
import seaborn as sns
color = sns.color_palette()
sns.set_style('darkgrid')
from plotly import tools
import chart_studio.plotly as py
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.figure_factory as ff
from IPython.display import HTML, Image
from scipy import stats
from scipy.stats import norm, skew #for some statistics



data = pd.read_excel('State of Indias Birds - Essentials.xlsx', sheet_name = 'Information', engine = 'openpyxl')
data.head()

data.describe().transpose()

"""### First Look- List of continuous and categorical features; data info"""

cont_features = [i for i in data.columns if data[i].nunique()>10]
cat_features=[i for i in data.columns if data[i].nunique()<=10]

cont_features

data['Common Name (India Checklist)'].value_counts()

cat_features

data.info()

data = data.dropna()

"""### Normality Check- Continuous Features:

Test for Normality Of Features(A pre requirement for parametric hypothesis tests): We check whether our continuous features are normal/not through:



*   Boxplots(to check for outliers causing non normality)
*   Distplots
*   Q-Q PLOTS
*  SHAPIRO WILK TEST(tests against the null hypothesis that the distribution is normal)

Long-term Trend (%)
Mean long-term trend - percentage change in the index of abuncance in 2018 when compared to pre-year-2000
"""

from plotly.offline import iplot
import plotly.graph_objs as go

fig = go.Figure()
fig.add_trace(go.Box(y=data['Long-term Trend (%)'], name='Long-term Trend (%).)',
                marker_color = 'rgb(0, 0, 100)'))
fig.show(renderer="colab")



fig = ff.create_distplot([data['Long-term Trend (%)']],['Long-term Trend (%)'],bin_size=5,colors=['rgb(0, 0, 100)'])
iplot(fig, filename='Basic Distplot')

#Get also the QQ-plot
fig = plt.figure()
res = stats.probplot(data['Long-term Trend (%)'], plot=plt)
plt.show()

"""Shapiro Wilk Test"""

from scipy.stats import shapiro
import scipy.stats as stats
shapiro([data['Long-term Trend (%)']])

"""Since the p value<0.05(significance level),the null hypothesis is rejected and we conclude that the distribution is non normal.

## Current Annual Change
"""

fig = go.Figure()
fig.add_trace(go.Box(y=data['Current Annual Change (%)'], name='Current Annual Change(%).)',
                marker_color = 'rgb(0, 0, 100)'))

"""Видим что есть жесткие аномалии"""

Q1 = data['Current Annual Change (%)'].quantile(0.25)
Q3 = data['Current Annual Change (%)'].quantile(0.75)

IQR = Q3 - Q1

filter = (data['Current Annual Change (%)'] >= Q1 - 1.5 * IQR) & (data['Current Annual Change (%)'] <= Q3 + 1.5 *IQR)
df1=data.loc[filter]

fig = ff.create_distplot([df1['Current Annual Change (%)']],['Current Annual Change (%)'],bin_size=5,colors=['rgb(0, 0, 100)'])
iplot(fig, filename='Basic Distplot')

# Get also the QQ-plot
fig = plt.figure()
res = stats.probplot(df1['Current Annual Change (%)'], plot=plt)
plt.show()

ntA = shapiro(df1['Current Annual Change (%)'])
ntA

"""Since the p value>0.05(significance level),we fail to reject the null hypothesis and conclude that the distribution is normal

### Тест Андерсона на принадлежность к распределению
"""

from scipy.stats import anderson
result = anderson(df1['Current Annual Change (%)'])
print('Statistic: %.3f' % result.statistic)
p = 0
for i in range(len(result.critical_values)):
    sl, cv = result.significance_level[i], result.critical_values[i]
    if result.statistic < result.critical_values[i]:
        print('%.3f: %.3f, data looks normal (fail to reject H0)' % (sl, cv))
    else:
        print('%.3f: %.3f, data does not look normal (reject H0)' % (sl, cv))

"""## Distribution Range Size

Mean range size within India estimated at the resolution of occupied 25x25 km grid cells (625 sq. km.) during the last 5 years and presented in units of 10,000 sq. km
"""

fig = go.Figure()

layout = go.Layout(template= "plotly_dark")
fig.add_trace(go.Box(y=data['Distribution Range Size (units of 10,000 sq. km.)'], name='Distribution Range Size(units of 10,000 sq. km.)',
                marker_color = 'rgb(0, 0, 100)'))

fig.show()

Q1 = data['Current Annual Change (%)'].quantile(0.25)
Q3 = data['Current Annual Change (%)'].quantile(0.75)

IQR = Q3 - Q1    #IQR is interquartile range. 

filter = (data['Current Annual Change (%)'] >= Q1 - 1.5 * IQR) & (data['Current Annual Change (%)'] <= Q3 + 1.5 *IQR)
df2=data.loc[filter]

fig = ff.create_distplot([df2['Distribution Range Size (units of 10,000 sq. km.)']],['Distribution Range Size (units of 10,000 sq. km.)'],bin_size=5,colors=['rgb(0, 0, 100)'])

iplot(fig, filename='Basic Distplot')

#Get also the QQ-plot
fig = plt.figure()
res = stats.probplot(df2['Distribution Range Size (units of 10,000 sq. km.)'], plot=plt)
plt.show()

from scipy.stats import shapiro
import scipy.stats as stats
shapiro(df2['Distribution Range Size (units of 10,000 sq. km.)'])

"""INFERENCE:

Out of the 3 continuous features we were interested in,only Current Annual Change (%) has an overall normal distribution.Rest of them show deviations from normality in their distributions as we saw above.So,we will be performing the parametric statistical tests on the Current Annual Change (%) feature only.
For the non normal features, we can perform some non parametric statistical test that we will see further.
"""

cat_features

data['IUCN Status'].unique()

"""## Confidence Intervals

1.What proportion of the Bird Population has a higher chance of being Critically Endangered?

Let's obtain a 95 pct confidence interval for the population proportion of critically endangered birds.
"""

df = df1
print(df['IUCN Status'].value_counts())
n = df.shape[0]

Critic_end = df['IUCN Status'].value_counts().loc['Critically Endangered']

print("\nTotal Observation ==>",n,"\t",
      "Number of Critically Endangered Birds in our sample data ==> ",Critic_end,"\n")

import statsmodels.api as sm
print("\n95% Confidence interval with statsmodels library ==>",
      sm.stats.proportion_confint(Critic_end, n),"\n")

"""Interpretation of the result:

With 95% confidence, the population proportion of critically endangered birds is estimated to be between 0% - 0.0062%.

3.What is the average Current Annual Change (%) level for birds which are nearly threatened ?

Our task:To obtain a 95% confidence interval around the sample average Current Annual Change (%) that will contain the population average Current Annual Change (%) in 95% of the samplings.
"""

df_near_threatened=df[df['IUCN Status']=='Near Threatened']
print("\n95% C.I. with statsmodels library ==>",sm.stats.DescrStatsW(df_near_threatened['Current Annual Change (%)']).zconfint_mean())

"""Interpretation of the result:

With 95% confidence, the population average Current Annual Change (%) level for birds which are nearly threatened is estimated to be between -7.04 and -3.48
"""

import seaborn as sns
sns.set()

plt.figure(dpi=120,figsize=(8,6))
sns.distplot(df_near_threatened['Current Annual Change (%)'])

plt.axvline(x=-7.045391069166767,color = 'black',ls=':')
plt.axvline(x=-3.4893057111189485,color = 'black',ls=':')
plt.axvline(x=df_near_threatened['Current Annual Change (%)'].mean(),color='red',ls='--')


plt.xticks([-7.045391069166767, -3.4893057111189485], ['lcb', 'ucb'], rotation = 90);

plt.xlabel('Current Annual Change (%) level for birds which are nearly threatened',fontdict={'fontsize':8})
plt.ylabel('Count/Distribution',fontdict={'fontsize':8})
plt.title('Current Annual Change (%) level distribution for birds which are nearly threatened',fontdict={'fontsize':8}) 
plt.show()

"""## PARAMETRIC STATISTICAL TEST"""

data.groupby('IUCN Status').mean()

"""**We understand that averages can be distorted by variations. So let's look at between-group differences.**

### Hypothetis test 1. IUCN Status. 1-way ANOVA

**Important assumption** - vairiances for groups are the same
"""

df.columns=['Serial Number', 'Common Name (India Checklist)',
       'Scientific Name (India Checklist)', 'iucn_status', 'WLPA Schedule',
       'Analysed Long-term', 'Analysed Current', 'Long-term Trend (%)',
       'Long-term Trend CI (%)', 'annual_change',
       'Current Annual Change CI (%)',
       'Distribution Range Size (units of 10,000 sq. km.)',
       'Distribution Range Size CI (units of 10,000 sq. km.)',
       'Long Term Status', 'Current Status', 'dist_status',
       'Status of Conservation Concern', 'Assessed Primarily Based On',
       'mig_status']

temp_df = df['iucn_status'].value_counts().reset_index()


# create trace1
trace1 = go.Bar(x = temp_df['index'],
                y = temp_df['iucn_status'],
                marker = dict(color = 'rgb(255,165,0)',
                              line=dict(color='rgb(0,0,0)',width=1.5)))
layout = go.Layout(title = 'IUCN STATUS DISTRIBUTION' , xaxis = dict(title = 'IUCN STATUS'), yaxis = dict(title = 'Count'))
fig = go.Figure(data = [trace1], layout = layout)
fig.show()

df['iucn_status'].unique()

df_near_threatened=df[df['iucn_status']=='Near Threatened']
df_least_concern=df[df['iucn_status']=='Least Concern']
df_vul=df[df['iucn_status']=='Vulnerable']
df_end=df[df['iucn_status']=='Endangered']
df_critic_end=df[df['iucn_status']=='Critically Endangered']

"""### LEVENE TEST - assessing the equality of variances for a variables calculated for 2 or more groups"""

leveneTest = stats.levene(df_least_concern['annual_change'], df_vul['annual_change'],df_end['annual_change'],df_critic_end['annual_change'],df_near_threatened['annual_change'])
leveneTest

"""P-value more 0.05. Hence we fail to reject null hypothesis. This implies that groups have equal variances.

### ANOVA Hypotheses

Null Hypothesis (H0) — All IUCN Status are equal in terms of average Average Annual Change(%).
Alternative Hypothesis (HA) — Atleast one IUCN status group has significantly different Average Annual Change(%).
"""

import statsmodels.api as sm
from statsmodels.formula.api import ols
lm = ols('annual_change ~ iucn_status',data=df).fit()
table = sm.stats.anova_lm(lm)
print(table)

"""In these results, the null hypothesis states that the mean Annual Change of all the IUCN status are equal. Because the p-value is 0.01474, which is less than the significance level of 0.05, we can reject the null hypothesis and conclude that at least one of the IUCN groups has significantly different average annual change(%).

POST HOC TEST

Post hoc tests are an integral part of ANOVA. When we use ANOVA to test the equality of at least three group means, statistically significant results indicate that not all of the group means are equal. However, ANOVA results do not identify which particular differences between pairs of means are significant. Hence,we use post hoc tests to explore differences between multiple group means.

I will be using the TUKEY TEST as the post hoc test in our example.It will help identify the groups that have significantly different average annual change(%)

### TUKEY TEST:
in these results, the confidence intervals indicate the following:

The confidence interval for the difference between the means the two respective groups is provided. 

If this range does not include zero, it indicates that the difference is statistically significant.


If the confidence intervals for the pairs of means include zero, which indicates that the differences are not statistically significant. Or by just looking at the p value:

We can simply compare the adjusted p-values to our significance level. When adjusted p-values are less than the significance level, the difference between those group means is statistically significant.
"""

from statsmodels.stats.multicomp import pairwise_tukeyhsd

# perform multiple pairwise comparison (Tukey HSD)
m_comp = pairwise_tukeyhsd(endog=df['annual_change'], groups=df['iucn_status'], alpha=0.05)
print(m_comp)

"""Here, all the confidence intervals include zero,and the adjusted p-values >0.05 for all the group pairs.Hence,this is contaradicting what we proved through the Anova test that atleast one pair has significantly different mean Annual Change(%). We can solve the problem by relaxing our alpha value in the Tukey test.It is possible that the difference exists but at higher alpha."""

m_comp = pairwise_tukeyhsd(endog=df['annual_change'], groups=df['iucn_status'], alpha=0.06)
print(m_comp)

"""The species with IUCN Status:Least Concerned and Near Threatened don't have 0 in the confidence interval now,which indicates that the difference between Annual change(%) of the two groups is statistically significant.Near threatened groups see higher Average Annual Change than Least concerned.

Now we get a significant outcome.We can report it as not significant at 0.05, but a significant difference is present at alpha = 0.06.

## Hypothesis Test 2: MIGRATORY STATUS

Question: Is there any difference between Migratory Status when considering Annual Change(%)?
"""

temp_df = df['mig_status'].value_counts().reset_index()

# create trace1
trace1 = go.Bar(
                x = temp_df['index'],
                y = temp_df['mig_status'],
                marker = dict(color = 'rgb(255,165,0)',
                              line=dict(color='rgb(0,0,0)',width=1.5)))
layout = go.Layout(template= "presentation",title = 'MIGRATORY STATUS DISTRIBUTION' , 
                   xaxis = dict(title = 'MIGRATORY STATUS'), yaxis = dict(title = 'Count'))
fig = go.Figure(data = [trace1], layout = layout)
fig.show()

df['mig_status'].unique()

df_res=df[df['mig_status']=='Resident']
df_migratory_local=df[df['mig_status']=='Migratory-Local']
df_migratory_ld=df[df['mig_status']=='Migratory-Long-Distance']

leveneTest = stats.levene(df_res['annual_change'], df_migratory_local['annual_change'],df_migratory_ld['annual_change'])
leveneTest

"""Variances are the same. We can proceed to One-Way Anova."""

import statsmodels.api as sm
from statsmodels.formula.api import ols
lm = ols('annual_change ~ mig_status',data=df).fit()
table = sm.stats.anova_lm(lm)
print(table)

"""P-value in One-Way Anova is more than 0.05. That implies that all mig.status are equal in terms of variable given - Average Annual Change.

### Hypothesis Test 3: DISTRIBUTION STATUS
"""

temp_df = df['dist_status'].value_counts().reset_index()


# create trace1
trace1 = go.Bar(
                x = temp_df['index'],
                y = temp_df['dist_status'],
                marker = dict(color = 'rgb(255,165,0)',
                              line=dict(color='rgb(0,0,0)',width=1.5)))
layout = go.Layout(template= "presentation",title = 'DISTRIBUTION Status' , xaxis = dict(title = 'DISTRIBUTION STATUS'), yaxis = dict(title = 'Count'))
fig = go.Figure(data = [trace1], layout = layout)
fig.show()

df['dist_status'].unique()

df_1=df[df['dist_status']=='Very Large']
df_2=df[df['dist_status']=='Large']
df_3=df[df['dist_status']=='Moderate']
df_4=df[df['dist_status']=='Restricted']
df_5=df[df['dist_status']=='Very Restricted']

leveneTest = stats.levene(df_1['annual_change'],df_2['annual_change'],df_3['annual_change'],df_4['annual_change'],df_5['annual_change'])
leveneTest

"""We see that p-value is very small. Hence we cannot proced with classis Anova as the variances are unequal.

Alternative - Welch's ANOVA.

### Welch’s ANOVA

ANOVA Hypotheses




*   Null Hypothesis  (H0) — All Distribution status are equal in terms of average Average Annual Change(%).
*   Alternative Hypothesis (HA) — Atleast one Distribution status group has significantly different Average Annual Change(%).
"""

#!pip install pingouin

from pingouin import welch_anova, read_dataset

aov = welch_anova(dv='annual_change', between='dist_status', data=df)
aov

"""The mean Annual Change of all the Distribution status are equal. Because the p-value is 0.294282, which is more than the significance level of 0.05, we fail to reject the null hypothesis and conclude that: All Distribution Status are equal in terms of Average Annual Change(%)."""







