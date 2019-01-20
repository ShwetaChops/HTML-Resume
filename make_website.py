"""
HW 5 - MAKE WEBSITE
"""

"""
Program that reads resume text files and
creates formatted HTML verisons for display
"""

### FUNCTIONS FOR PARSING THE FILE ###

def read_file(file):
    """
    Function that reads text files and stores the lines as a list
    """
    #Open file to read
    with open(file, 'r') as fin:
        lines = fin.readlines()
    #Return a list containing lines
    return lines

def clean_text(lines):
    """
    Function that cleans lines in a list by removing all unnecessary whitespaces
    """
    clean_lines = []
    for line in lines:
        line = line.strip()
        clean_lines.append(line)
    return clean_lines


def detect_name(lines):
    """
    Function that detects the name on the Resume
    """
    #Check to ensure the first letter of the name is uppercase, and that the line is not another section, else return error
    if check_alphabet(lines[0][0], 'upper') and "@" not in lines[0] and "projects" not in lines[0].lower() and "courses" not in lines[0].lower():
        name = lines[0]
        return name
    else:
        raise RuntimeError("Warning: First line of Resume must be Name, with first letter capitalized!")

def detect_email(lines):
    """
    Function that detects and returns the email id in the Resume
    """
    email = ""
    for line in lines:
        #Look for the line that contains @
        if '@' in line.lower():
            #Store index for the @ in the email line
            at_index = line.index("@")
            #Ensure email id ends in .edu or .com
            if line[-4:] == '.edu' or line[-4:] == '.com':
                #Ensure at least 1 lowercase letter exists after '@' and before '.'
                if check_alphabet(line[find_string_index('@', line) + 1], 'lower'):
                    #Ensure email doesn't contain any digits
                    if check_for_digits(line) is False:
                        #Ensure email key is all alphabetical
                        for char_index in range(at_index):
                            if check_alphabet(line[char_index]) is False:
                                return email
                        #Ensure no space in email
                        if " " not in line:
                            email += line
                            return email
               
    return email


def detect_courses(lines):
    """
    Function that extracts and returns a list
    of all courses mentioned in the resume
    """
    #Look for line that contains the word 'Courses'
    for line in lines:
        if 'courses' in line.lower():
            course_line = line

            #Locate index from where the course names begin, ignoring punctuations
            for index in range(7,(len(course_line) + 1)):
                if check_alphabet(course_line[index]):
                    start_index = index
                    break

            #Extract courses from string and save as list, to be returned
            course_list = course_line[start_index:].split(",")
            return course_list
    #If no courses detected, return empty list
    return []


def detect_projects(lines):
    """
    Function that extracts and returns a list of
    projects mentioned in the resume
    """
    #Look for line index that contains the word 'Projects'
    start_line_index = find_line_index('projects', lines)

    #Look for line index that contains at least ten -s
    end_line_index = find_line_index("----------", lines)

    #Extract all strings between start and end line indices that are not blank
    project_list = []
    if type(start_line_index) == int and type(end_line_index) == int:
        for line in lines[(start_line_index + 1):(end_line_index)]:
            if line == '':
                continue
            else:
                project_list.append(line)

    return project_list
    
#_______________________________________________________________________#
    
### HELPER FUNCTIONS ###

def find_string_index(element, main_string):
    """
    Function that finds the index of an element in a string
    """
    index = main_string.index(element)
    return index

def check_alphabet(element, case = False):
    """
    Function that returns a boolean value
    for whether a character is alphabet satisfying an
    optional case condition
    """
    import string
    alphabet_lower = list(string.ascii_lowercase)
    alphabet_upper = list(string.ascii_uppercase)
    alphabet_all = alphabet_lower + alphabet_upper

    if case == 'lower':
        if element in alphabet_lower:
            return True
        else:
            return False
    elif case == 'upper':
        if element in alphabet_upper:
            return True
        else:
            return False
    elif case is False:
        if element in alphabet_all:
            return True
        else:
            return False
    else:
        print("Case argument must be 'upper' or 'lower'\n")

def check_for_digits(main_string):
    """Function that returns boolean value for
    whether a string contains any digits"""
    #Set up digits list
    digits = list("0123456789")

    #Check if string contains any digit
    for char in main_string:
        if char in digits:
            return True
    else:
            return False


def find_line_index(search_string, lines_list):
    """
    Function that returns the index for
    which list element contains a certain search string
    """
    #Look for line index that contains the search string
    for index in range(len(lines_list)):
        if search_string in lines_list[index].lower():
            line_index = index
            return line_index
    
def surround_block(tag, text):
    """
    This function surrounds the given text with the given HTML tag
    and returns the string
    """
    return "<" + tag + ">" + text + "</" + tag + ">"


def make_basic_info(name, email):
    """
    Function that creates the basic info section of the resume
    """
    #Check if email is blank, then do not write that in basic info block
    if email != "":
        basic_info = surround_block("div", surround_block("h1", name) +
                                    surround_block("p", "Email: " + email))
    else:
        basic_info = surround_block("div", surround_block("h1", name) +
                                    surround_block("p", email))
    #Write basic info block to html
    return basic_info


def make_project_section(project_list):
    """
    Function that creates the project section of the resume
    """
    if project_list != []:
        #Header
        project_header = surround_block("h2", "Projects")
    
        #Projects list
        project_bullets_list = []
        for project in project_list:
            project_line = surround_block("li", project)
            project_bullets_list.append(project_line)
        #Merge project bullets into a string
        project_bullets = "".join(project_bullets_list)
        #Create bullets section
        bullets_section = surround_block("ul", project_bullets)

        #Create entire block
        project_block = surround_block("div", project_header + bullets_section)
        return project_block

    else:
        return ""

    
def make_courses_section(course_list):
    """
    Function that creates the courses section of the resume
    """
    if course_list != []:
        
        #Create single course list as string
        course_string = ", ".join(course_list)
        
        #Create entire block to be printed
        courses_block = surround_block("div", surround_block("h3", "Courses") +
                                       surround_block("span", course_string))
        return courses_block

    else:
        return ""
    
def end_html():
    """
    Function that returns string to end the html
    """
    return "</div></body></html>"

#_______________________________________________________________________#
        
### MAIN FUNCTION ###

def main():
    #Read file into program memory
    text = read_file("test_hw5.txt")
    #Clean text to ensure extra whitespaces are removed
    text = clean_text(text)

    #Extract name
    name = detect_name(text)

    #Extract email id
    email = detect_email(text)
    
    #Extract list of courses
    courses = detect_courses(text)

    #Extract list of projects
    projects = detect_projects(text)

    #Open HTML, prepare to write
    f = open("resume.html", "r+")
    lines = f.readlines()
    f.seek(0)
    f.truncate()
    del lines[-1]
    del lines[-1]
    f.writelines(lines)

    #Add first line within html
    f.write("<div id=\"page-wrap\">")

    #Write basic information section
    f.write(make_basic_info(name, email))

    #Write projects section
    f.write(make_project_section(projects))

    #Write courses section
    f.write(make_courses_section(courses))

    #Print last 3 lines to html
    f.write(end_html())

    #Close stream
    f.close()

if __name__ == '__main__':
    main()
