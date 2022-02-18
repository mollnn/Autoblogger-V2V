# Video Extractor

Automatically extract the best clips from streaming media and edit them into mixed videos

Structure description:

The web is the front end of the material monitoring system for the extractor.

web-man manages the front end for the extractor website.

webservice is the backend of the extractor website, including the core components of the extractor, which is used to crawl videos, analyze videos, and generate video clips. The visualization backend has not been merged for the time being.

data is the location where the extractor stores/outputs data.

tmp is used by the extractor to store some temporary files. Currently it needs to be cleared manually and periodically.

The last merge has been undone.
