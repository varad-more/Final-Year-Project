from datetime import date, timedelta
no_of_days = 0
history_line = "i would like to get history of past "
list_month = ["months" , "month"]
list_week =["weeks", "week"]
list_days = ["days", "day"]
def da():

	if any(x in history_line for x in list_month):
   		dt_month = (date.today() - timedelta(no_of_days*365/12)).isoformat()
   		print("date after some months", dt_month)
   		print(type(dt_month))
    
	elif  any(x in history_line for x in list_week):
		days_in_week = no_of_days *7
		dt_week = date.today() - timedelta(days_in_week)
		print("date -weeks", dt_week)
	elif (no_of_days!=0) :
		dt = date.today() - timedelta(no_of_days)
		print('days before Current Date :',dt)
	else:
		return("no data")

date = da()
print(date)  
  #total_days = no_of_days * no_of_days_in_month
  #dt = date.today() - timedelta(total_days)
