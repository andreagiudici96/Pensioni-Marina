import pandas as pd
import numpy as np

# Load the CSV file with pandas
df = pd.read_csv('coeff_rivalu.csv')

year_list = np.arange(1991, 2025, 1)

# Extract coeff_tazionerivalu values for the years in anni_list
cumulative_inflation = df[df['anno'].isin(year_list)]['coeff_rivalu'].values


initial_effective_wage = 10000
average_inflation_growth = np.full(len(year_list),  1.005)
average_yearly_growth = 3 # in percentage, i.e. 3 means 3/100
variance = 0 # in percentage, i.e. 1 per 1/100

average_inflation_growth[0] = 1  # Start from 1 for the first year
cumulative_inflation = np.cumprod(average_inflation_growth)[::-1]
print(cumulative_average_inflation)
yearly_wadge = np.array([])
growth_coefficient_yearly = 1 + np.random.normal(loc=average_yearly_growth / 100, scale=variance / 100, size=len(year_list))
growth_coefficient_yearly[0] = 1  # Start from 1 for the first year
cumulative_growth_coefficient = np.cumprod(growth_coefficient_yearly)

structured_array = np.array(list(zip(year_list, cumulative_inflation, cumulative_growth_coefficient)), dtype=[('Year', 'i4'), ('Cumulative Inflation', 'f8'), ('Cumulative Growth', 'f8')])
# Function to calculate wages and effective wages from a given starting year to a final year
def wages(initial_year, final_year):
    # Create lists to store the results
    years = np.arange(initial_year, final_year + 1)
    wages = []
    effective_wages = []
    cg = []
    ci = []
    
    # Start from the initial effective wage
    initial_wage = initial_effective_wage
    initial_growth = 1
    
    # Create an array for cumulative growth coefficient for the entire period
    total_years = final_year - initial_year + 1
    growth_coefficient_yearly = 1 + np.random.normal(loc=average_yearly_growth / 100, scale=variance / 100, size=total_years)
    growth_coefficient_yearly[0] = 1  # Start from 1 for the first year
    cumulative_growth_coefficient = np.cumprod(growth_coefficient_yearly)

    # Loop through the years from the start year to the final year
    for i in range(len(years)):
        if years[i] <= 2024:  # If the year is before or equal to 2024
            # Use the cumulative growth and inflation from the original structured data for years <= 2024
            cumulative_growth = cumulative_growth_coefficient[i]
            cumulative_inflation_value = cumulative_inflation[i]
        else:  # If the year is after 2024
            # Continue cumulative growth by multiplying previous year's growth by random growth factor
            cumulative_growth = cumulative_growth_coefficient[i]
            cumulative_inflation_value = 1  # After 2024, cumulative inflation is fixed at 1
        
        # Calculate the wage and effective wage
        wage = initial_wage * cumulative_growth
        effective_wage = initial_wage * cumulative_growth * cumulative_inflation_value
        
        # Append the results
        wages.append(wage)
        effective_wages.append(effective_wage)
        cg.append(cumulative_growth)
        ci.append(cumulative_inflation_value)
        

    # Create a new structured array to return
    wage_array = np.array(
        list(zip(years, wages, effective_wages, ci, cg)),
        dtype=[('Year', 'i4'), ('Wage', 'f8'), ('Effective Wage', 'f8'), ('Cumulative Inflation', 'f8'),
               ('Cumulative Growth', 'f8')]
    )
    
    return wage_array


# Example usage of the function
initial_year = 1991
final_year = 2024  # Example final year
wage_results = wages(initial_year, final_year)

# Display the result
print(wage_results)
import numpy as np

# Function to calculate I1, I2, and I3 from the output of the wages function
def calculate_I_values(initial_year, final_year):
    # Get the wage data for the given initial_year using the wages function
    wage_results = wages(initial_year, final_year)
    
    # Extract the effective wages and years
    effective_wages = wage_results['Effective Wage']
    years = wage_results['Year']
    
    # Calculate I1: Average of the best 10 effective wages before or on 2001
    # Select the wages before or on 2001
    wages_before_2001 = effective_wages[years <= 2001]
    print(wages_before_2001)
    
    # Get the best 10 (or fewer if there are less than 10)
    if len(wages_before_2001) > 0:
        if len(wages_before_2001) <= 10:
            I1 = np.mean(wages_before_2001)  # Average if there are fewer than or exactly 10 wages
        else:
            I1 = np.mean(wages_before_2001[-10:])  # Average of the last 10 wages if more than 10
    else:
        I1 = 0  # If no wages before or on 2001, set to 0
    
    
    # Calculate I2: Average of all effective wages before or on 2007
    wages_before_2007 = effective_wages[years <= 2007]
    if len(wages_before_2007) > 0:
        I2 = np.mean(wages_before_2007)
    else:
        I2 = 0  # If no wages before or on 2007, set to 0
    
    # Calculate I3: Average of the largest wages minus the 5 smallest ones before 2012
    wages_before_2012 = effective_wages[years <= 2012]
    if len(wages_before_2012) > 5:
        sorted_wages = np.sort(wages_before_2012)
        wages_after_removal = sorted_wages[5:]  # Remove the 5 smallest
        I3 = np.mean(wages_after_removal)
    elif len(wages_before_2012) > 0:
        I3 = np.mean(wages_before_2012)  # If fewer than 5 wages, use all of them
    else:
        I3 = 0  # If no wages before or on 2012, set to 0
    
    # Calculate I4: Average of all effective wages
    if len(effective_wages) > 0:
        I4 = np.mean(effective_wages)
    else:
        I4 = 0  # If no wages, set to 0
    
    return I1, I2, I3, I4

