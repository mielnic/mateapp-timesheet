import math

def paginator(index, length, l):

    pageNumber = int(index/l) + 1
    pages = math.ceil(length / l) 
    links = []

    # Creates a dictionary list of pages, considering
    # total records and page length

    for i in range(pages):
        linkData = {}
        linkData['page'] = i + 1
        linkData['pl'] = i*l
        linkData['pr'] = (i*l)+l
        links.append(linkData)

    # Determine the page numbers to be displayed.

    if pages <= 5:
        start = 1
        end = pages
    elif pageNumber < 3:
        start = 1
        end = 5
    elif (pages-pageNumber) <= 2:
        start = (pages - 4)
        end = (pages)
    else:
        start = pageNumber - 2
        end = pageNumber + 2

    links = links[(start-1):(end)]

    # Determine the forward & back pages.

    if index == 0:
        idxPreviousL = 0
    else:
        idxPreviousL = index - l

    idxPreviousR = idxPreviousL + l

    if (index + l) >= length:
        idxNextR = index + l
    else:
        idxNextR = index + 2 * l

    idxNextL = idxNextR - l
    
    # Return the variables.

    return links, idxPreviousL, idxPreviousR, idxNextL, idxNextR