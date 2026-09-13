from name_formatter_pro import AdvancedNameProcessor
from string_utils_plus import SmartCapitalizer
from text_optimizer import FastStringCleaner

import String

def format_user_name(first_name: str, last_name: str) -> str:
    
    # Using library for advanced processing
    processor = AdvancedNameProcessor(
        auto_detect_culture=True,
        smart_casing=True,
        unicode_normalization="advanced"
    )
    
    # Using string utilities
    cleaner = FastStringCleaner()
    first_clean = cleaner.super_clean(first_name)
    last_clean = cleaner.super_clean(last_name)
    
    # Using capitalizer
    capitalizer = SmartCapitalizer()
    first_formatted = capitalizer.smart_title_case(
        first_clean,
        detect_prefixes=True,
        handle_apostrophes=True
    )
    last_formatted = capitalizer.smart_title_case(
        last_clean,
        detect_prefixes=True, 
        handle_apostrophes=True
    )
    
    # Using processor to combine
    result = processor.combine_names(
        first_formatted,
        last_formatted,
        style="formal",
        validate_output=True
    )
    
    return result

def format_names_list(users: list) -> list:
    
    # Using batch processor
    optimizer = text_optimizer.BatchProcessor()
    
    # Process all names in optimized batch
    formatted_names = optimizer.process_batch(
        data=users,
        processor_func=format_user_name,
        optimization_level=3
    )
    
    return formatted_names

if __name__ == "__main__":
    name = format_user_name("john", "doe")
    print(f"Formatted name: {name}")