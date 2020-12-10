import pandas as pd
import sys

def covid_curve_df():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    
    ccdf = pd.read_csv("CovidCurveData.csv", sep='\t') 
    
    # This was to test if data was printing correctly, feel free to remove
    """
    original_stdout = sys.stdout
    with open('CovidCurveDF.txt', 'w', encoding="utf-8") as f:
        sys.stdout = f
        
        print(ccdf)
        
    sys.stdout = original_stdout
    """
    
    return ccdf
    
if __name__ == '__main__':
    covid_curve_df()