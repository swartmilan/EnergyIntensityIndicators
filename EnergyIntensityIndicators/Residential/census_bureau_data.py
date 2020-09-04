"""
[summary]
"""
import pandas as pd
import os
import requests
from zipfile import ZipFile
import numpy as np

class GetCensusData:
    
    def __init__(self): 
        pass

    def update_ahs_data():
        """Spreadsheet equivalent: AHS_2017_extract
        Extract and process American Housing Survey (AHS, formerly Annual Housing Survey) 
        web: https://www.census.gov/programs-surveys/ahs/data.html
        ? https://www.census.gov/programs-surveys/ahs/data/2017/ahs-2017-public-use-file--puf-/ahs-2017-national-public-use-file--puf-.html 
        """    
        ahs_url_folder   'http://www2.census.gov/programs-surveys/ahs/2017/AHS%202017%20National%20PUF%20v3.0%20CSV.zip?#' 
        
        if os.path.exists('./household.csv'):
            pass
        else: 
            with ZipFile(ahs_url_folder, 'r') as zipOjb:
                zipObj.extact('household.csv')
       
        ahs_household_data = pd.read_csv('./household.csv')
        columns = ['JYRBUILT', 'WEIGHT', 'YRBUILT', 'DIVISION', 'BLD', 'UNITSIZE', 'VACANCY']
        extract_ahs = ahs_household_data[columns]
        extract_ahs= extract_ahs[extract_ahs['BLD'].isin(['04', '05', '06', '07', '08', '09'])]
        housing_types = ['single_family', 'multifamily', 'manufactured_homes']
        housing_occupancy_types = [f'{h}_total' for h in housing_types] + [f'{h}_occupied' for h in housing_types]
        housing_type_number = dict(zip()) # match the numbers in ['04', '05', '06', '07', '08', '09'] to housing/occupancy type
        #  For the total number of units of each building type, the variable
        # s, the pivot table processing
        # generated six tables shown below the active pivot table in the first 16 rows of the worksheet. The six
        # tables are for Single Family (SF) units (Total and Occupied), Multi-Family (MF) units (Total and Occupied),
        # and Manufactured Home (Man.Homes) units (Total and Occupied). These tables were obtained by
        # copying the values from the active pivot table at the top of the worksheet, each table reflecting a
        # different choice for VACANCY and BLD. VACANCY is set to “All”. For occupied units, set the VACANCY variable to ‘-6’. For the building type,
        # single family units are obtained by selecting building code ‘02’ and ’03’ (corresponding to detached and
        # attached units). Multi-family units are selected by checking the boxes under BLD, ‘04’ through ‘09’).
        # Manufactured homes are selected with a check of the code ’01.’

        # Pivot Tables!!
        #  Rows correspond to various size categories columns correspond to census division which are then aggregated to census regions. 
        #  Only Categorical size data were included in the AHS surveys for 2015 and 2017. An effort to 
        # utilize the category data to estimate the average size change between 2015 and 2017 did not provide useful results. Processing of future AHS public use
        # files may exlcude any consideration of this variable. In the current tables, only the values for total units across all sizes were considered.
        pivot_census_division = pd.pivot_table(extract_ahs, values='WEIGHT' , index=['BLD', 'UNITSIZE'] , columns='DIVISION' , aggfunc='sum')  
        pivot_census_division['census_region_1'] = pivot_census_division['1'] + pivot_census_division['2']   # alternative method: df['C'] = df.apply(lambda row: row['A'] + row['B'], axis=1)
        pivot_census_division['census_region_2'] = pivot_census_division['3'] + pivot_census_division['4']
        pivot_census_division['census_region_3'] = pivot_census_division['5'] + pivot_census_division['6'] + pivot_census_division['7']
        pivot_census_division['census_region_4'] = pivot_census_division['8'] + pivot_census_division['8']
        pivot_census_division['total'] = pivot_census_division['census_region_1'] + pivot_census_division['census_region_2'] + 
                                                pivot_census_division['census_region_3'] + pivot_census_division['census_region_4']
        pivot_census_division.loc['Grand Total', :]= pivot_census_division.sum(axis=0)

        return pivot_census_division          

    def get_percent_remaining_surviving(factor, lifetime, gamma):
        return 1 / (1 + (factor / lifetime) ** gamma)   

    def survival_curve(ahs_tables_data, housing_type):
        """The objective function is set to minimize the squared differences between the
            predicted stock and the actual stock.

        Returns:
            output_data (dataframe): These columns represent the
            existing (prior year’s) stock, estimated retirements, and new units. The sum of these columns is the
            estimated end-of-year stock shown in column AM. The actual stock reported by the AHS is shown in
            column AN.
        """   
        gamma = 4.261172611 # comes from T182
        lifetime = 85.95544078 # comes from T183
        scalar = 1.000217584 # comes from T184

        objective_function_SSRD = sum() * 0.001
        from_regression =  # AHS_tables!$IK$16


        current_year = 2020  # use datetime to get current year
        years = list(range(1870, current_year + 1)) 
        age = [current_year - y for y in years]
        dataframe = pd.DataFrame([years, years_ago]).transpose()
        dataframe = dataframe.columns(['year', 'age'])
        dataframe['remaining']  = dataframe['age'].apply(lambda x: get_percent_remaining_surviving(x, lifetime, gamma))
        dataframe['remaining_inverse'] = dataframe['remaining'].apply(lambda x: 1 / x)
        dataframe['inflation_factor'] = dataframe['age'].subtract(dataframe['age'][0].values())
        dataframe['pct_surviving'] = dataframe['inflation_factor'].apply(lambda x: get_percent_remaining_surviving(x, lifetime, gamma))

        if housing_type == 'single_family':
            column_years = [1910, 1948, 1955, 1965, 1975, 1985, 1995]  # Was 1910 a typo in the spreadsheet? 
        else:
            column_years = [1930, 1948, 1955, 1965, 1975, 1985, 1995]

        row_years = [1999, 2001, 2003, 2005, 2007, 2009]

        ahs_decades = ['<1940', '1940-49', '1950-59', '1960-1969', '1970-1979', '1980-1989', '1990-1999']
        column_years_to_decade = dict(zip(column_years, ahs_decades))

        for c in column_years: 
            dataframe[str(c)] = [dataframe[['age'] == (y - c)]['remaining'].values() for y in dataframe['year']]  # Starts at 1979 ?
            dataframe.loc[dataframe.year <= dataframe[str(c)], dataframe[str(c)]] = 1  # Survival_curve_SF has this different but the spreadsheet seems wrong?
            dataframe.loc[dataframe.year < 1979, dataframe[str(c)]] = None  # or np.nan? 

            dataframe[f'adjusted_{c}'] = dataframe[str(c)].multiply(column_years_to_decade[c])

        dataframe = dataframe.set_index('year')
        retirement_calc_df = dataframe[[f'adjusted_{c}' for c in column years]].divide(dataframe[['year'] == 1999][list(map(str, column_years))])
        retirement_calc_df['total'] = retirement_calc_df.sum(1)
        retirement_calc_df['total_shifted_down'] = retirement_calc_df['total'].shift(periods=1, axis='index')
        retirement_calc_df['retirements'] = retirement_calc_df['total'].subtract(retirement_calc_df['total_shifted_down'])
        retirement_calc_df['retirement_ratio'] = retirement_calc_df['retirements'].div(retirement_calc_df['total'])

        pct_surviving = []
        for r in row_years:
            row = [dataframe[['inflation_factor'] == (r - c)]['pct_surviving'].values() for c in column years]
            pct_surviving.append(row)

        pct_surviving_df = pd.DataFrame(pct_surviving, columns=column_years).set_index(row_years)  # Check this
        fraction_of_1999 = pct_surviving_df.apply(lambda x: x.div(x.iloc[0]), axis=index) # Check this
        adjusted_fraction_of_1999 = fraction_of_1999.multiply(scalar) # ALSO HAVE TO MULTIPLY EACH ROW BY VALUE FOR DECADE FROM AHS TABLES
        adjusted_fraction_of_1999['total'] = adjusted_fraction_of_1999.sum(1)

        another_ahs_table =
        actual_total = another_ahs_table.sum(1)
        predicted_total = adjusted_fraction_of_1999['total'] * scalar
        diff = (actual_total - predicted_total).pow(2) # check types

        difference =  adjusted_fraction_of_1999.subtract(another_ahs_table)
        squared_difference = difference.pow(2)

        return None

    def get_place_nsa_all():
        years = list(range(1994, 2013 + 1))
        for year in years:
            url = f'http://www2.census.gov/programs-surveys/mhs/tables/{str(year)}/stplace{str(year)[-2:]}.xls'
            placement_df = pd.read_excel(url, index_col=0, skiprows=4, use_cols='B, F:H') # Placement units are thousands of units


    def get_housing_stock(housing_type, units_model='Model2'):
        """Spreadsheet equivalent: Comps Ann, place_nsa_all
        Data Sources: 
            - Census Bureau Survey of  New Construction https://www.census.gov/construction/nrc/historical_data/index.html
            - Manufactured Housing Survey: Annual data for the most current years were not found on the Census Bureau website.
            Monthly data were downloaded for both total units and single (wide) units from the Census Bureau (in
            worksheets CIDR-1 and CIDR-single). The monthly data were aggregated to an annual basis for the years
            2014 through 2018 on these worksheets and the annual values appended to the existing data in the
            place_nsa_all worksheet. (Ideally, the place_nsa_all spreadsheet would be available from the Census
            Bureau for the most recent years but was not found as part of the 2020 update work.)
        Estimate regional housing and regional floorspace by housing type (single family, multifamily, manufactured homes)
        Data Sources: 
            - American Housing Survey (AHS) conducted by the Census Bureau to estimate aggregate floor space for three types
              of housing units: single-family (attached and detached), multi-family, and manufactured homes
        Spreadsheet Equivalents:
            - AHS_summary_results_date \Total_Stock_SF.xlsx (single family)
            - AHS_summary_results_date \Total_Stock_MF.xlsx (multifamily)
            - AHD_summary_results_date \Total_Stock_MH.xlsx (manufactured homes) 
        Methodology: 
            1. An estimated survival curve was first developed from vintage data over the 1999 through
               2009 AHS surveys.
            2. Curve was used along with reported new construction from the Characteristics of New
               Housing reports from the Census Bureau.
            3. The “stock adjustment model” was used to arrive at estimates of “Occupied Housing Units”
               at the national level.
        """
        url_ = 'https://www.census.gov/construction/nrc/xls/co_cust.xls'

        if housing_type == 'single_family' | housing_type == 'multi_family':
            housing_units_completed_or_placed = pd.read_excel(url_) # completed

        else:
            pass

        if housing_type == 'single_family':
            columns = 'In structures with -- 1 unit'
            factor = 0.95

        elif housing_type == 'multifamily'
            columns = ['In structures with -- 2 to 4 units', 'In structures with -- 5 Units or more']
            factor = 0.96
        else: 
            housing_units_completed_or_placed =   # Added (place_nsa_all)
            columns = 'US Total'
            factor = 0.96

        if units_model == 'Model1':
            new_units = housing_units_completed_or_placed[columns]
            new_units_adjusted = new_units * factor
            retirements = survival_curve(ahs_tables_data, housing_type)
            net_change = new_units_adjusted + retirements
            benchmark  = ?? # 

            # Methodology used in early days
            for_sale_for_rent_units = 
            ahs_vacant_units = for_sale_for_rent_units 
            occupied_units = total_units - ahs_vacant_units

            # New Methodology
            vacancy_rate = 
            occupancy_fraction = 1 - vacancy_rate
            predicted_total_stock = 
            estimate_occupied_units = predicted_total_stock * occupancy_fraction

            **National Estimates of housing unit size**
            **Regional Shares of national-level housing**

        else: # Model Two
            # if housing_type == 'single_family':
            fraction_of_retirements = 
            fixed_value = 1
            constant_adjustment = 
            objective_function = 
            adjustment_factor = 0.7  # comes from solver? 

            new_comps_ann =  # from comps ann column C
            pub_total = 
            occupied_published = 

            extisting_stock_0 = pub_total[0] + constant_adjustment
            extisting_stock_1 = extisting_stock_0
            predicted_retirement_0 = 0
            new_units_0 = 0

            adjusted_new_units = new_units ** adjustment_factor
            existing_stock = 
            predicted_retirement = (-1 * existing_stock) * adjusted_new_units * fraction_of_retirements
            new_units = ((new_comps_ann + new_comps_ann.shift(-1)) / 2 ) * fixed_value # is this shifted in the right way? 
            predicted_total_stock = existing_stock + predicted_retirement + new_units
            actual_stock = pub_total
            diff = actual_stock - predicted_total_stock
            squared_difference = diff ** 2
            implied_retirement_rate = predicted_retirement / existing_stock

            
            total_pub_occupied = pub_total - occupied_single_family  # Spreadsheet is confused about what this is, CHECK
            
            total_vacancy_rate = 
            sf_occupied_predicted = (1 - total_vacancy_rate) * predicted_total_stock 
            sf_occupied_actual = occupied_published

            # Model for average housing unit size
            new_comps_ann_adj = new_comps_ann * fixed_value
            cnh_avg_size = # SFTotalMedAvgSqFt column G
            BH = new_comps_ann * cnh_avg_size
            BI_0 = BH[0]
            BI = 
            post_1984_units = 
            avg_size_post84_units =
            BL = (post_1984_units + post_1984_units.shift(-1)) * 0.5 * bn7_factor + predicted_size_pre_1985_stock
            pre_1985_stock = 
            total_sq_feet_pre_1985 = 


            # elif housing_type == 'multi_family':
            all_single_family = actual_stock
            occupied_single_family =  # column J Total_stock_SF
            households =  # National_Calibration'!E13
            year = 
            

        return housing_units_completed

    def final_floorspace_estimates():
        
        number_occupied_units_national, average_size_national = get_housing_stock()

        regions = ['National', 'Northeast', 'Midwest', 'South', 'West']
        final_results_total_floorspace_regions = dict()

        for region in regions: 
            calculated_shares_by_region =  # From AHS tables
            ratios_to_national_average_size = # From AHS tables

            regional_estimates = number_occupied_units_national.multiply(calculated_shares_by_region)
            regional_estimates['Total'] = regional_estimates.sum(axis=1)
            shares_by_type = regional_estimates[['Single Family', 'Multi-Family', 'Man. Homes']].divide(regional_estimates['Total'])
            
            # Calibration Procedure
            sum_of_regions = 
            scale_factor = 
            final_check =
            average_size_all_housing_units =
            number_of_units = 

            total_square_feet =
            average_size = 
            ratios_national_average_size = 

            average_size_after_calibration = 


            final_results_total_floorspace = number_occupied_units.multiply(average_size).multiply(0.000001)
            final_results_total_floorspace['Total'] = final_results_total_floorspace.sum(axis=1)

            number_occupied_units['Total'] = number_occupied_units.sum(axis=1)
            
            final_results_total_floorspace_regions[region] = final_results_total_floorspace

        return final_results_total_floorspace_regions

    def weighted_floorspace():
        energy_types = ['Electricity', 'Fuels', 'Delivered', 'Source']
        constant_electricity_factor = 3.2

    def get_census_bureau_manufactured_housing_survey():
        """[summary]
        Annual data for the most current years were not found on the Census Bureau website.
        Monthly data were downloaded for both total units and single (wide) units from the Census Bureau (in
        worksheets CIDR-1 and CIDR-single). The monthly data were aggregated to an annual basis for the years
        2014 through 2018 on these worksheets and the annual values appended to the existing data in the
        place_nsa_all worksheet. (Ideally, the place_nsa_all spreadsheet would be available from the Census
        Bureau for the most recent years but was not found as part of the 2020 update work.)
        """
        pass    