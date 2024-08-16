# Load necessary libraries
library(ScottKnott)
library(dplyr)

# Load the data from CSV file
data <- read.csv("../../data/rq1/grouped_refactorings.csv")

# Perform the Kruskal-Wallis test
kruskal_test <- kruskal.test(counts ~ type, data = data)
print(kruskal_test)

# Check if the result is significant
if (kruskal_test$p.value < 0.05) {
  # If significant, proceed with Scott-Knott post-hoc test
  data$rank_counts <- rank(data$counts)
  av <- aov(rank_counts ~ type, data = data)
  sk <- SK(av, which = "type")
  
  # Print the Scott-Knott results
  print(sk)
  
  # Convert Scott-Knott results to a data frame
  sk_results <- as.data.frame(sk$out)
  sk_results$type <- rownames(sk_results)
  
  # Write the results to a CSV file
  write.csv(sk_results, "../../data/rq1/scott_knott_results.csv", row.names = FALSE)
  
  print("Scott-Knott results have been saved to 'scott_knott_results.csv'")
} else {
  print("Kruskal-Wallis test is not significant; no need for post-hoc analysis.")
}

