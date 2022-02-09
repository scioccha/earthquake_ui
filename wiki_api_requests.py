import wikipediaapi

def wiki_connect(search_term, section, subsection = None):
    """
    Takes as arguments a wikipedia search term, section and subsection (optional)
    and returns the paragraph of information in that section. If the page does not exist, returns an
    error message.
    """
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page_py = wiki_wiki.page(search_term)
    if page_py.exists():
        for s in page_py.sections:
            if subsection is not None:  #if a subsection was specified, search within section
                for sub in s.sections:
                    if sub.title == subsection:
                        return sub.text

            if s.title == section: #if not subsection was specified
                return s.text

        return page_py.summary #if section is not found, prints page summary
    else:
        return "Wikipedia Pages Does Not Exist. Please Refine Search Terms"


from sys import argv
if __name__ == "__main__":
    print(wiki_connect(argv[1], argv[2], argv[3]))


#example command line usage:
#python wiki_api_requests.py "Taylor Swift" "Artistry" "Influences"
#The above command will print the text for the Artistry:Incluences subsection of the
#Taylor Swift wikipedia page. Note that all search terms need to be strings.

#example use with no subsection:
#python wiki_api_requests.py "Arcata, California" "Geology" None
#use None as the third argument without quotes.


