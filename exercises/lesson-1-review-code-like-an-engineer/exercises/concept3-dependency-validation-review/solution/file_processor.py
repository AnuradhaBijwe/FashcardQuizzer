"""
Code Review Solution 3: Fixed File Processing with Real Dependencies

Key Issues Fixed:
1. Phantom libraries -> real, existing libraries
2. print() statements -> proper logging
3. Generic exception handling -> specific error types
4. Missing input validation -> basic file checks
"""

import os
import logging
import pandas as pd

# Configure logging instead of using print()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_uploaded_files(file_paths):
    """
    Process multiple uploaded files and return cleaned datasets.
    
    Args:
        file_paths: List of file paths to process
    
    Returns:
        List of pandas DataFrames with processed data
    """
    # Input validation
    if not isinstance(file_paths, list):
        raise ValueError("file_paths must be a list")
    
    if not file_paths:
        logger.warning("No file paths provided")
        return []
    
    results = []

    for file_path in file_paths:
        try:
            # Basic file validation
            if not os.path.exists(file_path):
                logger.error(f"File does not exist: {file_path}")
                continue
            
            if not os.path.isfile(file_path):
                logger.error(f"Path is not a file: {file_path}")
                continue
            
            logger.info(f"Processing file: {file_path}")
            
            # Load file using pandas (real library) based on extension
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.csv':
                raw_data = pd.read_csv(file_path)
            elif file_extension == '.json':
                raw_data = pd.read_json(file_path)
            elif file_extension in ['.xlsx', '.xls']:
                raw_data = pd.read_excel(file_path)
            else:
                logger.warning(f"Unsupported file format: {file_extension}")
                continue
            
            # Clean the data using pandas built-in methods (instead of phantom library)
            cleaned_data = clean_dataframe(raw_data)
            
            # Already a pandas DataFrame, no conversion needed
            results.append(cleaned_data)
            
            logger.info(f"Successfully processed: {file_path} ({len(cleaned_data)} rows)")

        except pd.errors.EmptyDataError:
            logger.error(f"File is empty: {file_path}")
            continue
        except pd.errors.ParserError as e:
            logger.error(f"Error parsing file {file_path}: {e}")
            continue
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            continue
        except PermissionError:
            logger.error(f"Permission denied reading file: {file_path}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error processing {file_path}: {e}")
            continue

    logger.info(f"Processing complete. Successfully processed {len(results)} out of {len(file_paths)} files")
    return results

def clean_dataframe(df):
    """
    Clean pandas DataFrame using built-in pandas methods.
    
    Args:
        df: pandas DataFrame to clean
    
    Returns:
        Cleaned pandas DataFrame
    """
    if df.empty:
        return df
    
    # Remove completely empty rows and columns
    cleaned = df.dropna(how='all').dropna(axis=1, how='all')
    
    # Strip whitespace from string columns
    string_columns = cleaned.select_dtypes(include=['object']).columns
    for col in string_columns:
        cleaned[col] = cleaned[col].astype(str).str.strip()
    
    # Remove rows that are all empty strings after stripping
    cleaned = cleaned.loc[~(cleaned.astype(str) == '').all(axis=1)]
    
    logger.debug(f"Data cleaning: {len(df)} -> {len(cleaned)} rows")
    return cleaned

# Example usage showing the fixed implementation
if __name__ == "__main__":
    # Test with sample files
    test_files = ["sample1.csv", "sample2.json", "nonexistent.xlsx"]
    
    try:
        results = process_uploaded_files(test_files)
        print(f"Successfully processed {len(results)} files")
        
        for i, df in enumerate(results):
            print(f"File {i+1}: {df.shape[0]} rows, {df.shape[1]} columns")
            
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        print(f"Error: {e}")