from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd



def get_jobs(keyword, num_jobs, verbose,slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.EdgeOptions()
    
    #Stop edge personalised ads popup
    prefs = {
    'user_experience_metrics': {
        'personalization_data_consent_enabled': True
    }
    }
    options.add_experimental_option('prefs', prefs)

    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where edge driver is in your home folder.
    driver = webdriver.Edge(options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element(by='class name',value='selected').click()
            # driver.find_element_by_class_name("selected").click()
            
        except ElementClickInterceptedException:
            pass

        time.sleep(.1)

        try:
            driver.find_element(by='class name',value='e1jbctw80').click()
            
            # driver.find_element_by_class_name("ModalStyle__xBtn___29PT9").click()  #clicking to the X.
        except NoSuchElementException:
            pass
           
        time.sleep(.1)
        
        try:
            driver.find_element(by='id',value='onetrust-accept-btn-handler').click()
            
            # driver.find_element_by_class_name("ModalStyle__xBtn___29PT9").click()  #clicking to the X.
        except NoSuchElementException:
            pass
        
        
        #Going through each job in this page
        job_buttons = driver.find_elements(by='class name',value ="react-job-listing")
        # job_buttons = driver.find_elements_by_class_name("jl")  #jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break
            
            # # Click the job button after scrolling to it
            # job_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "react-job-listing")))
            # actions = ActionChains(driver)
            # actions.move_to_element(job_button).perform()
            
            job_button.click()  #You might 
            time.sleep(3)
            collected_successfully = False
            print("x1 out worked")
            print(len(job_buttons))
            while not collected_successfully:
                try:
                    print("x2 out worked")
                    # company_name = driver.find_element(by='class name',value='css-87uc0g.e1tk4kwz1').text
                    company_name = driver.find_element(by='css selector',value='[data-test="employerName"]').text
                    # company_name = driver.find_element(by='xpath',value='.//div[@class="employerName"]').text
                    print("x3 out worked")
                    location = driver.find_element(by='css selector',value='[data-test="location"]').text
                    print("x4 out worked")
                    # job_title = driver.find_element(by='css selector',value='[data-test="jobTitle"]').text
                    # job_title = driver.find_element(by='xpath', value='//*[@data-test="jobTitle"]').text
                    job_title = driver.find_element(by='class name', value='css-1vg6q84.e1tk4kwz4').text
                    print("x5 out worked")
                    print(job_title)
                    job_description = driver.find_element(by='class name',value="jobDescriptionContent.desc").text
                    collected_successfully = True
                    print("x6 out worked")
                # except:
                except Exception as e:
                    print(f"Error: {str(e)}")
                    time.sleep(5)

            try:
                print("x7 out worked")
                salary_estimate = driver.find_element(by='class name',value='css-1bluz6i.e2u4hf13').text
                # salary_estimate = driver.find_element(by='xpath',value='.//span[@class="gray small salary"]').text
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
            
            try:
                rating = driver.find_element(by='class name',value='mr-sm.css-ey2fjr.e1pr2f4f2').text
                # rating = driver.find_element(by='xpath',value='.//span[@class="rating"]').text
                print("x8 out worked")
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                # driver.find_element(by='xpath',value='.//div[@class="tab" and @data-tab-type="overview"]').click()


                try:
                    size = driver.find_element(by='xpath', value='//span[contains(@class, "css-1taruhi") and text()="Size"]/following-sibling::span[@class="css-i9gxme e1pvx6aw2"]').text
                    # size = driver.find_element(by='class name',value='css-i9gxme.e1pvx6aw2').text
                    print("x9 out worked")
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element(by='xpath', value='//span[contains(@class, "css-1taruhi") and text()="Founded"]/following-sibling::span[@class="css-i9gxme e1pvx6aw2"]').text
                    # founded = driver.find_element(by='class name',value='css-i9gxme.e1pvx6aw2').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element(by='xpath', value='//span[contains(@class, "css-1taruhi") and text()="Type"]/following-sibling::span[@class="css-i9gxme e1pvx6aw2"]').text
                    # type_of_ownership = driver.find_element(by='class name',value='').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element(by='xpath', value='//span[contains(@class, "css-1taruhi") and text()="Industry"]/following-sibling::span[@class="css-i9gxme e1pvx6aw2"]').text
                    # industry = driver.find_element(by='class name',value='.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element(by='xpath', value='//span[contains(@class, "css-1taruhi") and text()="Sector"]/following-sibling::span[@class="css-i9gxme e1pvx6aw2"]').text
                    # sector = driver.find_element(by='class name',value='.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element(by='xpath', value='//span[contains(@class, "css-1taruhi") and text()="Revenue"]/following-sibling::span[@class="css-i9gxme e1pvx6aw2"]').text
                    # revenue = driver.find_element(by='class name',value='.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                    print("x10 out worked")
                except NoSuchElementException:
                    revenue = -1

           

            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                

                
            if verbose:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue})
            #add job to jobs
            print("x11 out worked")
    #Clicking on the "next page" button
        try:
            driver.find_element(by='class name',value='navIcon.e13qs2070.job-search-4iku5v.e7xsrz90').click()

            # # Find the element (you can adjust the selector)
            # next_page_button = driver.find_element(By.CLASS_NAME, "navIcon.e13qs2070.job-search-4iku5v.e7xsrz90")
            # # Scroll to the element
            # driver.execute_script("arguments[0].scrollIntoView();", next_page_button)
            # # Click the element
            # next_page_button.click()

            print("x12 out worked")
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break       

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.