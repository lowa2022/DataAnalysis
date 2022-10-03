import unicodecsv as cs
from faker import Faker
from datetime import date
#from datetime import datetime
import datetime
import random
import string
import configparser
import time
import csv
import re

# record start time
start = time.time()  # start time

config = configparser.ConfigParser()  # assign configparser to config
config.read('config.ini')  # read config.ini file

fake = Faker('en_US')  # US

locales = 'en_IN', 'en_US', 'es_ES', 'en_PH'  # list of the locales
faker = Faker(locales)  # Diversified


# faker = Faker(config['General']['Locale']) #not working
def anonymize(sourcefile):
    # Anonymizes the given original data to anonymized form
    with open(
            sourcefile, 'rb'
    ) as f:  # automatically close reldata.csv when it’s not needed anymore
        with open("fakedata.csv", 'wb') as o:
            # Use the DictReader to easily extract fields
            reader = cs.DictReader(f)
            writer = cs.DictWriter(o, reader.fieldnames)
            # write header only if required
            if config["General"]["WriteHeaderInOutput"] == "Yes":
                writer.writeheader()  # writes the headers
            else:
                pass

            for row in reader:
                # if gender in list of column names
                if config['Mappings']['Gender'] not in list_of_column_names[0]:
                    pass
                else:
                    row[config['Mappings']['Gender']] = row[
                        config['Mappings']['Gender']].strip(' ')
                    row[config['Mappings']['Gender']] = row[
                        config['Mappings']['Gender']].capitalize()

                    # if First in column names
                if config['Mappings']['First'] not in list_of_column_names[0]:
                    pass
                else:
                    if row[
                        config['Mappings']
                            ['Gender']] == 'Male' or 'M':  # create male names for male
                        row[config['Mappings']
                            ['First']] = faker.first_name_male()
                    elif row[config['Mappings']['Gender']] == 'Female' or 'F':
                        row[config['Mappings']
                            ['First']] = faker.first_name_female(
                        )  # female names for females
                    else:
                        row[config['Mappings']['First']] = faker.first_name()

                # check if last nmae in dataset
                if config['Mappings']['Last'] not in list_of_column_names[0]:
                    pass
                else:
                    row[config['Mappings']['Last']] = faker.last_name()

                # check if street in data set
                if config['Mappings']['Street'] not in list_of_column_names[0]:
                    pass
                else:
                    if not row[config['Mappings']
                               ['Street']]:  # for empty cells
                        row[config['Mappings']['Street']] = None
                    else:
                        row[config['Mappings']
                            ['Street']] = fake.street_address()

                # dates according to users locale
                if config['Mappings']['DOB'] not in list_of_column_names[0]:
                    pass
                else:
                    if not row[config['Mappings']['DOB']]:
                        row[config['Mappings']['DOB']] = None
                    else:
                        date_str = row[config['Mappings']
                                       ['DOB']]  # get the person's dob
                        date_obj = datetime.datetime.strptime(
                            date_str, '%m/%d/%Y')  # strip the time in format
                        birthYear = date_obj.year  # get the birth year
                        row[config['Mappings']['DOB']] = GetValidDob(
                            birthYear
                        )  # using get Birth year function, generate new valid DOB

                # for fake person's dob
                date_str = row[config['Mappings']['DOB']]
                # getting the fake persons dob to generate new data
                new_date_obj = datetime.datetime.strptime(
                    date_str, '%m/%d/%Y')  # strip in format
                new_birthYear = new_date_obj.year  # get year
                new_birthMonth = new_date_obj.month  # get month
                new_birthDay = new_date_obj.day  # get day

                # ssn

                if config['Mappings']['SSN'] not in list_of_column_names[0]:
                    pass
                else:
                    if '-' in row[config['Mappings']['SSN']]:
                        row[config['Mappings']['SSN']] = fake.ssn(
                        )  # only dases if the original had dashes, otherwise empty spaces
                    else:
                        row[config['Mappings']['SSN']] = fake.ssn().translate(
                            {ord("-"): None})  # dont use dashes

                # email
                emailfunctions = [
                    firstnameemail(row[config['Mappings']['First']],
                                   row[config['Mappings']['Last']]),
                    lastnameemail(row[config['Mappings']['First']],
                                  row[config['Mappings']['Last']]),
                    fLastNameemail(row[config['Mappings']['First']],
                                   row[config['Mappings']['Last']])
                ]  # use from these fucntions

                if config['Mappings']['Email'] not in list_of_column_names[0]:
                    pass
                else:
                    if not row[config['Mappings']['Email']]:  # for empty cells
                        row[config['Mappings']['Email']] = None
                    else:
                        row[config['Mappings']['Email']] = random.choice(
                            emailfunctions)

                if config['Mappings']['Phone'] not in list_of_column_names[0]:
                    pass
                else:
                    if not row[config['Mappings']['Phone']]:  # for empty cells
                        row[config['Mappings']['Phone']] = None
                    else:
                        row[config['Mappings']['Phone']] = fake.phone_number()

                if config['Mappings'][
                        'Drivers license'] not in list_of_column_names[0]:
                    pass
                else:
                    if not row[config['Mappings']['Drivers license']]:
                        row[config['Mappings']['Drivers license']] = None
                    else:
                        # declare to use out of the function for fake
                        global firstname, lastname, year, day, month
                        firstname = row[config['Mappings']['First']]
                        lastname = row[config['Mappings']['Last']]
                        if new_birthMonth < 10:
                            # adding 0 in front of one digit month or day
                            month = f"0{str(new_birthMonth)}"
                        else:
                            month = str(new_birthMonth)
                        year = str(new_birthYear)
                        if new_birthDay < 10:
                            day = f"0{str(new_birthDay)}"
                        else:
                            day = str(new_birthDay)

                        state = row[config['Mappings'][
                            'State']]  # assign state for drivers license

                        row[config['Mappings']
                            ['Drivers license']] = random.choice(
                                license_rules[state])(month, firstname,
                                                      lastname, year,
                                                      day)  # apply function

                # LICENSE PLATE
                if config['Mappings'][
                        'License Plate'] not in list_of_column_names[0]:
                    pass
                else:
                    if not row[config['Mappings']['License Plate']]:
                        row[config['Mappings']['License Plate']] = None
                    else:
                        row[config['Mappings']
                            ['License Plate']] = fake.license_plate()

                # CLAIM NUMBER
                if config['Mappings'][
                        'Claim number'] not in list_of_column_names[0]:
                    pass
                else:
                    if not row[config['Mappings']['Claim number']]:
                        row[config['Mappings']['Claim number']] = None
                    else:
                        row[config['Mappings'][
                            'Claim number']] = f"{random.randint(0,9)}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}{random.randint(10000000,99999999)}"

                # VIN
                if config['Mappings']['VIN'] not in list_of_column_names[0]:
                    pass
                else:
                    if not row[config['Mappings']['VIN']]:
                        row[config['Mappings']['VIN']] = None
                    else:
                        row[config['Mappings']['VIN']] = vin_generator(11)

                # TIN
                if config['Mappings']['TIN'] not in list_of_column_names[0]:
                    pass
                else:
                    if not row[config['Mappings']['TIN']]:
                        row[config['Mappings']['TIN']] = None
                    else:
                        row[config['Mappings']['TIN']] = TIN()

                writer.writerow(row)


