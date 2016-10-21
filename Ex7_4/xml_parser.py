#!/usr/bin/env python
"""
###############################################################################
# FILE NAME : xml_parser.py
# AUTHOR : J.Enochs
# CREATION DATE : 20-Oct-2016
# LAST MODIFIED : 21-Oct-2016
# DESCRIPTION : XML parser example
#               A tutorial can be found here: http://lxml.de/tutorial.html 
#
###############################################################################/
"""

import argparse
from lxml import etree as ET

LEVEL = 0

def main():

    ##################### PARSE XML FROM FILE #####################

    # Read in the file
    f = open("books.xml")
    
    # Parse the XML out of the file and store in a variable named 'tree' 
    tree = ET.parse(f)

    # Find the root (uppermost) element and save to the variable 'root'
    root = tree.getroot()


    print"\n##################### PARSE XML FROM STRING #####################\n"

    # Make a string containing XML to demonstrate
    xml_string = "<message>data</message>"
    
    # Read from string
    node = ET.fromstring(xml_string)
    print ET.tostring(node)

    print"\n##################### PRINT #####################\n"

    # Print the entire tree
    print (ET.tostring(root, pretty_print=True))

    # Print the name of any given element 
    print "\n{}\n".format(root.tag)

    # Print the sub-elements of an element.  This only drills down one level.
    for child in root:
        print child.tag
    
    print "\n"
    for child in root:  # compare with .iter() below
        print child.tag

    print "\n"
    for child in root.iter(): 
        print child.tag

    print "\n"
    # Recursively print sub-elements of an element without duplicates
    # Took several lines so it's a function (functions at the bottom)
    map_sub_elements(root)


    ##################### TEST #####################

    # Test if it's some kind of element
    if ET.iselement(root):
        pass  # do something

    # Test if it has children
    if len(root):
        pass # do something


    print"\n##################### ADD, INSERT & MOVE ELEMENTS #####################\n"

    # Create an element from scratch instead of reading from file
    myElement = ET.Element("master")

    # ADD children to our new element
    child1 = ET.SubElement(myElement, "child1")
    child2 = ET.SubElement(myElement, "child2")
    child3 = ET.SubElement(myElement, "child3")

    for child in myElement: # Print our first 3 children
        print child.tag

    # INSERT a 4th sub-element  at index 0
    myElement.insert(0, ET.Element("Pet"))
    
    print "\n"
    for child in myElement: # Print to see we now have 4 children
        print child.tag

    # MOVE the last sub-element to index 0 (the first position)
    myElement[0] = myElement[-1] # Overwrites myElement[0] ! So not only
                                 # did you move the last child but you
                                 # deleted the first by overwriting it.

    print "\n"
    for child in myElement:  # Now we only have 3 children again
        print child.tag


    print"\n##################### Access siblings and parent #####################\n"

    # Who's your daddy!
    parent = child2.getparent()
    print "\nThe parent of {} is {}\n".format(child2.tag, parent.tag)

    # Stop touching me!
    previous_element = child2.getprevious()
    print previous_element.tag
    previous_element = myElement[1].getprevious()  # also works by indexing the parent
                                        # this returns the child at master[0]
    print previous_element.tag
    
    next_element = child1.getnext()
    print next_element.tag  # You should test to ensure you have something
    next_element = myElement[1].getnext()  # also works by indexing the parent
                                        # this returns the child at master[0]
    print next_element.tag


    print"\n##################### Add attributes #####################\n"

    # Add an attribute 
    myElement = ET.Element("master", mode="auto") # Attributes stored in dict
    print ET.tostring(myElement)
    
    # Another way to add an attribute
    myElement.set("color", "red")
    print ET.tostring(myElement)

    # Get a sorted list of an element's attributes
    print sorted(myElement.keys())

    
    print"\n##################### Add text to an element #####################\n"
    
    child2.text = "Adopted"
    print ET.tostring(child2)  # prints entire child2 element
    print ET.tostring(child2, method="text")  # prints only the text


    print"\n##################### Searching with XPATH #####################\n"

    # Extract an element's text using XPATH
    line1 = (child2.xpath("string()")) # print only the text - no getparent()
    line2 = (child2.xpath("//text()")) # places the text in a list 
    print(child2.xpath("//text()")) # prints: ["Adopted"] 

    # Who's the parent of the text string "Adopted"
    parent = line2[0].getparent()
    print parent.tag  # Child2


    print"\n##################### Searching without XPATH #####################\n"
    
    # Build new tree
    base = ET.Element("base")
    ET.SubElement(base, "child").text = "Child1"
    ET.SubElement(base, "child").text = "Child2"
    ET.SubElement(base, "child").text = "Child3"
    ET.SubElement(base, "pet").text = "Child4"
    print(ET.tostring(base, pretty_print=True))

    # Find a specific element by its name (tag)
    for element in base.iter("child"):
        print "{} - {}".format(element.tag, element.text)

    for element in base.iter("pet"):
        print "{} - {}".format(element.tag, element.text)

    # Find the description that mentions James Salway
    for element in root.iter("description"):
        if "James Salway" in element.text:
            print "{} - {}".format(element.tag, element.text)



    ##################### FUNCTIONS #####################
    
def map_sub_elements(element):
    global LEVEL  # This statement permits us to change the value of this global
                  # variable. Otherwise LEVEL would be read-only
                  # LEVEL is used by get_spacer() to determine indentation  
    dup_killer = {}  # Used below to eliminate duplicate sub-elements
    if LEVEL == 0: # Only print the root element once at the beginning 
        print "\n{}".format(element.tag)
    for sub in element: 
        dup_killer[sub.tag] = sub # Sub-elements with same name (tag) overwrite
    spacer = get_spacer() # Spacer used to format the output when printed
    for sub_element in dup_killer: # Unique sub_elements 
        print "{}{}".format(spacer, dup_killer[sub_element].tag)
        if len(dup_killer[sub_element]): # Evals to true only when not empty
            LEVEL += 1
            map_sub_elements(dup_killer[sub_element]) # recursion
            LEVEL -= 1

def get_spacer():
    if LEVEL == 0:
        spacer = "   |__"
    elif LEVEL == 1:
        spacer = "       |__"
    elif LEVEL == 2:
        spacer = "           |__"
    elif LEVEL == 3:
        spacer = "               |__"
    elif LEVEL == 4:
        spacer = "                   |__"
    elif LEVEL == 5:
        spacer = "                       |__"
    elif LEVEL == 6:
        spacer = "                           |__"
    elif LEVEL == 7:
        spacer = "                               |__"
    return spacer

        



    





if __name__ == "__main__":
    main()
