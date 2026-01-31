import pandas as pd

def process_scores(input_file):
    df = pd.read_excel(input_file)
    level_columns = [c for c in df.columns if c != "ParticipantName"]

    df[level_columns] = df[level_columns].apply(pd.to_numeric, errors="coerce")
    df["TotalScore"] = df[level_columns].sum(axis=1)
    df["AverageScore"] = df[level_columns].mean(axis=1)

    df[df["AverageScore"] >= 50][["ParticipantName", "TotalScore", "AverageScore"]] \
        .to_excel("succeeded.xlsx", index=False)

    df[df["AverageScore"] < 50][["ParticipantName", "TotalScore", "AverageScore"]] \
        .to_excel("failed.xlsx", index=False)

    return "succeeded.xlsx", "failed.xlsx"



