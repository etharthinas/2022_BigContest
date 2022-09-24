# basic importing
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', None)

# read data
log = pd.read_csv("log_data.csv")
loan = pd.read_csv("loan_result.csv")
user = pd.read_csv("user_spec.csv")

joined = loan.join(user.set_index("application_id"), on="application_id")

# basic preprocessing
j = joined.dropna(subset = ["loan_limit", "loan_rate"])
mean_income = j.yearly_income.mean()
j.yearly_income = j.yearly_income.fillna(mean_income)
median_birth_year = j.birth_year.median()
j.birth_year = j.birth_year.fillna(median_birth_year)
j.birth_year = pd.to_datetime(j.birth_year, format = "%Y")
j[["personal_rehabilitation_yn", "personal_rehabilitation_complete_yn", 
   "existing_loan_cnt", "existing_loan_amt"]] = j[["personal_rehabilitation_yn", 
    "personal_rehabilitation_complete_yn", "existing_loan_cnt", "existing_loan_amt"]].fillna(0)

# company_enter_month
j.company_enter_month = j.company_enter_month.fillna(202206)
j.company_enter_month = j.company_enter_month.astype("str").str[:6]
x = j.company_enter_month.str[:6]
x = pd.to_datetime(x, format = "%Y%m")
j.company_enter_month = x
j.loanapply_insert_time = pd.to_datetime(j.loanapply_insert_time)
j.user_id = j.user_id.astype(int)

# gender
p = j[j.gender.isna()]
k = j[~j.gender.isna()]
total = len(k.user_id.unique())
by_user = k.groupby("user_id").max()
num_males = by_user.gender.sum()
prob = num_males / total
userid = p.user_id.unique()
np.random.seed(0)
arr = np.random.binomial(1, prob, len(userid))
user_gender = dict(zip(userid, arr))
a = j.loc[j.user_id.isin(userid)].groupby(j.user_id).max()
notnaid = a[~a.gㅎender.isna()].user_id
notnagender = a[~a.gender.isna()].gender
z = dict(zip(notnaid, notnagender))
j.gender = j.gender.fillna(j.user_id.map(z))
j.gender = j.gender.fillna(j.user_id.map(user_gender))

# export
j.to_csv("joined.csv")
