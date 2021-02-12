from datetime import datetime,timedelta

def get_daily_slots(start, end, slot, date):
    # combine start time to respective day
    dt = datetime.combine(date, datetime.strptime(start,"%H:%M").time())
    slots = [dt]
    # increment current time by slot till the end time
    while (dt.time() < datetime.strptime(end,"%H:%M").time()):
        dt = dt + timedelta(minutes=slot)
        slots.append(dt)
    return slots

# Some Dummy values 
start_time = '9:00'
end_time = '15:00'
slot_time = 20
days = 2
start_date = datetime.now().date()

unavailable_slot=[]


for i in range(days):
    date_required = datetime.now().date() + timedelta(days=1)
    list_date_available = get_daily_slots(start=start_time, end=end_time, slot=slot_time, date=date_required)
    # print (get_daily_slots(start=start_time, end=end_time, slot=slot_time, date=date_required))

for i in list_date_available:
    print(i)
    print(i.year)
    print(i.month)
    print(i.day)
    print(i.hour)
    print(i.minute)
    if i.year == 2021 and i.month== 2 and i.day== 12 and i.hour== 15 and i.minute == 0:
        list_date_available.remove(i)
for i in list_date_available:
    print(i)

print(list_date_available)
