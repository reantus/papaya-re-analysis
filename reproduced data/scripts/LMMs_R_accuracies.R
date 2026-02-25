library(lme4) 

current_working_dir <- dirname(rstudioapi::getActiveDocumentContext()$path)
setwd(current_working_dir)

data <- read.csv('file_with_data_without_outliers_accuracies.csv')


data$flanker_condition <- factor(data$flanker_condition,
labels=c("unrelated","relatedn-3", "relatedn-2", "relatedn-1", "relatedn+1", "relatedn+2", "relatedn+3"))


data$flanker_condition <- relevel(data$flanker_condition, ref="unrelated")

#data$response_time_keyboard_response <- log(data$response_time_keyboard_response)


model1 <- glmer(
  correct_keyboard_response ~ flanker_condition + (1|Participant_unique_ID) + (1|target),
  data = data, family="binomial" )

summary(model1)



