import pandas as pd
import numpy as np


class BmiClassifier:
    '''Class object of data specific BMI classifier

    methods:
        get_bmi(self)
        set_bmi_info(self)
        get_category_frequency(self, bmi_category)

    '''

    def __init__(self, input_data, print_info=False):
        '''Class contructor to initialize object

        argument1 (str): Takes data file path as string
        argument2 (bool): Option argument to view dataframe head
        '''

        # read in data
        self.df = pd.read_json(input_data, dtype={'Gender': 'category', 'HeightCm': np.int16, 'WeightKg': np.int16})

        for column in self.df[['HeightCm', 'WeightKg']]:

            # filter rows containing strings
            self.df = self._rem_str_row(self.df[column])

            # recast dtype
            self.df[column] = self._recast_dtype_int(self.df[column])

        # filter ranges
        self.df = self.df[self.df.HeightCm.between(50, 300)]
        self.df = self.df[self.df.WeightKg.between(5, 750)]
        self.df = self.df[self.df.Gender.isin(['Male', 'Female'])]

        # get bmi
        self.get_bmi()

        # set bmi info
        self.set_bmi_info()

        # option to view data
        if print_info:
            print(self.df.head())

    def _rem_str_row(self, column):
        '''Filters dataframe of row containing strings columns that shouldn only contain integers.'''

        if column.dtype != np.int16:
            self.df = self.df[column.apply(lambda x: str(x).isnumeric())]
        return self.df

    def _recast_dtype_int(self, column):
        '''If datatype not correct for column recasts to correct.'''

        if column.dtype != np.int16:
            column = column.astype(np.int16)
        return column

    def get_bmi(self):
        '''Calculates BMI using the formula: (kg/m2) = mass(kg) / height(m)2'''

        self.df['BMI'] = (self.df.WeightKg / (self.df.HeightCm / 100) ** 2).astype(np.float16)

    def _get_bmi_info(self, bmi):
        '''Takes BMI as argument and using BMI range to return BMI category and health risk classification.'''

        if bmi <= 18.4:
            bmi_category = 'Underweight'
            health_risk = 'Malnutrition risk'
        elif bmi >= 18.5 and bmi <= 24.9:
            bmi_category = 'Normal weight'
            health_risk = 'Low risk'
        elif bmi >= 25 and bmi <= 29.9:
            bmi_category = 'Overweight'
            health_risk = 'Enhanced risk'
        elif bmi >= 30 and bmi <= 34.9:
            bmi_category = 'Moderately obese'
            health_risk = 'Medium risk'
        elif bmi >= 35 and bmi <= 39.9:
            bmi_category = 'Severely obese'
            health_risk = 'High risk'
        elif bmi >= 40:
            bmi_category = 'Very severely obese'
            health_risk = 'Very high risk'
        else:
            bmi_category = None
            health_risk = None
        return bmi_category, health_risk

    def set_bmi_info(self):
        '''Using BMI, derives BMI category and health risk classification and appends values to dataframe.'''

        self.df['BMICategory'], self.df['HealthRisk'] = zip(*[self._get_bmi_info(bmi) for bmi in self.df.BMI.values if bmi != None])

        # recast dtype
        self.df = self.df.astype({'BMICategory':'category', 'HealthRisk':'category'})

    def get_category_frequency(self, categories=[]):
        '''Takes user specified BMI category as argument, returns frequency count of the BMI category'''

        category_count = 0

        if isinstance(categories, list) != True:
            raise TypeError(f"input '{categories}' should be a list")

        if categories:
            for category in categories:
                # check for typos/non present BMI categories
                if category in self.df.BMICategory.values:
                    category_count += self.df[self.df.BMICategory == category].shape[0]
                else:
                    print(f"Please check '{category}' is correct/present")

            # get total and other value counts to confirm numbers make sense
            total_category_count, uncounted_categories = self.check_frequency(categories)
            if total_category_count - uncounted_categories == category_count:
                return category_count
            else:
                print(f"Uncounted frequency count '{uncounted_categories}' plus counted frequency count {category_count} is less than total frequency count {total_category_count}")

    def check_frequency(self, categories):
        '''Takes list of categories given by user to get counts of remainder categories. Returns total counts and remainder category counts. '''

        count = 0
        total_category_count = self.df.BMICategory.value_counts().sum()
        uncounted_categories = set(self.df.BMICategory.unique()) - set(categories)
        if uncounted_categories:
            for category in uncounted_categories:
                count += self.df[self.df.BMICategory == category].shape[0]
            return total_category_count, count


if __name__ == '__main__':
    bmi_object = BmiClassifier('bmi_data.json')
    overweight_frequency = bmi_object.get_category_frequency(['Overweight', 'Moderately obese'])
    print(f"Number of of people classified as overweight are: {overweight_frequency}")