"""
Code Review Exercise 3: File Processing with Dependencies

Your task: Review this file processing code for dependency and structural issues.
Focus on:
- Library imports and dependencies
- Code structure and error handling
- Function design and testability

Instructions:
1. Verify all imported libraries are valid
2. Check for structural patterns and issues
3. Evaluate error handling approach
4. Rate the overall code quality (Poor, Fair, Good, Excellent)
5. Provide your recommendation (Accept, Modify, Reject)
"""

import os
import logging
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_file(file_path: str) -> pd.DataFrame:
    """
    Load a file using pandas with support for multiple formats.

    Args:
        file_path: Path to the file to load

    Returns:
        DataFrame containing the loaded data

    Raises:
        ValueError: If file format is not supported
        FileNotFoundError: If file does not exist
    """
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.csv':
        return pd.read_csv(file_path)
    elif file_extension in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    elif file_extension == '.json':
        return pd.read_json(file_path)
    elif file_extension == '.parquet':
        return pd.read_parquet(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")


def clean_dataset(df: pd.DataFrame, method: str = 'mean') -> pd.DataFrame:
    """
    Clean dataset by handling missing values and standardizing numeric columns.

    Args:
        df: DataFrame to clean
        method: Imputation method ('mean', 'median', 'most_frequent')

    Returns:
        Cleaned DataFrame
    """
    df_cleaned = df.copy()

    # Separate numeric and non-numeric columns
    numeric_cols = df_cleaned.select_dtypes(include=['number']).columns

    if len(numeric_cols) > 0:
        # Handle missing values in numeric columns
        imputer = SimpleImputer(strategy=method)
        df_cleaned[numeric_cols] = imputer.fit_transform(df_cleaned[numeric_cols])

        # Standardize numeric columns
        scaler = StandardScaler()
        df_cleaned[numeric_cols] = scaler.fit_transform(df_cleaned[numeric_cols])

    # Drop rows with all missing values
    df_cleaned = df_cleaned.dropna(how='all')

    return df_cleaned


def process_uploaded_files(file_paths: list[str], clean_method: str = 'mean') -> list[pd.DataFrame]:
    """
    Process multiple uploaded files and return cleaned datasets.

    Args:
        file_paths: List of file paths to process
        clean_method: Method for imputing missing values

    Returns:
        List of cleaned DataFrames
    """
    results = []

    for file_path in file_paths:
        try:
            # Load the file
            df = load_file(file_path)
            logger.info(f"Successfully loaded {file_path}: {df.shape[0]} rows, {df.shape[1]} columns")

            # Clean the dataset
            df_cleaned = clean_dataset(df, method=clean_method)
            logger.info(f"Cleaned {file_path}: {df_cleaned.shape[0]} rows remaining")

            results.append(df_cleaned)

        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
        except ValueError as e:
            logger.error(f"Invalid file format for {file_path}: {e}")
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")

    return results

def validate_file_paths(file_paths: list[str]) -> list[str]:
    """
    Validate that all file paths exist and are accessible.

    Args:
        file_paths: List of file paths to validate

    Returns:
        List of valid file paths
    """
    valid_paths = []
    for path in file_paths:
        if os.path.exists(path):
            valid_paths.append(path)
        else:
            logger.warning(f"File not found: {path}")
    return valid_paths