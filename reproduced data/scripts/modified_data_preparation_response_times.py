import pandas as pd

# Reading data from 98 participants and checking their overall accuracy.
df_data = pd.read_csv(
    "../../original_data/Experiment_2/Data/data.csv"
)

list_sufficient_accuracy = []

# Our df_only_sufficient_accuracy contains data of participants with the overall accuracy above or exactly 70 %.
for participant_unique_ID, df_one_participant in df_data.groupby(
    "Participant_unique_ID"
):

    accuracy = df_one_participant["correct_keyboard_response"].mean()
    if accuracy >= 0.70:
        list_sufficient_accuracy.append(participant_unique_ID)

df_only_sufficient_accuracy = df_data[
    df_data["Participant_unique_ID"].isin(list_sufficient_accuracy)
]

# Working with participants with sufficient overall accuracy, we are excluding outliers per participant per condition.
# We only take correctly answered word trials, as we are preparing a file for the analysis of response times.
df_all_people_without_outliers = pd.DataFrame()
list_upper_and_lower_values = []

for participant_ID, df_participant in df_only_sufficient_accuracy.groupby(
    "Participant_unique_ID"
):

    df_word_correct = df_participant[
        (df_participant["correct_keyboard_response"] == 1)
        & (df_participant["target_type"] == "word")
    ]

    participant_boundaries = [participant_ID]
    df_subject_without_outliers = pd.DataFrame()

    # Looping through all 7 flanker conditions and excluding outliers (more than 2.5 standard deviations above or below the mean value)
    # based on the mean and standard deviation calculated per condition per participant.
    for flanker_condition, df_condition in df_word_correct.groupby("flanker_condition"):

        cond_time_mean = df_condition["response_time_keyboard_response"].mean()
        cond_time_std = df_condition["response_time_keyboard_response"].std()

        upper_boundary = cond_time_mean + 2.5 * cond_time_std
        lower_boundary = cond_time_mean - 2.5 * cond_time_std

        df_cond_without_outliers = df_condition[
            ((df_condition["response_time_keyboard_response"]) > (lower_boundary))
            & ((df_condition["response_time_keyboard_response"]) < (upper_boundary))
        ]

        participant_boundaries.extend(
            [flanker_condition, upper_boundary, lower_boundary]
        )

        # This dataframe contains data without outliers of a single participant.
        df_subject_without_outliers = pd.concat(
            [df_cond_without_outliers, df_subject_without_outliers], ignore_index=True
        )

    # Upper and lower cut-off boundaries per participant per condition are saved into a list,
    # as they will be applied for defining outliers for the analysis of accuracies as well.
    list_upper_and_lower_values.append(participant_boundaries)

    # This dataframe contains data without outliers for all the participants with the sufficient overall accuracy.
    df_all_people_without_outliers = pd.concat(
        [df_all_people_without_outliers, df_subject_without_outliers], ignore_index=True
    )

# Extracting target word from the whole stimulus.
for i in range(len(df_all_people_without_outliers)):
    row = df_all_people_without_outliers["stimulus"][i]
    word = row.split(" ")[3]
    df_all_people_without_outliers.at[i, "target"] = word

# Saving the file with all correctly answered participants' word trials without outliers for the analyis of response times.
df_all_people_without_outliers.to_csv(
    "file_with_data_without_outliers_response_times.csv"
)



# Same upper and lower cut-off boundaries per participant per condition as for the response times analysis will be applied to define outliers.
# We are firstly creating a dataframe (from a previously created list_upper_and_lower_values) with subject numbers and upper and lower boundaries per condition.
df_limits = pd.DataFrame()
participants = []

for participant in list_upper_and_lower_values:
    unique_ID = participant[0]
    conditions = participant[1:]

    # Looping through the 7 flanker conditions, finding upper and lower boundaries.
    for i in range(0, len(conditions), 3):
        condition = conditions[i]
        upper_value = conditions[i + 1]
        lower_value = conditions[i + 2]
        participants.append([unique_ID, condition, upper_value, lower_value])


df_limits = pd.DataFrame(
    participants,
    columns=[
        "Participant_unique_ID",
        "flanker_condition",
        "upper_boundary",
        "lower_boundary",
    ],
)

# Creating a dataframe with all trials from participants with the sufficient overall accuracy and merging it with the newly created dataframe
# with upper and lower boundaries per condition per participant.
df_all_data_with_boundaries = df_only_sufficient_accuracy.merge(
    df_limits,
    left_on=["Participant_unique_ID", "flanker_condition"],
    right_on=["Participant_unique_ID", "flanker_condition"],
    how="inner",
)

# This dataframe will be used when defining outliers for the incorrectly answered trials for the analysis of accuracies (the next Jupyter Notebook file).
df_all_data_with_boundaries.to_csv("all_data_with_boundaries.csv")