def isZipCode(number):
    test_string = number
    matched = re.match("^[0-9]{5}$", test_string) or re.match(
        "^[0-9]{10}$", test_string)
    is_match = bool(matched)
    return is_match


def isPhoneNumber(number):
    test_string = number
    matched = re.match("^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$",
                       test_string)
    is_match = bool(matched)
    return is_match


def vin_generator(n):
    return f"{''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))}{random.randint(100000,999999)}"


def TIN():  # like social security
    tin = f"9{str(random.randint(10,99))}-{str(random.randint(10,99))}-{str(random.randint(1000,9999))}"
    return tin


def firstnameemail(
        firstname,
        lastname):  # generstes email with firstname in the beginning
    email = f"{firstname}.{lastname}{random.randint(1,99)}@{faker.domain_name()}"
    return email


def lastnameemail(firstname,
                  lastname):  # generstes email with lastname in the beginning
    email = f"{lastname}.{firstname}{random.randint(1,99)}@{faker.domain_name()}"
    return email


def fLastNameemail(firstname,
                   lastname):  # generstes email with lastname in the beginning
    email = f"{firstname[0]}.{lastname}{random.randint(1,99)}@{faker.domain_name()}"
    return email


def GetValidDob(birthYear):
    todays_date = date.today()
    start_date = datetime.date(todays_date.year, 1, 1)
    fakedate = fake.date_between_dates(date_start=start_date,
                                       date_end=todays_date)
    dob = datetime.date(birthYear, fakedate.month, fakedate.day)
    birthday = dob.strftime('%m/%d/%Y')
    return birthday


def rule1(*args):  # 7 digits #this format
    license_number = str(random.randint(1000000, 9999999))
    return license_number


def rule2(*args):  # 9 digits #this format
    license_number = str(random.randint(100000000, 999999999))
    return license_number


def rule3(*args):  # 1 Letter followed by 8 numbers #this format
    license_number = random.choice(string.ascii_uppercase) + str(
        random.randint(10000000, 99999999))
    return license_number


def rule4(*args):  # 9 digits beginning with 9 #this format
    license_number = str(random.randint(900000000, 999999999))
    return license_number


def rule5(*args):  # 1 Letter followed by 7 numbers #this format
    license_number = random.choice(string.ascii_uppercase) + str(
        random.randint(1000000, 9999999))
    return license_number


