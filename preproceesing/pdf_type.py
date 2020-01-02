
import PyPDF2
def pdftype(file):    
    object = PyPDF2.PdfFileReader(file)
    NumPages = object.getNumPages()
    # extract text and do the search
    for i in range(0, NumPages):
        PageObj = object.getPage(i)
        #print("this is page " + str(i)) 
        Text = PageObj.extractText() 
    if Text!="":
        print("pdf is searchable") #pytesseract
        document="readable"  
    else:
        print("pdf is scanned or not searchable") #computer vision
        document="scanned"
    return document