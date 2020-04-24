import pandas as pd

# TODO: Enable getting thresholds for each metric, if any run does not meet the criteria, then disregard the run
directory = r"C:\Users\Iman\Desktop\PerfMetrReport.csv"
df = pd.read_csv(directory, header=0, sep=",", index_col="RunNumber")


# Creates the metrics_dict: 'BestValue' representing perfect match value when sim exactly matches obs and 'Weight' shows
# the importance of the metric in the scoring function, the more the 'Weight' is, the more the metric influences the
#  scoring function
metrics_dict = {
    "NSE": {"BestValue": 1.0, "Weight": 10.0},
    "PB": {"BestValue": 0.0, "Weight": 10.0},
    "RMSE": {"BestValue": 0.0, "Weight": 10.0},
    "R_squared": {"BestValue": 1.0, "Weight": 10.0},
}

df_eval = df.copy()
for column in df.columns:
    df_eval["{}_eval".format(column)] = abs(
        df_eval[column] - metrics_dict["{}".format(column)]["BestValue"]
    )
    df_eval["{}_Score".format(column)] = df_eval["{}_eval".format(column)].rank(
        ascending=False
    )

df_eval["Score"] = 0
weights_sum = 0
for column in df.columns:
    df_eval["Score"] += (
        df_eval["{}_Score".format(column)] * metrics_dict["{}".format(column)]["Weight"]
    )
    weights_sum += metrics_dict["{}".format(column)]["Weight"]

# Create a sorted dataframe with based on the ranks
df_sorted = df.copy()
df_sorted["Score"] = df_eval["Score"] / weights_sum
df_sorted["Rank"] = df_sorted["Score"].rank(ascending=False)
df_sorted.sort_values("Rank", inplace=True)
df_sorted = round(df_sorted, 3)

del df_eval

df_sorted.to_csv(r"C:\Users\Iman\Desktop\SortedPerfMetrReport.csv")
