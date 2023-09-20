#!/bin/py
import re

def extract_sentences(input_str):
    # Find all the sentences enclosed in double quotes
    speeches = re.findall(r'"(.*?)"', input_str)
    
    # Find all content not enclosed in double quotes
    descriptions = re.sub(r'"(.*?)"', '', input_str)
    
    return speeches, descriptions

# Example usage
if __name__ == "__main__":
    input_str = '''He said, "Hello, how are you?" She replied, "I am fine, thank you." They then walked to the park.'''
    
    speeches, descriptions = extract_sentences(input_str)
    
    print("Speeches:")
    for speech in speeches:
        print(speech)
    
    print("\nDescriptions:")
    print(descriptions)
