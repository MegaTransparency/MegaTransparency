# FreeOpenData.com

The mission of FreeOpenData.com is to make government agencies transparent by default by generating overwhelming public demand for transparency, advocating well for black and white transparency laws that demand transparency as the default and mandate open data and publishing of all records released to members of the public where additional redaction wouldn't be required, making it free and easy for governments to publish open data and over-redacted previews of records requiring manual review/redaction to a centralized public database, providing a free viable alternative to expensive open data portals, and automating as much of the public disclosure process as possible.

Business plan: create the most popular open data site and offer subscription plans, consulting, advertising, job boards, books, courses, affiliate marketing, and swag.

Top competitors: https://socrata.com, https://carto.com/, https://opengov.com/, and https://data.world

Status:
* Currently copying Socrata's data catalog to BigQuery. https://bigquery.cloud.google.com/table/freeopendata-161213:copy_of_socrata_data.data_catalog
* Writing script to copy to BigQuery and keep updated all Socrata datasets

Infrastructure:
* Dedicated server with 32GB of ram, 8 Dedicated x86 64bit Cores, 300GB of SSD, and 800Mbit/s unlimited internet bandwidth machine for $26.25/month at https://www.scaleway.com/
* BigQuery: 2 cents per GB/month stored https://cloud.google.com/bigquery/ Taking advantage of the $300 in credits each new user gets for one year and 1TB of processed data every user gets every month forever
* Google G Suite https://gsuite.google.com/ for email and cheap storage http://www.techrepublic.com/article/how-to-mount-your-google-drive-on-linux-with-google-drive-ocamlfuse/
* CloudFlare.com

