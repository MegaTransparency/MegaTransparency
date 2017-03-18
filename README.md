# FreeOpenData.com

This site was created in response to http://datasmart.ash.harvard.edu/news/article/an-open-letter-to-the-open-data-community-988 and an erroneous Google marketing blurb claiming public datasets are hosted for free on BigQuery. FreeOpenData.com is owned by WayEasy Corporation, which is lead by Tim Clemans https://transparenttim.com. Tim had the honor of working for Seattle Police as an employee piloting automatic publishing of over-redacted body camera videos and police report narratives to give frequent records requesters a tool for making narrow records requests, see https://www.nytimes.com/2016/10/23/magazine/police-body-cameras.html?_r=0 Tim is currently homeless, housed in transitional housing, while he finishes life skills and food service training at http://farestart.org Starting in about two months, he needs to make about a thousand a month to make ends meet. Becoming a contractor for Socrata to improve on what he did at Seattle Police fell through and his last employer SageMath Inc https://sagemathcloud.com. decided it was too stressful to review the code he wrote. So now he's focusing on employing himself to make governments transparent by default. Funding for the site currently comes from Tim's parents. 

[Note to readers: please suggest improvements to the mission. It's way too long/wordy] The mission of FreeOpenData.com is to make government agencies transparent by default by generating overwhelming public demand for transparency, advocating well for black and white transparency laws that demand transparency as the default and mandate open data and publishing of all records released to members of the public where additional redaction wouldn't be required, making it free and easy for governments to publish open data and over-redacted previews of records requiring manual review/redaction to a centralized public database, providing a free viable alternative to expensive open data portals, and automating as much of the public disclosure process as possible.

Need a lot of money to be able to offer government agencies the sweet deal of taking over their open data and public disclosure efforts. So the business plan is to create the most popular open data site and offer subscription plans, consulting, advertising, job boards, books, courses, affiliate marketing, and swag.

Values:
* Transparent by default: clear business rules, all code is open source under Apache License unless using an existing code base that is licensed as GPL/AGPL (Wordpress/CKAN/CoCalc)

Top competitors: https://socrata.com, https://carto.com/, https://opengov.com/, and https://data.world

To-do:
* Write script to copy to BigQuery and keep updated all Socrata datasets
* Make the blog
* Make the website

Status:
* Currently copying Socrata's data catalog to BigQuery. https://bigquery.cloud.google.com/table/freeopendata-161213:copy_of_socrata_data.data_catalog
* Writing script to copy to BigQuery and keep updated all Socrata datasets

Infrastructure:
* Dedicated server with 32GB of ram, 8 Dedicated x86 64bit Cores, 300GB of SSD, and 800Mbit/s unlimited internet bandwidth machine for $26.25/month at https://www.scaleway.com/
* BigQuery: 2 cents per GB/month stored https://cloud.google.com/bigquery/ Taking advantage of the $300 in credits each new user gets for one year and 1TB of processed data every user gets every month forever
* Google G Suite https://gsuite.google.com/ for email and cheap storage http://www.techrepublic.com/article/how-to-mount-your-google-drive-on-linux-with-google-drive-ocamlfuse/
* CloudFlare.com

