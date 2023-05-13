import models


def applications(selection=1):
    if selection == 1:
        models.document_summarizer()
    elif selection == 2:
        models.job_description_generator()
    elif selection == 3:
        models.multi_lingual()
    elif selection == 4:
        models.question_answering()
    elif selection == 5:
        models.resume_creator()
    elif selection == 6:
        models.resume_validator()
    elif selection == 7:
        models.summarizer_langchain()
    else:
        print("Invalid Selection")


if __name__ == '__main__':

    print("Welcome to Open Source AI")
    print("Select the application you want to run")
    print("1. Document Summarizer")
    print("2. Job Description Generator")
    print("3. Multi Lingual")
    print("4. Question Answering")
    print("5. Resume Creator")
    print("6. Resume Validator")
    print("7. Summarize Langchain")
    selection = int(input("Enter your selection: "))
    applications(selection)
    print("Thank you!!!")
