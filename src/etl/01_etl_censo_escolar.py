import pandas as pd
from typing import List, Dict

# Global variables and Settings
INPUT_PATH = 'data/raw/microdados_ed_basica_2024.csv'
OUTPUT_PATH = 'data/processed/censo_escolar_2024_RJ_Enderecos&Matriculas.csv'

TARGET_MUNICIPALITIES = [3304557, 3303302, 3304904, 3301900] # Rio, Niterói, Itaboraí and São Gonçalo
TARGET_COLUMNS = [
    'NO_ENTIDADE', 'DS_ENDERECO', 'NU_ENDERECO', 'CO_CEP', 'NO_BAIRRO', 
    'NO_MUNICIPIO', 'NO_UF', 'QT_MAT_BAS', 'QT_MAT_INF', 'QT_MAT_FUND', 
    'QT_MAT_MED', 'QT_MAT_MED_CT', 'QT_MAT_PROF', 'QT_MAT_EJA', 'QT_MAT_ESP'
]
NUMERIC_COLUMNS = [
    'QT_MAT_BAS', 'QT_MAT_INF', 'QT_MAT_FUND', 'QT_MAT_MED', 
    'QT_MAT_PROF', 'QT_MAT_EJA', 'QT_MAT_ESP', 'QT_MAT_MED_CT'
]



def load_and_filter_data(filepath: str, cities: List[int], columns: List[str]) -> pd.DataFrame:
    """Loads the Census microdata and performs spatial and column filtering."""
    print("Starting data extraction...")

    try:
        df = pd.read_csv(filepath, encoding='latin1', delimiter=';', usecols=lambda c: c in columns or c == 'CO_MUNICIPIO')
        print(f"Total original records loaded: {len(df)}")

        filtered_df = df[df['CO_MUNICIPIO'].isin(cities)].copy()
        filtered_df['NO_UF'] = 'RJ'
        filtered_df = filtered_df[columns] # Keeps only the columns of interest
        
        print(f"Filter applied. Final records: {len(filtered_df)}")
        return filtered_df

    except FileNotFoundError:
        print(f"File not found at path: {filepath}")
        raise



def validate_enrollments_vectorized(df: pd.DataFrame) -> None:
    """Validates enrollment consistency using Pandas vectorized operations."""
    print("Performing exploratory analysis and enrollment validation...")


    df[NUMERIC_COLUMNS] = df[NUMERIC_COLUMNS].fillna(0).astype(int)
    
    columns_to_sum = ['QT_MAT_INF', 'QT_MAT_FUND', 'QT_MAT_MED', 'QT_MAT_EJA', 'QT_MAT_MED_CT']
    
    calculated_sum = df[columns_to_sum].sum(axis=1)
    
    valid_mask = (calculated_sum == df['QT_MAT_BAS'])
    
    count_true = valid_mask.sum()
    count_false = (~valid_mask).sum()
    
    print(f"Validation completed -> Consistent (True): {count_true} | Inconsistent (False): {count_false}")



def clean_address_numbers(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans and standardizes the NU_ENDERECO column based on predefined values."""
    print("Starting address numbers cleaning and standardization...")

    df['NU_ENDERECO'] = df['NU_ENDERECO'].astype(str).str.replace(r'\.0$', '', regex=True)
    
    # Identifies non-purely numeric values
    dirty_mask = ~df['NU_ENDERECO'].str.isdigit()
    addresses_NA = df.loc[dirty_mask, 'NU_ENDERECO'].unique().tolist()
    
    # Records obtained above cleaned
    cleaned_addresses_NA = [0, 0, 0, 0, 10, 0, 0, 167, 0, 38, 0, 0, 544, 0, 0, 0, 620, 60, 813, 10,
    1156, 1181, 29, 24, 132, 49, 224, 14, 5, 27, 350, 537, 294, 0, 355, 0, 31, 17,
    234, 0, 3, 70, 0, 103, 390, 574, 0, 204, 25976, 14809, 234, 289, 17, 0, 0,
    0, 3323, 7523, 0, 8505, 323, 445, 104, 0, 1696, 109, 1386, 1340, 18476, 2514, 477,
    57, 191, 35, 31, 6, 114, 11, 205, 3, 20, 343, 3, 1310, 120, 161, 1, 18, 6475,
    6700, 730, 41, 75, 342, 746, 27, 30, 588, 80, 936, 1645, 76, 73, 142, 96,
    21, 1004, 103, 55, 2, 39, 0, 0, 0, 11, 9183, 5974, 302, 302, 3325, 40, 285, 117,
    13501, 54, 31, 0, 82, 21, 4480, 618, 0, 96, 5, 498, 115, 361, 19, 191, 24, 1049,
    1686, 20, 55, 214, 130, 580, 59, 638, 60, 225, 492, 590, 35, 105, 239, 6810,
    3896, 368, 29, 234, 541, 19400, 0, 32, 25, 2376, 59, 74, 12, 554, 0, 0, 0,
    493, 47, 0, 40, 0, 557, 8, 542, 13, 0, 37, 20]
    
    # Checks if lists have the same size before creating the dictionary
    if len(addresses_NA) <= len(cleaned_addresses_NA):
        mapping = dict(zip(addresses_NA, cleaned_addresses_NA[:len(addresses_NA)]))
        
        # Applies mapping using vectorized .replace()
        df['NU_ENDERECO'] = df['NU_ENDERECO'].replace(mapping)
    else:
        print("The replacement list is smaller than the unique values found. Check the data.")
    
    df['NU_ENDERECO'] = df['NU_ENDERECO'].fillna(0)


    print("NU_ENDERECO column cleaning completed successfully.")
    return df



def main():
    """Main function that orchestrates the ETL pipeline."""
    print("# Starting Pipeline #")

    census_df = load_and_filter_data(INPUT_PATH, TARGET_MUNICIPALITIES, TARGET_COLUMNS)
    
    validate_enrollments_vectorized(census_df)
    
    census_df = clean_address_numbers(census_df)
    
    census_df.to_csv(OUTPUT_PATH, index=False, header=True)
    print(f"# Pipeline finished. Data saved to: {OUTPUT_PATH} #")


if __name__ == "__main__":
    main()