def rule6(*args):  # ##-###-#### #this format
    license_number = f"{str(random.randint(10,99))}-{str(random.randint(100,999))}-{str(random.randint(1000,9999))}"
    return license_number


def rule7(*args):  # 1 Letter followed by 12numbers #this format
    license_number = random.choice(string.ascii_uppercase) + str(
        random.randint(100000000000, 999999999999))
    return license_number


def rule8(*args):  # L##-###-##-###-# #this format
    license_number = f"{random.choice(string.ascii_uppercase)}{str(random.randint(10,99))}-{str(random.randint(100,999))}-{str(random.randint(10,99))}-{str(random.randint(100,999))}-{str(random.randint(1,9))}"
    return license_number


def rule9(*args):  # 2L6N1L #this format
    license_number = f"{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}{str(random.randint(100000,999999))}{random.choice(string.ascii_uppercase)}"
    return license_number


def rule10(*args):  # L###-####-#### #this format
    license_number = f"{random.choice(string.ascii_uppercase)}{str(random.randint(100,999))}-{str(random.randint(1000,9999))}-{str(random.randint(1000,9999))}"
    return license_number


def rule11(*args):  # -##-####  #this format
    license_number = f"{str(random.randint(1000,9999))}-{str(random.randint(10,99))}-{str(random.randint(1000,9999))}"
    return license_number


def rule12(*args):  # 3N2L4N
    license_number = f"{str(random.randint(100,999))}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}{str(random.randint(1000,9999))}"
    return license_number


def rule13(*args):  # L##-###-####
    license_number = f"{random.choice(string.ascii_uppercase)}{str(random.randint(10,99))}-{str(random.randint(10,99))}-{str(random.randint(1000,9999))}"
    return license_number


def rule14(*args):  # L##-###-###
    license_number = f"{random.choice(string.ascii_uppercase)}{str(random.randint(10,99))}-{str(random.randint(100,999))}-{str(random.randint(100,999))}"
    return license_number


def rule15(*args):  # L-###-###-###-###
    license_number = f"{random.choice(string.ascii_uppercase)}-{str(random.randint(100,999))}-{str(random.randint(100,999))}-{str(random.randint(100,999))}-{str(random.randint(100,999))}"
    return license_number


def rule16(*args):  # 1 Letter followed by 9 numbers
    license_number = random.choice(string.ascii_uppercase) + str(
        random.randint(100000000, 999999999))
    return license_number


def rule17(*args):
    license_number = f"{str(random.randint(10,99))} {str(random.randint(100,999))} {str(random.randint(100,999))}"
    return license_number


# rule18 reqquires the license issued number


def rule19(*args):
    license_number = str(random.randint(10000000, 99999999))
    return license_number


def rule20(*args):  # 7 numbers followed by 1 Letter
    license_number = str(random.randint(1000000, 9999999)) + random.choice(
        string.ascii_uppercase)
    return license_number


def rule21(*args):  # 3L ** 2L3N1l1N
    license_number = f"{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}**{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}{str(random.randint(100,999))}{random.choice(string.ascii_uppercase)}{str(random.randint(1,9))}"
    return license_number


def rule22(*args):  # 1 Letter followed by 6 numbers
    license_number = random.choice(string.ascii_uppercase) + str(
        random.randint(100000, 999999))
    return license_number


def rule23(*args):  # L###-####-####-##
    license_number = f"{random.choice(string.ascii_uppercase)}{str(random.randint(100,999))}-{str(random.randint(1000,9999))}-{str(random.randint(1000,9999))}-{str(random.randint(10,99))}"
    return license_number


def rule24(*args):  # ######-###
    license_number = f"{str(random.randint(100000,999999))}-{str(random.randint(100,999))}"
    return license_number


def rule25(*args):  # social security
    license_number = f"{str(random.randint(100,999))}-{str(random.randint(10,99))}-{str(random.randint(1000,9999))}"
    return license_number


def rule26(*args):
    birthmonth = month
    firstandlastoflastname = f"{lastname[0].capitalize()}{lastname[-1].capitalize()}{firstname[0].capitalize()}"
    birthyear = year[-2:]
    birthday = day

    license_number = f"{birthmonth}{firstandlastoflastname}{birthyear}{birthday}{random.randint(0,9)}"
    return license_number


def rule27(*args):  # L####-#####-#####
    license_number = f"{random.choice(string.ascii_uppercase)}{str(random.randint(1000,9999))}-{str(random.randint(10000,99999))}-{str(random.randint(10000,99999))}"
    return license_number


def rule28(*args):  # ### ### ###
    license_number = f"{str(random.randint(100,999))} {str(random.randint(100,999))} {str(random.randint(100,999))}"
    return license_number


