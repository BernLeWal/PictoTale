#!/bin/py
import re

def extract_sentences(input_str):
    isSpeaking = False
    result = []

    str = ""
    for c in input_str:
        if c=='"':
            result.append( (str, isSpeaking) )
            isSpeaking = not isSpeaking
            str = ""
        elif c=='.':
            str += c
            result.append( (str, isSpeaking) )
            str = ""
        else:
            str += c
    if len(str) > 0:
        result.append( (str, isSpeaking) )
    
    return result

# Example usage
if __name__ == "__main__":
    input_str = '''He said, "Hello, how are you?" She replied, "I am fine, thank you." They then walked to the park.'''
    print( input_str )
    print()
    
    sentences = extract_sentences(input_str)
    
    for s in sentences:
        print(s)
    
