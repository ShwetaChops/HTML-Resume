"""
HW 5 - UNIT TESTS
"""
#Import module
import unittest

#Import the program to be tested
from make_website import *

class Test_Make_Website(unittest.TestCase):

#-----------------------------------------------------------------------------------------------#
    ### TESTS FOR PARSING FUNCTIONS ###

    def test_read_file(self):
        #Test if files are being read properly with tabs, empty lines, letters, numbers
        self.assertEqual(["Shweta Chopra\n", "ABC"], read_file("test3.txt"))
        self.assertEqual(["---\n","\n", "\t90210"], read_file("test2.txt"))
        
    
    def test_clean_text(self):
        #Create list of strings for testing
        list = [" List ", "of\n", "\tStrings\t", " \nto TEST"]
        #Test to check if spaces/tabs/new line characters before and after are removed
        self.assertEqual(["List", "of", "Strings", "to TEST"], clean_text(list))
        

    def test_detect_name(self):
        #Create text from which to detect name
        text = ["Full Name", "Age: 7", "Address: NYC, NY"]
        text_1 = ["@Full Name", "Age: 7", "Address: NYC, NY"]
        text_2 = ["Projects: 123", "Email"]
        #Ensure Full Name is detected
        self.assertTrue("Full Name" is detect_name(text))
        #Ensure error raised if Full Name does not begin with capital letter
        self.assertRaises(RuntimeError, detect_name, text_1)
        #Ensure error raised if no name exists
        self.assertRaises(RuntimeError, detect_name, text_2)
        
    def test_detect_email(self):
        #Create text cases from which to detect email
        text = ["Full Name", "Age: 7", "cit@abc.com"] #.com
        text_1 = ["Full Name", "Age: 7", "cit@abc.edu"] #.edu
        text_2 = ["Full Name", "Age: 7", "cit590@abc.com"] #digits in email
        text_3 = ["Full Name", "Age: 7", "Address: NYC, NY"] #no email
        text_4 = ["Full Name", "Age: 7", "cit@.com"] #no gap b/w @ and .
        text_5 = ["Full Name", "Age: 7", "cit@ABC.com"] #capital leter after @
        text_6 = ["Full Name", "Age: 7", "cit_class@abc.com"] #special character in username
        text_7 = ["Full Name", "Age: 7", "cit@abc9.com"] #digit after @
        text_8 = ["Full Name", "Age: 7", "cit@ab c.com"] #space in email

        
        #Ensure correct emails extracted where function rules are met
        self.assertEqual("cit@abc.com", detect_email(text))
        self.assertEqual("cit@abc.edu", detect_email(text_1))
        self.assertEqual("", detect_email(text_2))
        self.assertEqual("", detect_email(text_3))
        self.assertEqual("", detect_email(text_4))
        self.assertEqual("", detect_email(text_5))
        self.assertEqual("", detect_email(text_6))
        self.assertEqual("", detect_email(text_7))
        self.assertEqual("", detect_email(text_8))
        

    def test_detect_courses(self):
        #Create text containing courses, to be extracted
        text = ["List", "of strings", "Courses:------:.,[]{}German, English, French", "end"]
        text_1 = ["List", "of strings", "end"]
        #Test for correct extraction of courses no matter anny punctuation use
        self.assertEqual(["German", " English", " French"], detect_courses(text))
        #Test for correct ignoring of courses when not present in original resume
        self.assertEqual([], detect_courses(text_1))

    def test_detect_projects(self):
        #Create text containing courses, to be extracted
        text = ["List", "of strings", "PROJECTS", "Project----1", "", "Project----2", "Project----3",
                "-----------------------", "Courses:------:.,[]{}German, English, French"]
        text_1 = ["List", "of strings", "-----------------------", "Courses:------:.,[]{}German, English, French"]
        #Test for correct extraction of projects, ignoring use of -s and empty lines
        self.assertEqual(["Project----1", "Project----2", "Project----3"],
                         detect_projects(text))
        #Test for empty list when project not present in text
        self.assertEqual([], detect_projects(text_1))
        
#-----------------------------------------------------------------------------------------------#
    ### TESTS FOR HELPER FUNCTIONS ###

    def test_find_string_index(self):
        #Define element for which string index is needed
        element1 = '^'
        element2 = 'w'
        element3 = '2'
        string = "5^2=twentyfive"
        #Test for correct detection of different element indices
        self.assertEqual(1, find_string_index(element1, string))
        self.assertEqual(5, find_string_index(element2, string))
        self.assertEqual(2, find_string_index(element3, string))
        
    def test_check_alphabet(self):
        #Test for detection of uppercase/lowercase letters
        self.assertTrue(check_alphabet('d'))
        self.assertTrue(check_alphabet('X'))
        #Test for correct acceptance and rejection for lowercase letter
        self.assertTrue(check_alphabet('d', 'lower'))
        self.assertFalse(check_alphabet('D', 'lower'))
        #Test for correct acceptance and rejection for uppercase letter
        self.assertTrue(check_alphabet('Z', 'upper'))
        self.assertFalse(check_alphabet('z', 'upper'))
        #Test for correct rejection of numeric digits and special characters
        self.assertFalse(check_alphabet('$'))
        self.assertFalse(check_alphabet('0'))
                        
    def test_check_for_digits(self):
         #Test for true result for numeric string
         self.assertTrue(check_for_digits("123456789"))
         #Test for false result for non-numeric string
         self.assertFalse(check_for_digits("abcdefgh"))
         #Test for true result for presence for single digit char
         self.assertTrue(check_for_digits("abcd2efgh"))

    def test_find_line_index(self):
        #Define list within which to search for the index
        string_list = ["Harry Potter", "Hermione Granger", "Ronald Weasley"]
        #Define search strings to be located in list
        search_string1 = "ranger"
        search_string2 = "potter"
        search_string3 = "ronald"
        #Search for strings in list and check if correct index is found
        self.assertEqual(1, find_line_index(search_string1, string_list))
        self.assertEqual(0, find_line_index(search_string2, string_list))
        self.assertEqual(2, find_line_index(search_string3, string_list))

    def test_surround_block(self):
        #Test if function works for simple words
        self.assertEqual("<tag>text</tag>", surround_block("tag", "text"))
        #Test if function works for words with quotes
        self.assertEqual("<tag>tex\"t</tag>", surround_block("tag", "tex\"t"))

    def test_make_basic_info(self):
        #Test if function returns correct string
        self.assertEqual("<div><h1>Harry</h1><p>Email: hp@hogwarts.com</p></div>",
                         make_basic_info("Harry", "hp@hogwarts.com"))
        #Test if function returns correct output with missing email
        self.assertEqual("<div><h1>Harry</h1><p></p></div>",
                         make_basic_info("Harry", ""))

    def test_make_project_section(self):
        #Create project list for testing
        project_list = ["Art", "Music", "Dance"]
        #Test if function returns correct output string
        self.assertEqual("<div><h2>Projects</h2><ul><li>Art</li><li>Music</li><li>Dance</li></ul></div>",
                         make_project_section(project_list))

    def test_make_courses_section(self):
        #Create course list for testing
        courses = ["CIT590", "897MSSP"]
        #Test if function returns correct output string
        self.assertEqual("<div><h3>Courses</h3><span>CIT590, 897MSSP</span></div>",
                         make_courses_section(courses))
        
    def end_html():
        #Check that correct result is returned
        self.assertEqual("</div></body></html>", end_html())
        
unittest.main()
