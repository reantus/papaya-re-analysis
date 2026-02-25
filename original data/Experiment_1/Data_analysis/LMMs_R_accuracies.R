library(lme4) 

setwd(path_to_your_file)
data <- read.csv("file_with_data_without_outliers_accuracies.csv")


data$flanker_condition <- factor(data$flanker_condition,
labels=c("unrelated","relatedn-3", "relatedn-2", "relatedn-1", "relatedn+1", "relatedn+2", "relatedn+3"))


data$flanker_condition <- relevel(data$flanker_condition, ref="unrelated")
#data$response_time_keyboard_response_1 <- log(data$response_time_keyboard_response_1)


model1 <- glmer(
    correct_keyboard_response_1 ~ flanker_condition + (1|subject_nr),
    data=data, family="binomial" )

summary(model1)