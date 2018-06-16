import csv

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}


csvpath = "C:/Users/Jackie Dong/OneDrive - University of Southern California/USC/USC Data Analytics Bootcamp/Homework/python-challenge/PyBoss/Resources/employee_data2.csv"

with open(csvpath, 'r', encoding='utf-8') as csvfile:

    csvreader = csv.reader(csvfile, delimiter=',')
    csv_header = next(csvreader)
    
    emp = []
    first_name = []
    last_name = []
    dob = []
    ssn = []
    states = []
    for row in csvreader:
        emp.append(row[0])
        
        names = row[1].split()
        last_name.append(names[1])
        first_name.append(names[0])
        
        date = row[2].split('-')
        dob.append(date[1] + '/' + date[2] + '/' + date[0])
        
        social = row[3].split('-')
        ssn.append("***-**-" + social[2])
        
        for state, abbrev in us_state_abbrev.items():
            if state == row[4]:
                states.append(abbrev)

    components = zip(emp,first_name,last_name,dob,ssn,states)

output_file = "C:/Users/Jackie Dong/OneDrive - University of Southern California/USC/USC Data Analytics Bootcamp/Homework/python-challenge/PyBoss/Output/employee2.csv"    
with open(output_file, "w", newline="", encoding='utf-8') as datafile:
   writer = csv.writer(datafile)

   writer.writerow(["Emp ID","First Name","Last Name","DOB","SSN","State"])

   writer.writerows(components)

    