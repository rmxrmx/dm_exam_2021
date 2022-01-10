import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('data_with_percentiles.csv', index_col=0, header=0)

print(data)
#c = data["remainTime"].corr(data["ownCon"])
d = pearsonr(data["remainTime"], data["age"])
print(d)
# Take only stuff not from the pilot study
processed = data.loc[data["Session0_Pilot1"] == 0]

avg_times_per_round = np.zeros(40)
avg_profit_top25 = np.zeros(40)
avg_profit_bot25 = np.zeros(40)
avg_profit_rest = np.zeros(40)
for i in range(40):
    avg_times_per_round[i] = 60 - np.sum(processed.loc[processed["Period"] == i+1]["remainTime"]) / 120

print(avg_times_per_round)
plt.plot(range(1, 41), avg_times_per_round, color='darkgreen')
plt.xlabel("trial round, #")
plt.ylabel("average time taken, s")
plt.title("Average time taken to make a choice over trial")
plt.grid(True)
plt.show()


avg_times_per_participant = np.zeros(120)
profit_per_participant = np.zeros(120)
age_per_participant = np.zeros(120)
gender_per_participant = np.zeros(120)
for i in range(120):
    avg_times_per_participant[i] = 60 - np.sum(processed.loc[processed["Subject"] == i+1]["remainTime"]) / 40
    profit_per_participant[i] = np.sum(processed.loc[processed["Subject"] == i+1]["totalPay"])
    age_per_participant[i] = processed.loc[processed["Subject"] == i+1]["age"].to_numpy()[0]
    gender_per_participant[i] = processed.loc[processed["Subject"] == i+1]["gender"].to_numpy()[0]


# profit_normalized = [float(i)/max(profit_per_participant) for i in profit_per_participant]
# times_normalized = [float(i)/max(avg_times_per_participant) for i in avg_times_per_participant]

# !!! MAIN IDEA: PROFIT CORRELATES WITH TIME TAKEN
print("Total profit with avg time taken: ", pearsonr(avg_times_per_participant, profit_per_participant))
print("Profit each round with remaining time: ", pearsonr(processed["profit"], processed["remainTime"]))
print("Age and profit: ", pearsonr(age_per_participant, profit_per_participant))
print("Age and speed: ", pearsonr(age_per_participant, avg_times_per_participant))
print("Gender and speed: ", pearsonr(gender_per_participant, avg_times_per_participant))
print("Gender and profit: ", pearsonr(gender_per_participant, profit_per_participant))




plt.scatter(range(1, 121), avg_times_per_participant, color='darkgreen')
plt.xlabel("participant, #")
plt.ylabel("average time taken, s")
plt.title("Average time taken to make a choice for each participant over all rounds")
plt.show()

print(pd.DataFrame(avg_times_per_participant).describe())
# print()
top25 = (avg_times_per_participant <= 20.531250).nonzero()
bot25 = (avg_times_per_participant >= 31.075000).nonzero()
# data["timing"] = 1
#
# # TOP 25: 2, BOT 25: 0
# for idx, row in data.iterrows():
#     if row["Subject"] in top25[0]:
#         data.loc[data["Subject"] == row["Subject"], "timing"] = 2
#     if row["Subject"] in bot25[0]:
#         data.loc[data["Subject"] == row["Subject"], "timing"] = 0
# print(data)
#
# data.to_csv("data_with_percentiles.csv")

for i in range(40):
    avg_profit_top25[i] = np.sum(processed.loc[(processed["timing"] == 2) & (processed["Period"] == i+1)]["profit"]) / len(top25[0])
    avg_profit_bot25[i] = np.sum(processed.loc[(processed["timing"] == 0) & (processed["Period"] == i+1)]["profit"]) / len(bot25[0])
    avg_profit_rest[i] = np.sum(processed.loc[(processed["timing"] == 1) & (processed["Period"] == i+1)]["profit"]) / (120 - len(bot25[0]) - len(top25[0]))

plt.plot(avg_profit_top25, label="top 25%")
plt.plot(avg_profit_bot25, label="bottom 25%")
plt.plot(avg_profit_rest, label="the rest")
plt.xlabel("trial round, #")
plt.ylabel("average profit per round, ECU")
plt.title("Average profit per round of 3 categories")
plt.legend()
plt.show()

names = ["top 25%", "bottom 25%", "the rest"]
values = [np.sum(avg_profit_top25), np.sum(avg_profit_bot25), np.sum(avg_profit_rest)]

print(values)