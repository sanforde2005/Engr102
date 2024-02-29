import csv


class Participant:
    def __init__(self, age, industry, salary, currency, country, experience, education):
        # self.x = x
        self.age = age
        self.industry = industry
        self.salary = salary
        self.currency = currency
        self.country = country
        self.experience = experience
        self.education = education

# TODO: Create a AverageSalary class
    # Including:
    # key - this is the group key (i.e. "Accounting, Banking & Finance" from industry)
    # average - this is the average salary
    # participant_count - this is how many total participants fit into this group
        
class AverageSalary:
    def __init__(self, key, average, participant_count):

        self.key = key
        self.average = average
        self.participant_count = participant_count


def main():

    rows = load_csv_file("survey.csv")
    participants = create_participants(rows)

    print("Answer #1:", len(participants))

    industry_groups = group_by_attribute(participants, "industry")

    average_salaries_by_industry = get_average_salary(industry_groups)

    filteredSalaries = []
    for obj in average_salaries_by_industry:
        if obj.participant_count >=10:
            filteredSalaries.append(obj)

    # sorts by 'average' attribute of object in list!
    sortedSalaries = sorted(filteredSalaries, key=lambda x: x.average, reverse=True)

    topFiveIndustries = []

    for item in sortedSalaries[:5]:
        topFiveIndustries.append(item.key)

    print(topFiveIndustries)


    age_groups = group_by_attribute(participants, "age")

    average_salaries_by_age = get_average_salary(age_groups)
    
    for group in average_salaries_by_age:
        print("answer 3:", group.key, group.average)

    education_groups = group_by_attribute(participants, "education")
    average_salaries_by_edu = get_average_salary(education_groups)

    for group in average_salaries_by_edu:
        print("answer 4:", group.key, group.average)


    experience_groups = group_by_attribute(participants, "experience")
    average_salaries_by_exp = get_average_salary(experience_groups)

    for group in average_salaries_by_exp:
        print(group.key, group.average)

    #topFive = get_top_five(average_salaries_by_industry)
    #print("answer 2 =", topFive)
    
    # TODO: print top 5 industries by salary. Only include industries with at least 10 participants

    # TODO: Use existing logic to solve questions 3,4,5

    return

#def get_top_five(list):
    
    with10 = []
    salaries = []
    for obj in list:
        if obj.participant_count >=10:
            with10.append(obj)
            salaries.append(obj.average)

    salaries.sort()
    salaries.reverse()

    for i in range(len(salaries)):
        for item in with10:
            if item.average == salaries[i]:
                salaries[i] = item.key

            
    return salaries[:5]

        


def get_average_salary(groups_list):
    '''
        get the average salary from a groupped list

        params:
            groups_list: dict<String, List<Participant>>

        return:
            List<tuple<Str, int, int>> - Returns a list of tuples which include the key as a string, the average as an int, and the amount of participants as an int.
            TODO: rather than returning a tuple, create an AverageSalary object, and process the information that way.
    
    '''
    average_salaries = []
    for key, group in groups_list.items():
        avg = int(sum([x.salary for x in group]) / len(group))
        # TODO: With the AverageSalaries class we created, append in instance of AverageSalaries instead of just key, avg, len(group)
        average_salaries.append(AverageSalary(key, avg, len(group)))

    return average_salaries


def group_by_attribute(objects, property):
    '''
        params:
            objects: List<Participant> - a list of the participant objects
            property: whichever object property we want to group by

        return:
            dict<String, List<Participant>> - a dictionary, using the value of the property as the key, and the list of participants which include that value as the value.

            value is key


    '''

    # The logic for grouping has been simplified greatly for both faster execution and easier understanding
    
    groups = {}
    
    # create a dictionary using the property
    for obj in objects:
        value = getattr(obj, property)
        if value in groups:
            groups[value].append(obj)
        else:
            #makes a new key and adds the obj as the first value inside
            groups[value] = [obj]

    return groups




def create_participants(rows):
    '''
    parse the rows, extracting the required content for the data analysis

    params:
        rows: Lists<List<Str>> - Each entry is a list of strings, the entries are contained in a larger list.

    return:
        List<Participant> - Returns a list of Participant objects
    '''
    # Age, Industry, Salary, Currency, Country, Years of Experience Overall, Highest level of Education

    participants = []

    for row in rows[1:]:
        age = row[1]
        industry = row[2]
        salary = int(row[5].replace(",",""))
        currency = row[7]
        country = row[10]
        experience = row[13]
        education = row[15]
        # only add if currency == 'USD'
        if currency == "USD":
            participants.append(Participant(age, industry, salary, currency, country, experience, education))

    return participants



def load_csv_file(filename):
    '''
    loads contents of a csv file and returns the contents as a list of the row, each row representing an entry.

    params: 
        filename: Str - filename with path to the csv file which will be read

    returns:
        rows: List<List<Str>> - A list of the rows, each row is a list of strings from the csv file

        list inside is each piece of data in row, list outside of string is list of rows
    '''
    rows = []
    with open(filename, "r", encoding='iso-8859-1') as f:
        reader_obj = csv.reader(f)

        for row in reader_obj:
            rows.append(row)

    return rows



if __name__ == "__main__":
    main()