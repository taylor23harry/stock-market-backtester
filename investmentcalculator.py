capital = 10000
annual_percentage = 20
time = 5 # Amount of time in years

monthly_contribution = 200
annual_contribution = 4000

for i in range(time):
    i+1
    capital += capital * (annual_percentage / 12)
    capital += monthly_contribution

    if i % 12 == 0:
        capital += annual_contribution
    else:
        pass
