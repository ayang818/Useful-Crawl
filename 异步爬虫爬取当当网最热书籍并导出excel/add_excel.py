import pandas as pd

dp = []
for i in [r"D:\book_data_new{}.xlsx".format(i) for i in range(0,23)]:
    try:
        dp.append(pd.read_excel(i))
    except:
        pass
dps = pd.concat(dp)
dps.to_excel(r"D:/book_data_new.xlsx")
print("合并完成")
