# import pandas with the alias pd
import pandas as pd

# Now read in the titanic data
titanic = pd.read_csv('./data/titanic.csv')

# Finally, check the data using head()
titanic.head()