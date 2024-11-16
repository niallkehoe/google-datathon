import pandas as pd
from functools import cache

class CountyNormalizer:
    def __init__(self, population_path='../data/population'):
        self.data2000_09 = CountyNormalizer.clean(pd.read_csv(f'{population_path}/co-est2009-alldata.csv', dtype={c: str for c in ['COUNTY', 'STATE', 'SUMLEV']},  encoding='ISO-8859-1'))
        self.data2010_19 = CountyNormalizer.clean(pd.read_csv(f'{population_path}/co-est2020-alldata.csv', dtype={c: str for c in ['COUNTY', 'STATE', 'SUMLEV']}, encoding='ISO-8859-1'))
        self.data2020_23 = CountyNormalizer.clean(pd.read_csv(f'{population_path}/co-est2023-alldata.csv', dtype={c: str for c in ['COUNTY', 'STATE', 'SUMLEV']}, encoding='ISO-8859-1'))
        self.id_to_row_00_09 = CountyNormalizer.id_to_row(self.data2000_09)
        self.id_to_row_10_19 = CountyNormalizer.id_to_row(self.data2010_19)
        self.id_to_row_20_23 = CountyNormalizer.id_to_row(self.data2020_23)
        
        self.cache = {}

    def clean(df):
        # remove all rows where CTYNAME == STNAME, except one instance of district of columbia; we arbitrarily keep the COUNTY == 0
        df = df[(df['STNAME'] != df['CTYNAME']) | ((df['STNAME'] == 'District of Columbia') & (df['COUNTY'] == 0))].reset_index()
        return df
    
    def id_to_row(df):
        def concat_state_and_county(row):
            return row['STATE'] + row['COUNTY']
        county_ids = df.apply(concat_state_and_county, axis=1)
        id_to_row_map = {}
        for i in range(len(county_ids)):
            id_to_row_map[county_ids.iloc[i]] = i
        return id_to_row_map
    
    def clear_cache(self):
        del self.cache
        self.cache = {}
    
    def get_population(self, row):
        return self.get_population_(row['FIPS'], row['Year'])
        
    def get_population_(self, FIPS, year):
        '''
        countyName: string
        year: int
        '''
        countyId = FIPS
        assert isinstance(year, int) and isinstance(countyId, str)
        assert 2000 <= year <= 2023
        if f'{countyId}{year}' in self.cache:
            return self.cache[f'{countyId}{year}']
        
        data = None
        id_to_row = None
        
        if year < 2010:
            data = self.data2000_09
            id_to_row = self.id_to_row_00_09
        elif year < 2020:
            data = self.data2010_19
            id_to_row = self.id_to_row_10_19
        else:
            data = self.data2020_23
            id_to_row = self.id_to_row_20_23
        
        self.cache[f'{countyId}{year}'] = data[f'POPESTIMATE{year}'].iloc[id_to_row[countyId]]
        return self.cache[f'{countyId}{year}']
        