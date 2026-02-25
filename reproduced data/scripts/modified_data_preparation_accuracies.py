import pandas as pd 

# Importing the files created with the previous Jupyter Notebook code.
df_all_data_with_boundaries = pd.read_csv("all_data_with_boundaries.csv")
df_word_correct_without_outliers = pd.read_csv(
    "file_with_data_without_outliers_response_times.csv"
)

df_all_people_without_outliers_analysis_of_accuracies = pd.DataFrame()

# The file with correct word trials without outliers was prepared with the previous Jupyter Notebook code.
# Here, outliers for the incorrect word trials are excluded based on the lower and upper boundaries calculated for the response time analysis with correct word trials.
for unique_number, df_one_participant in df_all_data_with_boundaries.groupby(
    "Participant_unique_ID"
):

    df_word_incorrect = df_one_participant[
        (df_one_participant["correct_keyboard_response"] == 0)
        & (df_one_participant["target_type"] == "word")
    ]

    df_subject_without_outliers_analysis_of_accuracies = pd.DataFrame()

    for flanker_condition, df_condition in df_word_incorrect.groupby(
        "flanker_condition"
    ):

        df_cond_without_outliers = df_condition[
            (
                (df_condition["response_time_keyboard_response"])
                > (df_condition["lower_boundary"])
            )
            & (
                (df_condition["response_time_keyboard_response"])
                < (df_condition["upper_boundary"])
            )
        ]
        # This dataframe containes outliers-free incorreclty answered trials per participant.
        df_subject_without_outliers_analysis_of_accuracies = pd.concat(
            [
                df_cond_without_outliers,
                df_subject_without_outliers_analysis_of_accuracies,
            ],
            ignore_index=True,
        )
    # This dataframe contains outliers-free incorreclty answered trials for all of the participants.
    df_all_people_without_outliers_analysis_of_accuracies = pd.concat(
        [
            df_all_people_without_outliers_analysis_of_accuracies,
            df_subject_without_outliers_analysis_of_accuracies,
        ],
        ignore_index=True,
    )

df_all_people_without_outliers_analysis_of_accuracies_dropped = (
    df_all_people_without_outliers_analysis_of_accuracies.drop(
        columns=["upper_boundary", "lower_boundary"]
    )
)
# Extracting a column 'target' from the column 'stimulus'.
for i in range(len(df_all_people_without_outliers_analysis_of_accuracies_dropped)):
    row = df_all_people_without_outliers_analysis_of_accuracies_dropped["stimulus"][i]
    word = row.split(" ")[3]
    df_all_people_without_outliers_analysis_of_accuracies_dropped.at[i, "target"] = word

# Merging the file with the correct word trials without outliers and the file with the incorrect word trials without outliers for the analysis of accuracies.
df_all = pd.concat(
    [
        df_all_people_without_outliers_analysis_of_accuracies_dropped,
        df_word_correct_without_outliers,
    ],
    ignore_index=True,
)

df_all.to_csv("file_with_data_without_outliers_accuracies.csv")