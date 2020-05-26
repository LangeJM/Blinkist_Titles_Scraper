'''Get a list of all available book reviews on blinkist.com and convert to csv file
'''
import msvcrt
import csv
import time
import tkinter as tk
from tkinter import filedialog

from selenium import webdriver


def get_book_category_links():
    '''Gets list of category urls, either from previously created list or by scraping ( with manual login effort though).
    '''
    print('The available list of category urls from blinklist.com is dated June, 2020.\nPress any other key to continue.')
    msvcrt.getch()
    category_links = ['https://www.blinkist.com/en/nc/categories/entrepreneurship-and-small-business-en/books', 'https://www.blinkist.com/en/nc/categories/politics-and-society-en/books', 'https://www.blinkist.com/en/nc/categories/marketing-and-sales-en/books', 'https://www.blinkist.com/en/nc/categories/science-en/books', 'https://www.blinkist.com/en/nc/categories/health-and-fitness-en/books', 'https://www.blinkist.com/en/nc/categories/personal-growth-and-self-improvement-en/books', 'https://www.blinkist.com/en/nc/categories/economics-en/books', 'https://www.blinkist.com/en/nc/categories/biography-and-history-en/books', 'https://www.blinkist.com/en/nc/categories/communication-and-social-skills-en/books', 'https://www.blinkist.com/en/nc/categories/corporate-culture-en/books', 'https://www.blinkist.com/en/nc/categories/management-and-leadership-en/books', 'https://www.blinkist.com/en/nc/categories/motivation-and-inspiration-en/books', 'https://www.blinkist.com/en/nc/categories/money-and-investments-en/books', 'https://www.blinkist.com/en/nc/categories/psychology-en/books', 'https://www.blinkist.com/en/nc/categories/productivity-and-time-management-en/books', 'https://www.blinkist.com/en/nc/categories/relationships-and-parenting-en/books', 'https://www.blinkist.com/en/nc/categories/technology-and-the-future-en/books', 'https://www.blinkist.com/en/nc/categories/mindfulness-and-happiness-en/books', 'https://www.blinkist.com/en/nc/categories/parenting-en/books', 'https://www.blinkist.com/en/nc/categories/nature-and-environment-en/books', 'https://www.blinkist.com/en/nc/categories/creativity-en/books', 'https://www.blinkist.com/en/nc/categories/society-and-culture-en/books', 'https://www.blinkist.com/en/nc/categories/career-and-success-en/books', 'https://www.blinkist.com/en/nc/categories/religion-and-spirituality-en/books', 'https://www.blinkist.com/en/nc/categories/education-en/books', 'https://www.blinkist.com/en/nc/categories/biography-and-memoir-en/books', 'https://www.blinkist.com/en/nc/categories/philosophy-en/books']
    num_cags = len(category_links)
    print('There are ' + str(num_cags) + ' categories on blinkist.com. PLease note, books can be listed for several categories.')
    return category_links, num_cags

def set_geckodriver_path():
    '''Point to Chrome webdriver local path'''
    print('\nPlease select the local geckodriver.exe\n')
    time.sleep(1.5)
    root = tk.Tk()
    root.withdraw()
    geckodriver_path = filedialog.askopenfilename()
    if geckodriver_path == '':
        geckodriver_path = 'geckodriver.exe'
    return geckodriver_path

def setup_geckodriver(): #normally with argument 'chrome_webdriver_path' but seems webdriver doesn't run in mopdule-function so transferred to main.py
    '''Setup of Chrome webdriver'''
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
    return firefox_profile


def get_all_book_info(category_links, num_cags, driver):
    '''Get info for all books
    '''
    category_names = ['Category']
    book_urls = ['Book_Url']
    read_urls = ['Read_Url']
    book_titles = ['Title']
    book_authors = ['Author']


    for cag in range(num_cags):
        driver.get(category_links[cag])

        book_urls_raw = driver.find_elements_by_class_name('letter-book-list__item')
        book_titles_raw = driver.find_elements_by_class_name('letter-book-list__item__title')
        book_authors_raw = driver.find_elements_by_class_name('letter-book-list__item__author')
        category_name = category_links[cag].split('/')[-2]


        #create lists with n number of category names, book urls, book titles, book authors
        for index in range(len(book_urls_raw)):
            category_names.append(category_name)

        for elem in book_urls_raw:
            book_urls.append(elem.get_attribute("href"))

        for elem in book_titles_raw:
            book_titles.append(elem.text)

        # Need to start at 4th index, since every element.text starts with 'by '
        for elem in book_authors_raw:
            book_authors.append(elem.text[3:])

        print('\n' + str(index) + ' new books added in category: ' + str(category_name) + '\nCategories: ' + str(len(category_names)) + '\nUrls: ' + str(len(book_urls)) + '\nBook titles: ' + str(len(book_titles)) + '\nBook authors: ' + str(len(book_authors)))

    # Need to start with second index since books_url list already start with header which is not url
    for elem in book_urls[1:]:
        read_urls.append(elem.replace('en/books', 'en/nc/reader'))

    return category_names, book_urls, read_urls, book_titles, book_authors

def create_csv(book_authors, book_titles, book_urls, read_urls, category_names):
    '''Create and export csv of book info
    '''
    columns = zip(book_authors, book_titles, book_urls, read_urls, category_names)

    with open('blinkist_all_books.csv', "w", newline='', encoding="utf-8") as output:
        writer = csv.writer(output)
        for column in columns:
            writer.writerow(column)

    print('\nCsv file saved to current work directory.')

def all_books_to_csv():
    '''Actually run code
    '''
    # Get geckodriver path from user dialogue
    geckodriver_path = set_geckodriver_path()

    # Set up Firefox profile to run private session
    firefox_profile = setup_geckodriver()

    # Start automated Firefox session on right screen (if multi screen setup) and maxed window
    driver = webdriver.Firefox(firefox_profile=firefox_profile, executable_path=geckodriver_path)
    driver.set_window_position(2000, 0)
    driver.maximize_window()

    # Actually scrape information
    category_links, num_cags = get_book_category_links()
    category_names, book_urls, read_urls, book_titles, book_authors = get_all_book_info(category_links, num_cags, driver)
    driver.quit()

    #Create csv file with scraped information
    create_csv(book_authors, book_titles, book_urls, read_urls, category_names)

    return driver

if __name__ == "__main__":
    all_books_to_csv()
