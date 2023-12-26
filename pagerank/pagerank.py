import os
import random
import re
import sys
import numpy as np
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus:dict, page:str, damping_factor:float) -> dict:
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    linked_pages = corpus[page]
    num_linked_pages = len(linked_pages)
    num_total_pages = len(corpus)    

    if num_linked_pages == 0:
        probability_distribution = { page : 1/num_total_pages for page in corpus}
        return probability_distribution

    probability_distribution = dict()
    probability_for_linked_pages = round(damping_factor/num_linked_pages, 7)
    probability_for_all_pages = round((1-damping_factor)/num_total_pages,7)

    for page in corpus.keys():
        if page in linked_pages:
            probability_distribution[page] = probability_for_linked_pages + probability_for_all_pages
        else:
            probability_distribution[page] = probability_for_all_pages
        
    return probability_distribution



def sample_pagerank(corpus:dict, damping_factor:float, n:int) -> dict:
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_samples_left = n
    page_rank_values = {page : 0 for page in corpus}

    previous_sample = random.choice(list(corpus.keys()))
    page_rank_values[previous_sample] += 1
    num_samples_left -= 1

    while(num_samples_left > 0):
        pages, probs = zip(*transition_model(corpus,previous_sample,damping_factor).items())
        next_page = np.random.choice(pages, p=probs)
        page_rank_values[next_page] += 1
        num_samples_left -= 1
        previous_sample = next_page
    
    #Normalize dictionary
    for key in page_rank_values:
        page_rank_values[key] /= n
    
    return page_rank_values

def iterate_pagerank(corpus:dict, damping_factor:float) -> dict: 
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_total_pages = len(corpus)
    PR = {page : 1/num_total_pages for page in corpus}

    #Corpus goes: page links to these others pages
    #i in the formula means all pages that link to this page
    each_possible_page_that_links_to_p = {page : [] for page in corpus}
    for page in corpus.keys():
        for linkedPage in corpus.keys():
            if page != linkedPage and page in corpus[linkedPage]:
                each_possible_page_that_links_to_p[page].append(linkedPage)

    threshhold = 0.001
    while(True):
        max_change = -math.inf
        for page in corpus.keys():
            old_PR_val = PR[page]
            new_PR_val = (1-damping_factor)/num_total_pages

            iterating_sum = 0
            for i in each_possible_page_that_links_to_p[page]:
                num_links_on_page_i = len(corpus[i])

                if num_links_on_page_i == 0:
                    iterating_sum += (PR[i]/num_total_pages)
                else:
                    iterating_sum += (PR[i]/num_links_on_page_i)
            
            new_PR_val += (damping_factor * iterating_sum)
            PR[page] = new_PR_val
            max_change = max(max_change,abs(PR[page]-old_PR_val))
        
        if(max_change < threshhold): 
            break
        

    return PR


if __name__ == "__main__":
    main()
