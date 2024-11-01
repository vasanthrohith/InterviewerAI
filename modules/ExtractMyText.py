from spire.pdf import *
from spire.pdf.common import *


class Extract_TXT:
    def __init__(self) -> None:
        pass

    def extractme(self,pdf_path):

        self.text=""

        pdf = PdfDocument()

        # Load the PDF document
        pdf.LoadFromFile(pdf_path)

        # Create a TXT file to save the extracted text
        # extractedText = open("Output/ExtractedText.txt", "w", encoding="utf-8")

        # Iterate through the pages of the document
        for i in range(pdf.Pages.Count):
            # Get the page
            page = pdf.Pages[i]
            # print(page)

            # Create a PdfTextExtractot object
            textExtractor = PdfTextExtractor(page)

            # Create a PdfTextExtractOptions object
            extractOptions = PdfTextExtractOptions()

            # Set IsExtractAllText to Ture
            extractOptions.IsExtractAllText = True

            self.text+= textExtractor.ExtractText(extractOptions)
            # print(text)

        return self.text


# o=Extract_TXT()
# o.extractme(pdf_path=r"C:\Users\CVHS ADMIN\Documents\github_repos\InterviewerAI\InterviewerAI\CVs\vasanth-AIML-07082024.pdf")


