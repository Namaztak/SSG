from textnode import *
from htmlnode import *
from functions import *
import re
import os
import shutil


print("hello world")

def main():
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "public")
    
    

if __name__ == "__main__":
    main()