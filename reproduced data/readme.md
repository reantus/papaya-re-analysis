# Modifications done
- Note that the scripts provided produce a single-folder structure. In order to keep modifications to the scripts to a minimum, this was kept throughout the process.
- Metadata for the csv used in the RScript are described by the author here:  
    `original_data\Experiment_2\Data\readme.txt`  
    The script in the re-analysis uses one of the files that results from the process described in this readme:
    `re-analysis/scripts/file_with_data_without_outliers_accuracies.csv` 
    A structured metadata for that csv can be found here:  
    `re-analysis/scripts/metadata - file_with_data_without_outliers_accuracies.md` 


1. Extracted and combined the two Python code blocks from  
    `original_data/Experiment_2/Data_analysis/data_preparation_response_times.ipynb`  
    into one Python file in  
    `re-analysis/scripts/modified_data_preparation_response_times.py`  
    The script performs the excact same cleanup task, but can now be run outside of Jupyter.

2. Extracted the Python code blocks from  
    `original_data/Experiment_2/Data_analysis/data_preparation_accuracies.ipynb`  
    into one Python file in  
    `re-analysis/scripts/modified_data_preparation_accuracies.py`  
    The script performs the excact same cleanup task, but can now be run outside of Jupyter.

3. Changed a section in:
    `re-analysis/scripts/modified_data_preparation_accuracies.py`

    from

    ```
    df_data = pd.read_csv(
    "path_to_your_file"
    )
    ```

    to

    ```
    df_data = pd.read_csv(
        "../../original_data/Experiment_2/Data/data.csv"
    )
    ```    
    
    This ensures that the script targets a valid file.  
    The change is necessary for the script to run and justification is provided in the re-analysis.

4. Ran the following script:
    `re-analysis/scripts/modified_data_preparation_response_times.py`  
    This produced the following files:
    `re-analysis/scripts/all_data_with_boundaries.csv`  
    `re-analysis/scripts/file_with_data_without_outliers_response_times.csv`  

5. Ran the following script:
    `re-analysis/scripts/modified_data_preparation_response_times.py`  
    This produced the following file:
    `re-analysis/scripts/file_with_data_without_outliers_accuracies.csv`  

6. Copied the following file:  
    `original_data/Experiment_2/Data_analysis/LMMs_R_accuracies.R`  
    into the folder:  
    `re-analysis/scripts/`

7. Changed a section in  
    `re-analysis/scripts/LMMs_R_accuracies.R`  

    from

    ```
    setwd("path_to_your_file")
    data <- read.csv('file_with_data_without_outliers_accuracies.csv')
    ```

    to

    ```
    current_working_dir <- dirname(rstudioapi::getActiveDocumentContext()$path)
    setwd(current_working_dir)

    data <- read.csv('file_with_data_without_outliers_accuracies.csv')
    ```   

    This ensures that the csv will be discovered by the script running in RStudio, but does not alter the data or interpretation.

8. Run the following script in RStudio:  
    `re-analysis/scripts/LMMs_R_accuracies.R`  


**Note**  
These steps were undertaken to clean up, understand and structure the data given by the authors.  
The changes have been done, and the resulting files have been created.  
Anyone looking look an the models predictions would find it sufficient to run:  
`re-analysis/scripts/LMMs_R_accuracies.R` 