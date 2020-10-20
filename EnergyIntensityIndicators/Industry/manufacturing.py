
# ASMdata_date.xlsx

# ind_hap3_date.xlsx

#2014_MECS = 'https://www.eia.gov/consumption/manufacturing/data/2014/'  # Table 4.2


# Table 3.1 and 3.2 (MECS total fuel consumption)  Table 3.1 shows energy
# consumption by fuel in physical units, including the total across all fuels expressed in trillion Btu and
# electricity in kWh. From Table 3.1, total fuel consumption in Btu can be calculated as difference between
# total energy and electricity consumption after conversion to Btu. Table 3.2 only differs from Table 3.1 by
# showing all fuel types in Btu. 



MER_Table24_Industrial_Energy_Consumption = [0]

# For 2014, the values for total energy consumption and electricity consumption, both defined in terms of
# trillion Btu, from Table 3.2 are transferred to spreadsheet ind_hap3. Worksheet MECS_Fuel in this
# spreadsheet has been used to collect the fuel consumption estimates for all the MECS dating back to the
# first MECS in 1985. The 2014 data are located in the cell range F218:F238.
# The first six NAICS sectors are aggregated into three sectors (311-312, 313-314, and 315-316) as a part
# of the set of manufacturing indicators. The energy consumption data under this revised sectoring
# classification are shown in the columns to the right, columns O and P.



# Energy prices
MECS_Table72 = [0]

def get_historical_mecs(self):
            """Read in historical MECS csv, format (as in e.g. Coal (MECS) Prices)
            """            
            historical_mecs = pd.read_csv('./') 
            return historical_mecs

        def manufacturing_prices(self):
            """Call ASM API method from Asm class in get_census_data.py
            Specify three-digit NAICS Codes
            """ 
            fuel_types = ['Gas', 'Coal', 'Distillate', 'Residual', 'LPG', 'Coke', 'Other']

            asm_price_data = Mfg_prices().calc_calibrated_predicted_price(latest_year=self.end_year, fuel_type, naics)
            return asm_price_data           




    def manufacturing(self):
        """Main datasource is the Manufacturing Energy Consumption Survey (MECS), conducted by the EIA since 1985 (supplemented for non-MECS years by 
        estimates derived from the Annual Survey of Manufactures (ASM) and the Economic Census (EC) conducted every five years)
        https://www.eia.gov/consumption/manufacturing/data/2014/
        https://www.eia.gov/consumption/manufacturing/data/2014/#r4 
        """    
    
    return manufacturing
