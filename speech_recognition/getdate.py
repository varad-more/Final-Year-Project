from datetime import date, timedelta
no_of_days = 2
history_line = "i would like to get history of past 2 month"
list_month = ["months" , "month"]
list_week =["weeks", "week"]
list_days = ["days", "day"]

if any(x in history_line for x in list_month):
    dt_month = (date.today() - timedelta(no_of_days*365/12)).isoformat()
    print("date after some months", dt_month)
    print(type(dt_month))
    
elif  any(x in history_line for x in list_week):
    days_in_week = no_of_days *7
    dt_week = date.today() - timedelta(days_in_week)
    print("date -weeks", dt_week)
else :
    dt = date.today() - timedelta(no_of_days)
    print('days before Current Date :',dt)


    
  #total_days = no_of_days * no_of_days_in_month
  #dt = date.today() - timedelta(total_days)
