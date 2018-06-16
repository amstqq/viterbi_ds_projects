import csv

csvpath = "C:/Users/Jackie Dong/OneDrive - University of Southern California/USC/USC Data Analytics Bootcamp/Homework/python-challenge/PyBank/Resources/budget_data_1.csv"

with open(csvpath, 'r', encoding='utf-8') as csvfile:

    csvreader = csv.reader(csvfile, delimiter=',')
    csv_header = next(csvreader)
    
    total_rev = 0
    total_change_rev = 0
    max_increase_rev = 0
    max_decrease_rev = 0
    
    for row in csvreader:
        total_rev = total_rev + int(row[1])
        if csvreader.line_num == 2:
            previous_rev = int(row[1])
        else:
            current_rev = int(row[1])
            change_rev = current_rev - previous_rev
            total_change_rev = total_change_rev + abs(change_rev)
            if change_rev > max_increase_rev:
                max_increase_rev = change_rev
                max_increase_month = str(row[0])
            if change_rev < max_decrease_rev:
                max_decrease_rev = change_rev
                max_decrease_month = str(row[0])
            previous_rev = int(row[1])
            
    total_month = csvreader.line_num - 1
    avg_change_rev = total_change_rev / (total_month-1)
    
    print(f"Financial Analysis \n----------------------------\nTotal Months: {total_month}\nTotal Revenue: ${total_rev}\nAverage Revenue Change: ${int(avg_change_rev)}\nGreatest Increase in Revenue: {max_increase_month} (${max_increase_rev})\nGreatest Decrease in Revenue: {max_decrease_month} (${max_decrease_rev})")
    
output = "C:/Users/Jackie Dong/OneDrive - University of Southern California/USC/USC Data Analytics Bootcamp/Homework/python-challenge/PyBank/Output/Analysis_1.txt"
with open(output,'w',newline='', encoding='utf-8') as datafile:
   datafile.write(f"Financial Analysis \n----------------------------\nTotal Months: {total_month}\nTotal Revenue: ${total_rev}\nAverage Revenue Change: ${int(avg_change_rev)}\nGreatest Increase in Revenue: {max_increase_month} (${max_increase_rev})\nGreatest Decrease in Revenue: {max_decrease_month} (${max_decrease_rev})")
   datafile.close()
            
        
        