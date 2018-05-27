# translation-olympics
***This repository is under very active development. Expect frequent updates as the experiments are ongoing.***

This is a collection of scripts used to quantitatively evaluate and compare the quality of Baidu, Bing, Google, Sogou and Yandex Translate.

The code is written in Python 3 (Python 2 not supported) and depends on Selenium's Python binding to scrape translation data.

The tests will be conducted using a subset of the Datum English-Chinese Parallel Corpus, made available for the 2017 WMT Conference.

***Contents:***
-Results So Far
-Experimental Procedure
-After the Experiments Are Done
-Current Status and Preliminary Findings
-Next Steps

***Spoiler Alert: Results So Far***

I have not yet analyzed the quality of the websites' Chinese to English translation, but Bing and Sogou seem to be the best at English to Chinese translation.

Bing has the highest median translation quality, and a satisfyingly low variance and IQR, indicating that its translations are pretty reliable and usually quite good.

Sogou has a fairly high median, the lowest variance and also has the highest 25th percentile, meaning its translations are very consistent, usually pretty good and almost never bad. Bing performs better than Sogou on average, but Sogou is more dependable to 'get the gist' of a translation.

***Experimental Procedure:***
1. Use Selenium to automatically enter sentences into the five websites, wait for them to translate (and wait some extra time in order to respect their terms of service), then scrape the translations and save them in a file.

2. Clean the data to make sure that formatting differences and style conventions do not adversely impact any website's score.

3. For English to Chinese translation, separate the words in all the Chinese sentences using Python's Jieba library. The same library is used for the entire experiment, so hopefully any inaccuracies generated from Jieba will not skew the experiment's results.

4. Use Python's NLTK implementation of the BLEU metric (see https://en.wikipedia.org/wiki/BLEU) to programmatically evaluate machine translation quality.

5. Analyze the results.

***After the Experiments Are Done:***

After the experiments are done, future research will involve using other metrics to evaluate performance, since BLEU does have some known limitations (including the fact that it is designed for languages that use spaces to separate words, which Chinese does not), as well as using a larger dataset.

Further research will also involve creating a webcrawler to automatically scrape parallel language data from various websites, or searching for an existing open source crawler that serves this purpose. This will be useful because the corpora made available for WMT 2017 (of which I think the Datum 2017 corpus used for these preliminary tests is the best) are all constrained to the domains of politics and news, and several of the corpora have low quality. So, a crawler-based approach is highly desirable, and will come in a future iteration of this project.

***Current Status and Preliminary Findings:***

Chinese to English translation results not yet analyzed, but the translations have already been scraped from the websites.

So far, Bing and Sogou Translate seem to be the winners for English to Chinese translation. Further testing is required, but based on the BLEU scores, on the dataset of 100 sentences analyzed, these are the winners. 

For the original English sentences, see newEnglish.txt; for the reference Chinese translations (translated by professional human translators), see newChinese.txt.

For the machine translations from each website, see newChineseOutputPostProcessed.txt.

For boxplots of the BLEU scores of each website on the dataset, see the png files, and for percentiles, variance and interquartile range of each website's performance, see results.txt.

Results are preliminary for several reasons:

1. I have done some pre- and post-processing of the data to try to make the tests fair, but I might have missed some processing which could have given some sites a disadvantage in BLEU evaluation.

2. The dataset is fairly small, and all the sentences are about very similar topics.

3. I have not yet examined the affect that Jieba could have on the results.

***Next Steps***

The next iteration of this project will include a preliminary analysis of the Chinese to English translations.

After that, I will clean up the programming style and make a smoother workflow, since right now you have to use a few different scripts in an order unintuitive to you, the reader.

Following that, I will expand the dataset to 200 sentences and analyze the results at that time.

Then, I will use translation quality metrics other than BLEU to get a more complete understanding of the quality of the websites' translations.

Following that, I will create or find a webcrawler to extract sentences from the web that are about topics other than news and politics, to provide a more complete picture of the translation websites' well-roundedness.

***There are lots of things to come, so I encourage you to follow this repository if you are curious***
