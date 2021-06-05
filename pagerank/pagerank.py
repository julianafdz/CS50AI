import os
import random
import re
import sys

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


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    linked_pages = corpus[page]
    trans_dict = {}
    if linked_pages:
        num_of_links = len(linked_pages)
        prob = damping_factor / num_of_links
        p_of_page = (1 - damping_factor) / len(corpus)
        p_of_link = prob + p_of_page
        for page in corpus:
            if page in linked_pages:
                trans_dict[page] = p_of_link
            else:
                trans_dict[page] = p_of_page
        return trans_dict
    else:
        num_of_links = len(corpus)
        p_of_page = 1 / num_of_links
        for page in corpus:
            trans_dict[page] = p_of_page
        return trans_dict
        

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    res_dict = {}
    for key in corpus:
        res_dict[key] = 0
    rand_page = random.choice(list(corpus.keys()))
    rand_link = random.choice(list(corpus[rand_page]))
    for i in range(n):        
        res_dict[rand_link] += 1
        trans_dict = transition_model(corpus, rand_link, damping_factor)
        res_link = random.choices(list(trans_dict.keys()), trans_dict.values())
        rand_link = res_link[0]
    for page in res_dict:
        res_dict[page] /= n
    return res_dict   


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    res_dict = {}
    n = len(corpus)
    init_value = 1 / n    
    for key in corpus:
        res_dict[key] = init_value
    while True:
        ranks_dict = {}
        for page in corpus:
            ranks_dict[page] = ((1 - damping_factor) / n) + (damping_factor * sigma_function(page, corpus, res_dict))
        checker = True
        for page in res_dict:
            if round(ranks_dict[page] - res_dict[page], 3) > 0.001:
                checker = False
                break                
        if checker == True:
            return ranks_dict
        else:
            res_dict = ranks_dict.copy()        


def sigma_function(page, corpus, res_dict):
    result = 0
    for i in corpus:
        links = corpus[i]
        if not links:
            links = corpus.keys()
        if page in links:            
            result += (res_dict[i] / len(links))
    return result


if __name__ == "__main__":
    main()
