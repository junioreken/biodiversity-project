# Biodiversity Project


from matplotlib import pyplot as plt
import pandas as pd
from scipy.stats import chi2_contingency

# Loading 'specied_info' dataset
species = pd.read_csv('species_info.csv')

# Inspect the species DataFrame 
species.head()

# Assessing number of different species in the `species` DataFrame?
species.scientific_name.nunique()

# Assessing the different values of `category` in `species`?
species.category.unique()

# Assessing the different values of `conservation_status`?
species.conservation_status.unique()

# The column `conservation_status` has several possible values:
# - `Species of Concern`: declining or appear to be in need of conservation
# - `Threatened`: vulnerable to endangerment in the near future
# - `Endangered`: seriously at risk of extinction
# - `In Recovery`: formerly `Endangered`, but currently neither in danger of extinction throughout all or a significant portion of its range
# 
# Assessing how many species meet each of these criteria. 
species.groupby('conservation_status').scientific_name.nunique().reset_index()

# There are far more than 200 species in the `species` table.  Clearly, only a small number of them are categorized as needing some sort of protection.  
# The rest have `conservation_status` equal to `None`. Because `groupby` does not include `None`, the null values will be filled using `.fillna`.  
species.fillna('No Intervention', inplace=True)

# Assessing how many species require `No Protection`.
species.groupby('conservation_status').scientific_name.nunique().reset_index()

# Sorting the columns by how many species are in each categories. Sorting by `scientific_name`:
protection_counts = species.groupby('conservation_status').scientific_name.nunique().reset_index().sort_values(by='scientific_name')

# Creating creating a bar chart
plt.figure(figsize=(10, 4))
ax = plt.subplot()
plt.bar(range(len(protection_counts)), protection_counts.scientific_name.values)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
plt.show()

# Question: Are certain types of species more likely to be endangered?
# Creating a new column in `species` called `is_protected`, which is `True` if `conservation_status` is not equal to `No Intervention`, and `False` otherwise.
species['is_protected'] = species.conservation_status != 'No Intervention'

# Grouping the `species` data frame by the `category` and `is_protected` columns and counting the unique `scientific_name`s in each grouping.
category_counts = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()

# Examining `category_counts` using `head()`.
category_counts.head()

# For better visualization, pivoting and rearranging `category_counts` such that:
# - `columns` is `is_protected`
# - `index` is `category`
# - `values` is `scientific_name`
category_pivot = category_counts.pivot(columns='is_protected',
                                      index='category',
                                      values='scientific_name')\
                                .reset_index()

# Renaming the categories `True` and `False` to something more descriptive:
category_pivot.columns = ['category', 'not_protected', 'protected']

# Creating a new column of `category_pivot` called `percent_protected`, which is equal to `protected` (the number of species that are protected) divided by `protected` plus `not_protected` (the total number of species).
category_pivot['percent_protected'] = category_pivot.protected / (category_pivot.protected + category_pivot.not_protected)

# Examining `category_pivot`.
print(category_pivot)

# It looks like species in category `Mammal` are more likely to be endangered than species in `Bird`. Performing a significance test to see if this statement is true.  
# Questions to consider before doing the significance test:
# - Is the data numerical or categorical?
# - How many pieces of data are being compared?

# Based on those answers, a *chi squared test* should be performed.  In order to run a chi squared test, a contingency table should be created.  
contingency = [[30, 146],
              [75, 413]]

chi2_contingency(contingency)

# It looks like this difference isn't significant!
# 
# Performing another test.  Is the difference between `Reptile` and `Mammal` significant?
contingency = [[30, 146],
               [5, 73]]
chi2_contingency(contingency)

# From the results, it looks like there is a significant difference between `Reptile` and `Mammal`

# Observing the data of conservationists about the sightings of different species at several national parks

observations = pd.read_csv('observations.csv')
observations.head()

# Some scientists are studying the number of sheep sightings at different national parks.  
# There are several different scientific names for different types of sheep.  Assessing which rows of `species` are referring to sheep.  
# Creating a new column in `species` called `is_sheep` which is `True` if the `common_names` contains `'Sheep'`, and `False` otherwise.
species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)
species.head()

# Selecting the rows of `species` where `is_sheep` is `True` and `category` is `Mammal`.  
sheep_species = species[(species.is_sheep) & (species.category == 'Mammal')]
sheep_species

# Merging `sheep_species` with `observations` to get a DataFrame with observations of sheep. 
sheep_observations = observations.merge(sheep_species)

# Question: How many total sheep observations (across all three species) were made at each national park?  
# This is the total number of sheep observed in each park over the past 7 days.
obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()
obs_by_park

# Creating a bar chart showing the different number of observations per week at each park.
plt.figure(figsize=(16, 4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park)),
        obs_by_park.observations.values)
ax.set_xticks(range(len(obs_by_park)))
ax.set_xticklabels(obs_by_park.park_name.values)
plt.ylabel('Number of Observations')
plt.title('Observations of Sheep per Week')
plt.show()

# Our scientists know that 15% of sheep at Bryce National Park have foot and mouth disease.  
# Park rangers at Yellowstone National Park have been running a program to reduce the rate of foot and mouth disease at that park.  
# The scientists want to test whether or not this program is working.  They want to be able to detect reductions of at least 5 percentage point.  
# For instance, if 10% of sheep in Yellowstone have foot and mouth disease, they'd like to be able to know this, with confidence.
# 
# Using the default level of significance (90%).

minimum_detectable_effect = 100 * 0.05 / 0.15
minimum_detectable_effect

baseline = 15
sample_size_per_variant = 870


# Question: how many weeks would one need to observe sheep at Bryce National Park in order to observe enough sheep?  
# Question: How many weeks would you need to observe at Yellowstone National Park to observe enough sheep?
bryce = 870 / 250.
yellowstone = 810 / 507.

# Answers: Approximately 3.5 weeks at Bryce and 1.5 weeks at Yellowstone.



