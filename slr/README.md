# SLYRAT Systematic Literature Review Assistant

A tool for automating the process of generating systematic liteature reviews in an interative workflow.

## Contributors

Tim Storer

## Notes

A systematic literature review is an iterative process based on the following stages.

1. Raw search based on keywords of multiple databases.

2. Merger of results from all searches

3. Filtering of results based on:

 * Irrelevance of field (indicated by keywords in publication venue)
 * Date ranges

4. Forward and backward snowballing to identify further relevant papers.

5. Manual review of titles and abstracts so that they can be marked as irrelevant and are not re-included in future
   iterations.

An automated tool for doing this would be really helpful!

Components:

 * A library class for retrieving bibtex entries for each database service.  Each library class would need to support
   both searching and snowballing.

 * A Merger mechanism that marked each entry with its source and original keyword, e.g.
    database_id={ACM:10}

 * A Filtering mechanism for relevant field and date range

 * An interactive tool for

## Implementation Notes

Can download bibtex references from the ACM like this:

https://dl.acm.org/downformats.cfm?id=10&parent_id=&expformat=bibtex

Can search like this:

https://dl.acm.org/exportformats_search.cfm?query=test&filtered=&within=owners%2Eowner%3DHOSTED&dte=&bfr=&srt=%5Fscore&expformat=bibtex