# Example usage
initial_year = 2012
final_year = 2046
I1, I2, I3, I4 = calculate_I_values(initial_year, final_year)

print(f"I1: {I1}, I2: {I2}, I3: {I3}, I4: {I4}")

ent =[ 21.04238974, 20.80005893, 20.61988514, 20.15036219, 19.97581624, 20.231161,   20.46964218, 20.75170423, 20.8326075,20.8934623]
np.average(ent)

np.average(ent[-10:])
def calculate_pension_F1(I1, initial_year):
    # Constants for the formula
    year_2001 = 2001
    max_1 = 48300
    max_2 = 72700
    max_3 = 84500
    
    # Calculate the difference between 2001 and the initial year
    years_difference = year_2001 - initial_year
    
    # First part: MIN(J5, 48300) * 1.75% * (2001 - initial_year)
    part1 = min(I1, max_1) * 0.0175 * years_difference
    
    # Second part: MAX(MIN(J5, 72700) - 48300, 0) * 1.5% * (2001 - initial_year)
    part2 = max(min(I1, max_2) - max_1, 0) * 0.015 * years_difference
    
    # Third part: MAX(MIN(J5, 84500) - 72700, 0) * 1.3% * (2001 - initial_year)
    part3 = max(min(I1, max_3) - max_2, 0) * 0.013 * years_difference
    
    # Fourth part: MAX(J5 - 84500, 0) * 1.15% * (2001 - initial_year)
    part4 = max(I1 - max_3, 0) * 0.0115 * years_difference
    
    # Final pension value F1
    F1 = part1 + part2 + part3 + part4
    
    return F1

# Example usage
initial_year = 1991
I1 = 20576  # Example I1 value
F1 = calculate_pension_F1(I1, initial_year)

print(f"Calculated Pension (F1): {F1}")

def calculate_pension_F2(I2, initial_year):
    # Constants for the formula
    year_2007 = 2007
    year_2002 = 2002
    max_1 = 48300
    max_2 = 72700
    max_3 = 84500
    
    # Calculate the difference between 2007 and 2002
    years_difference = year_2007 - year_2002
    
    # First part: MIN(J6, 48300) * 1.75% * (2007 - 2002)
    part1 = min(I2, max_1) * 0.0175 * years_difference
    
    # Second part: MAX(MIN(J6, 72700) - 48300, 0) * 1.5% * (2007 - 2002)
    part2 = max(min(I2, max_2) - max_1, 0) * 0.015 * years_difference
    
    # Third part: MAX(MIN(J6, 84500) - 72700, 0) * 1.3% * (2007 - 2002)
    part3 = max(min(I2, max_3) - max_2, 0) * 0.013 * years_difference
    
    # Fourth part: MAX(J6 - 84500, 0) * 1.15% * (2007 - 2002)
    part4 = max(I2 - max_3, 0) * 0.0115 * years_difference
    
    # Final pension value F2
    F2 = part1 + part2 + part3 + part4
    
    return F2

# Example usage
initial_year = 1991
I2 = 20956  # Example I2 value
F2 = calculate_pension_F2(I2, initial_year)

print(f"Calculated Pension (F2): {F2}")

def calculate_pension_F3(I3, initial_year):
    # Constants for the formula
    year_2012 = 2012
    year_2008 = 2008
    max_1 = 48300
    
    # Calculate the difference between 2012 and 2008
    years_difference = year_2012 - year_2008
    
    # First part: MIN(J7, 48300) * 1.75% * (2012 - 2008)
    part1 = min(I3, max_1) * 0.0175 * years_difference
    
    # Second part: MAX(J7 - 48300, 0) * 1.5% * (2012 - 2008)
    part2 = max(I3 - max_1, 0) * 0.015 * years_difference
    
    # Final pension value F3
    F3 = part1 + part2
    
    return F3

# Example usage
initial_year = 1991
I3 = 21495  # Example I3 value
F3 = calculate_pension_F3(I3, initial_year)

print(f"Calculated Pension (F3): {F3}")

def calculate_pension_F4(I4, final_year):
    # Constant for the formula
    year_2013 = 2013
    
    # Calculate the difference between final_year and 2013
    years_difference = final_year - year_2013
    
    # Calculate F4: 1.4% * I4 * (final_year - 2013)
    F4 = 0.014 * I4 * years_difference
    
    return F4

# Example usage
initial_year = 1991
final_year = 2024
I4 = 23012  # Example I4 value
F4 = calculate_pension_F4(I4, final_year)

print(f"Calculated Pension (F4): {F4}")

def pensione_retributiva(initial_year, final_year):
    # Step 1: Calculate I1, I2, I3, and I4 using the previous functions
    I1, I2, I3, I4 = calculate_I_values(initial_year, final_year)
    
    # Step 2: Calculate F1 using I1
    F1 = calculate_pension_F1(I1, initial_year)

    F2 = calculate_pension_F2(I2, initial_year)
    
    # Step 3: Calculate F2 (You can use a similar function for F2 if necessary)
    # Assuming you already have the F2 formula similar to the previous ones.
    
    # Step 4: Calculate F3 using I3
    F3 = calculate_pension_F3(I3, initial_year)
    
    # Step 5: Calculate F4 using I4
    F4 = calculate_pension_F4(I4, final_year)
    
    # Step 6: Sum F1, F2, F3, and F4 to get the total pension
    total_pension = F1 +F2+ F3 + F4  # Sum F1 to F4
    
    return total_pension

# Example usage
initial_year = 2010
final_year = 2044
total_pension = pensione_retributiva(initial_year, final_year)

print(f"Total Pension: {total_pension}")

# Example usage
initial_year = 2000
final_year = 2034
total_pension = pensione_retributiva(initial_year, final_year)