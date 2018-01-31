
# Analyzing Speeches by Douglass and Trump
- Import using Selenium, BeautifulSoup or load speeches.txt
- Measure word frequency
- Construct Word Clouds
- Sentiment Analysis
- Topic Model: Latent Dirichlet Distribution

# Structure
main_trump_speeches.py: 
- load and clean 12 trump speeches
- sort, select and visualize n most frequent words
- sentiment analysis

main_trump.py:
- using beautiful soup

main_lda.py:
- load and clean 12 trump speeches
- Topic Model: Latent Dirichlet Allocation

main_douglass.py:
- use selenium to download Douglass' speech
- analysis as in main_trump_speeches.py
- optional: use selfmade html parser

stromtrooper_wordcloud_script.py:
- load cleaned speeches as saved in the main functions
- create custom word cloud

furthermore:
- png's present output
- geckodriver required for selenium
- dictionary required for sentiment analysis
