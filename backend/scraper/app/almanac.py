import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException

dirname = r'%s' % os.path.dirname(os.path.realpath(__file__))
csv_name = dirname + '/contacts.csv'

def get_driverpath():
    dirname = r'%s' % os.path.dirname(os.path.realpath(__file__))
    print("directory name", dirname)
    driverpath = dirname + r"/chromedriver_97"
    print("Running Selenium from: " + driverpath)
    return driverpath

def sign_in(driverpath):
    options = webdriver.ChromeOptions()
    global driver
    driver = webdriver.Chrome(options=options, executable_path=driverpath)
    driver.get('https://directory.apps.upenn.edu/directory/jsp/fast2.do')
    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "/html/body/table[2]/tbody/tr/td/table[2]/tbody/tr[3]/td/table/tbody/tr/td[1]/form/table/tbody/tr[9]/td/a[1]/span")))
    except TimeoutException:
        print('Login failed.')

def create_csv(dirname):
    global csv_name
    csv_name = dirname + '/contacts.csv'
    print('Writing contacts to: ' + csv_name)
    with open(csv_name, mode='w') as contacts:
        writer = csv.writer(contacts, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        entry = ["Name", "Given Name", "Additional Name", "Family Name", "Email", "Major", "School"]
        writer.writerow(entry)
 
def iterate_dir(orgs, affil):
    # for first_let in range(105, 106):
    #     for second_let in range(113, 123):
    #         for org in orgs:
    #             driver.get('https://directory.apps.upenn.edu/directory/jsp/fast2.do')
    #             org_field = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/table[2]/tbody/tr[3]/td/table/tbody/tr/td[1]/form/table/tbody/tr[7]/td[2]/input')
    #             affil_field = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/table[2]/tbody/tr[3]/td/table/tbody/tr/td[1]/form/table/tbody/tr[6]/td[2]/select')
    #             search_field = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/table[2]/tbody/tr[3]/td/table/tbody/tr/td[1]/form/table/tbody/tr[3]/td[2]/input')
    #             search_button = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/table[2]/tbody/tr[3]/td/table/tbody/tr/td[1]/form/table/tbody/tr[9]/td/a[1]/span')
    #             org_field.clear()
    #             org_field.send_keys(org)
    #             search_field.clear()
    #             search_field.send_keys(chr(first_let) + chr(second_let))
    #             affil_field.send_keys(affil)
    #             while (True):
    #                 try :
    #                     search_button.click()
    #                     break
    #                 except ElementClickInterceptedException:
    #                     time.sleep(5)
                        
    #             try:
    #                 page_count = get_max_pages()
    #                 print(chr(first_let) + chr(second_let), org, page_count)
    #                 time.sleep(1)
    #                 scrape_page()
    #                 if page_count > 1:
    #                     for i in range(1, page_count):
    #                         next_button = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr/td/div[2]/a[last()]/span')
    #                         next_button.click()
    #                         time.sleep(1)
    #                         scrape_page()
    #             except Exception:
    #                 print("Some exception")
    #                 raise

    for first_let in range(122, 123):
        for second_let in range(121, 123):
            for org in orgs:
                driver.get('https://directory.apps.upenn.edu/directory/jsp/fast2.do')
                org_field = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/table[2]/tbody/tr[3]/td/table/tbody/tr/td[1]/form/table/tbody/tr[7]/td[2]/input')
                affil_field = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/table[2]/tbody/tr[3]/td/table/tbody/tr/td[1]/form/table/tbody/tr[6]/td[2]/select')
                search_field = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/table[2]/tbody/tr[3]/td/table/tbody/tr/td[1]/form/table/tbody/tr[3]/td[2]/input')
                search_button = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/table[2]/tbody/tr[3]/td/table/tbody/tr/td[1]/form/table/tbody/tr[9]/td/a[1]/span')
                org_field.clear()
                org_field.send_keys(org)
                search_field.clear()
                search_field.send_keys(chr(first_let) + chr(second_let))
                affil_field.send_keys(affil)
                while (True):
                    try :
                        search_button.click()
                        break
                    except ElementClickInterceptedException:
                        time.sleep(5)
                        
                try:
                    page_count = get_max_pages()
                    print(chr(first_let) + chr(second_let), org, page_count)
                    time.sleep(1)
                    scrape_page()
                    if page_count > 1:
                        for i in range(1, page_count):
                            next_button = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr/td/div[2]/a[last()]/span')
                            while (True):
                                try :
                                    next_button.click()
                                    break
                                except ElementClickInterceptedException:
                                    time.sleep(5)
                            scrape_page()
                except Exception:
                    print("Some exception")
                    raise

def scrape_page():
    print("scraping...")
    name_path = '/html/body/table[2]/tbody/tr/td/form/table[1]/tbody/tr/td/table/tbody/tr[{}]/td[1]/table/tbody/tr/td/a/span'
    email_path = '/html/body/table[2]/tbody/tr/td/form/table[1]/tbody/tr/td/table/tbody/tr[{}]/td[3]/table/tbody/tr[2]/td/a'
    major_path = '/html/body/table[2]/tbody/tr/td/form/table[1]/tbody/tr/td/table/tbody/tr[{}]/td[2]/table/tbody/tr[1]/td'
    school_path = '/html/body/table[2]/tbody/tr/td/form/table[1]/tbody/tr/td/table/tbody/tr[{}]/td[2]/table/tbody/tr[2]/td'

    name = None
    email = None
    major = None
    school = None
    for row in range(2, 22):
        try:
            name = driver.find_element(By.XPATH, name_path.format(row))
            email = driver.find_element(By.XPATH, email_path.format(row))
            major = driver.find_element(By.XPATH, major_path.format(row))
            school = driver.find_element(By.XPATH, school_path.format(row))
        except Exception:
            # needs to continuing trying, because some students don't have phone numbers, so their email is at tr[1]
            email_path = '/html/body/table[2]/tbody/tr/td/form/table[1]/tbody/tr/td/table/tbody/tr[{}]/td[3]/table/tbody/tr[1]/td/a'
            try :
                name = driver.find_element(By.XPATH, name_path.format(row))
                email = driver.find_element(By.XPATH, email_path.format(row))
                major = driver.find_element(By.XPATH, major_path.format(row))
                school = driver.find_element(By.XPATH, school_path.format(row))
                email_path = '/html/body/table[2]/tbody/tr/td/form/table[1]/tbody/tr/td/table/tbody/tr[{}]/td[3]/table/tbody/tr[2]/td/a'
            except Exception:
                email_path = '/html/body/table[2]/tbody/tr/td/form/table[1]/tbody/tr/td/table/tbody/tr[{}]/td[3]/table/tbody/tr[2]/td/a'
                continue
    
        name = name.text
        email = email.text
        major = major.text
        school = school.text
        make_entry(name, email, major, school)


def get_max_pages():
    next_path = '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr/td/div[2]/a[{}]/span'
    max = 1
    for i in range(2, 30):
        try:
            div = driver.find_element(By.XPATH, next_path.format(i))
            if (div.text.isnumeric()) :
                max = int(div.text)
        except NoSuchElementException:
            break
    return max
        
def make_entry(name, email, major, school):
    lastname = name[0 : name.index(',')]
    firstname = name[name.index(',') + 2 : len(name)]
    lastname = format_name(lastname)
    firstname = format_name(firstname)
    major = parse_for_major(major)
    school = "".join(school.lstrip().rstrip().lower())
    try:
        middlename = firstname[firstname.index(' ') + 1 : len(firstname)]
        firstname = firstname[0 : firstname.index(' ')]
    except Exception:
        middlename = ""
    if len(middlename) == 1:
        middlename = middlename + '.'
    name = firstname + " " + lastname
    entry = {'name': name, 'firstname': firstname, 'middlename': middlename, 'lastname': lastname, 'email': email, 'major': major, 'school': school}
    write_entry(entry)

def parse_for_major(major):
    items = major.split('-')
    major = "".join(items[-1].lstrip().rstrip().lower())
    return major

def format_name(name):
    try:
        gap = name.index(' ')
    except Exception:
        name = name[0 : 1] + name[1 : len(name)].lower()
        return name
    else:
        left = name[0 : gap]
        left = left[0 : 1] + left[1 : len(left)].lower()
        right = name[gap + 1 : len(name)]
        return left + " " + format_name(right)

def write_entry(entry):
    with open(csv_name, mode='a') as contacts:
        writer = csv.writer(contacts, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        entry = [entry['name'], entry['firstname'], entry['middlename'], entry['lastname'], entry['email'], entry['major'], entry['school']]
        writer.writerow(entry)

def get_orgs_input():
    organizations = input("Organization(s) semicolon-separated: ")
    orgs = []
    i = 0
    while i <= len(organizations):
        try:
            gap = organizations.index(';', i)
        except Exception:
            org = str(organizations[i : len(organizations)])
            orgs.append(org)
            break
        else:
            org = str(organizations[i : gap])
            orgs.append(org)
            i = gap 
        finally:
            i += 1
    return orgs
    
def get_affil_input():
    affiliation = input("Affiliation: ")
    return str(affiliation)

def upload_contacts():
    driver.get('https://contacts.google.com')
    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/c-wiz/div[2]/div[6]/div[2]/div/div/div[3]/button[2]/span[2]')))
    except TimeoutException:
        print('Login failed.')
    else:
        import_button = driver.find_element(By.XPATH, '/html/body/div[7]/c-wiz/div[2]/div[6]/div[2]/div/div/div[3]/button[2]/span[2]')
        import_button.click()
        time.sleep(1)
        select_button = driver.find_element(By.XPATH, '/html/body/div[7]/div[4]/div/div[2]/span/div/label/div')
        select_button.click()

def main():
    # orgs = get_orgs_input()
    # affil = get_affil_input()
    orgs = ["college of arts & sciences", "engineering", "nursing", "wharton"]
    affil = "Student"
    sign_in(get_driverpath())
    # create_csv(dirname)
    iterate_dir(orgs, affil)
    upload_contacts()

if __name__ == '__main__':
    main()