def rule29(*args):  # 12 numbers
    license_number = str(random.randint(100000000000, 999999999999))
    return license_number


def rule30(*args):  # North Dakota
    if len(lastname) <= 2:
        first3last = f"{lastname[0].capitalize()}{lastname[1].capitalize()}X"
    else:
        first3last = f"{lastname[0].capitalize()}{lastname[1].capitalize()}{lastname[2].capitalize()}"
    birthyear = year[-2:]
    license_number = f"{first3last}{birthyear}{random.randint(1000,9999)}"
    return license_number


def rule31(*args):  # 2L6N
    license_number = f"{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}{str(random.randint(100000,999999))}"
    return license_number


def rule32(*args):  # 2L9N
    license_number = f"{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}{str(random.randint(100000000,999999999))}"
    return license_number


def rule33(*args):  # L ### ### ### ###
    license_number = f"{random.choice(string.ascii_uppercase)} {str(random.randint(100,999))} {str(random.randint(100,999))} {str(random.randint(100,999))} {str(random.randint(100,999))}"
    return license_number


def rule34(*args):
    birthmonth = month
    birthyear = year[-2:]
    birthday = day

    license_number = f"{birthmonth}{random.randint(100,999)}{birthyear}41{birthday}"
    return license_number


def rule35(*args):  # 10 digits #this format
    license_number = str(random.randint(1000000000, 9999999999))
    return license_number


# rule dictionary to be applied in the program

license_rules = {
    "AL": [rule1],
    "AK": [rule1],
    "DE": [rule1],
    "ME": [rule1],
    "OR": [rule1],
    "DC": [rule1],
    "WV": [rule1, rule22],
    "RI": [rule1],
    "AZ": [rule2, rule3],
    "CT": [rule2],
    "GA": [rule2],
    "IA": [rule2, rule12],
    "LA": [rule2],
    "MT": [rule2, rule34],
    "NM": [rule2],
    "SC": [rule2],
    "UT": [rule2],
    "TN": [rule2, rule19],
    "HI": [rule3],
    "NE": [rule3],
    "VA": [rule3, rule13],
    "AR": [rule4],
    "CA": [rule5],
    "CO": [rule6],
    "FL": [rule7, rule8],
    "ID": [rule9],
    "IL": [rule10],
    "IN": [rule11],
    "KS": [rule13],
    "KY": [rule14],
    "MD": [rule15],
    "MA": [rule16],
    "MO": [rule16],
    "OK": [rule16],
    "PA": [rule17],
    "SD": [rule19],
    "TX": [rule19],
    "VT": [rule19, rule20],
    "WA": [rule21],
    "WI": [rule23],
    "WY": [rule24],
    "MS": [rule25],
    "NH": [rule26],
    "NJ": [rule27],
    "NY": [rule28],
    "NC": [rule29],
    "ND": [rule30],
    "OH": [rule31],
    "MI": [rule7, rule33],
    "MN": [rule7],
    "NV": [rule35]
}
# choose the source file

sourcefile = input("Input filename: ")
with open(sourcefile) as csv_file:

    # creating an object of csv reader
    # with the delimiter as ,
    csv_reader = csv.reader(csv_file, delimiter=',')

    # list to store the names of columns
    list_of_column_names = []

    # loop to iterate through the rows of csv
    for row in csv_reader:

        # adding the first row
        list_of_column_names.append(row)

        # breaking the loop after the
        # first iteration itself
        break

# printing the result
print("List of column names : ", list_of_column_names[0])
list_of_possible_phone = [
    "Phone", "number", "contact", "phone", "Phone number"
]
anonymize(sourcefile)
with open(sourcefile, 'rb') as f:
    reader = cs.DictReader(f)
    flag = False
    for row in reader:  # loop through each rows
        if flag:
            break
        for phoneIndex in range(len(list_of_column_names[0])
                                ):  # loop through each items in the row
            if isPhoneNumber(
                    str(row[list_of_column_names[0][phoneIndex]])
            ) == True and list_of_column_names[0][
                    phoneIndex] in list_of_possible_phone:  # if the item matches phonenumber test and its column title is phone number or number or phone or etc
                flag = True
                # print(row[list_of_column_names[0][i]])  #print that item
                break
        for zipIndex in range(len(list_of_column_names[0])
                              ):  # loop through each items in the row
            if isZipCode(
                    str(row[list_of_column_names[0][zipIndex]])
            ) == True:  # if the item matches phonenumber test and its column title is phone number or number or phone or etc
                flag = True
                # print(row[list_of_column_names[0][zipIndex]])  #print that item
                break

print(f"Column {zipIndex + 1} look like its for zip codes")

print(f"Column {phoneIndex + 1} look like its for phone numbers")
# record end time
end = time.time()

# print the difference between start
# and end time in milli. secs
print("Execution time :", (end - start), "s.")
