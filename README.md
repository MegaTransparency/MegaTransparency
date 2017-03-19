# FreeOpenData.com

## Mission and Strategy

The mission of FreeOpenData.com is to make organizations, particularly government agencies, transparent by default. Its strategy is to create overwhelming public demand for transparency, advocate well for forceful black and white transparency laws, make the disclosure of information as efficient as possible, use public disclosure laws to their fullest reasonable potential, and make it extremely easy to make positive use of open data. A key strategy for making governments transparent by default is to get to the point where FreeOpenData can completely take over transparency work at no cost to each agency. The information would be made available to the public completely free. In order to do this, FreeOpenData needs about sixty million dollars a year just for Washington State. So the business plan is to create the most popular open data site and generate money through subscription plans, consulting, advertising, job boards, book and course publishing, affiliate marketing, and swag.

We will generate overwhelming public demand for transparency by putting on lots of public presentations about transparency, being on the news every month advocating that the public demand transparency. We will track the uses of transparency.

Most of today's transparency laws are transparency to a given requester. We want to change that to automated publishing to a centralized international database of all non-exempt records not requiring manual review or redaction and automated publishing of over-redacted previews of non-exempt records that would require manual review or redaction. We want to make manual public disclosure highly efficient by getting transparency laws to mandate that:
1. Records be created in electronic form in machine readable format
1. Signatures be added electronically
1. All records management software as implemented support automated retrieval of records
1. Exemptions are black and white eliminating guessing about whether or not a piece of information needs to be redacted, third party notification inviting lawsuit when agencies should just be releasing or not releasing records, and long court reviews of good faith decisions
1. Public safety records not requiring manual redaction are automatically sent to involved parties including attorneys
1. Employees are trained in exemptions and when creating records mark what information needs to be redacted, except for public safety audio and video that isn't tied to a police report, and that agencies are to depend on those markings
1. Schemas of databases are to be published
1. Raw data powering cloud services used by the government be subject to disclosure. For example Taser's evidence.com has an audit trail system. The entire listing of what happened to each piece of evidence should be public just like that for Seattle Police's COBAN dashcam system: https://data.seattle.gov/Public-Safety/COBAN-Logs/tpvk-5fr3/data
1. Companies publish diversity stats

To make the disclosure of information as efficient as possible FOD will provide a free open source hosted viable alternative to expensive open data and records requesting portals.

In the beginning FOD is going to have to request most data through the various public records acts. 

Make the use of open data so easy that people pay good money to use the same tools on private data.

## History

The site was created in response to http://datasmart.ash.harvard.edu/news/article/an-open-letter-to-the-open-data-community-988 and an erroneous Google marketing blurb claiming public datasets are hosted for free on BigQuery. FreeOpenData.com is owned by WayEasy Corporation, which is lead by Tim Clemans https://transparenttim.com. Tim had the honor of working for Seattle Police as an employee piloting automatic publishing of over-redacted body camera videos and police report narratives to give frequent records requesters a tool for making narrow records requests, see https://www.nytimes.com/2016/10/23/magazine/police-body-cameras.html?_r=0 Tim is currently homeless, housed in a private room in a shelter, while he finishes life skills and food service training at http://farestart.org Starting in about two months, he needs to make about a thousand a month to make ends meet. Becoming a contractor for Socrata to improve on what he did at Seattle Police fell through and his last employer SageMath Inc https://sagemathcloud.com decided it was too stressful to review the code he wrote. So now he's focusing on employing himself to make governments transparent by default. Funding for the site currently comes from Tim's parents. 

## Values

* Transparent by default: clear business rules, all code is open source under Apache License unless using an existing code base that is licensed as GPL/AGPL (Wordpress/CKAN/CoCalc)

## Competitors

Top competitors: https://muckrock.com, https://data.world, https://socrata.com, https://carto.com/, https://opengov.com/, http://govqa.com/, and https://www.nextrequest.com/.

Initially we're focused on competeting with MuckRock and DataWorld because these sites focus on making money from end users like us. It'll take time to build the government relationships needed to compete with Socrata, OpenGov, Carto, GovQA, and NextRequest. It's important that Socrata in particular see FreeOpenData as encouraging more agencies to adopt open data and look into Socrata. Maybe they can be advertisers at some point if user is using a known government computer. One strategy to consider with say Socrata is to say "We want transparency to be free and as automated as possible. What do you think of focusing on becoming the analytics platform governments rely on and make transparency an automatic byproduct of that?"

## Roadmap and Status

### Roadmap

* Write script to copy to BigQuery and keep updated all Socrata datasets
* Make the blog
* Make the website
* Don't start filing public disclosure requests until have the money to pay for them and don't file one requiring legal action until have money for lawyers

#### Income goals

1. \$2,000/month: 100 \$19.99 subscribers (yes I know that 19.99 * 100 is just under 2K and that there will be credit card processing fees)
  * $12,000/year in total compensation for Tim Clemans including social security taxes and benefits
  * $12,000/year for computer related costs, records request fees, and other expenses/taxes and saving up
1. \$40,000/month: 2,000 \$19.99 subscribers
  * $240,000/year in total compensation for Tim Clemans including social security taxes and benefits
  * $120,000/year for computer related costs, records request fees, and other expenses/taxes and saving up
  * $120,000/year for filing public disclosure related lawsuits

### Status

* Currently copying Socrata's data catalog to BigQuery. https://bigquery.cloud.google.com/table/freeopendata-161213:copy_of_socrata_data.data_catalog
* Writing script to copy to BigQuery and keep updated all Socrata datasets

## Infrastructure

* Dedicated server with 32GB of ram, 8 Dedicated x86 64bit Cores, 300GB of SSD, and 800Mbit/s unlimited internet bandwidth machine for $26.25/month at https://www.scaleway.com/
* BigQuery: 2 cents per GB/month stored https://cloud.google.com/bigquery/ Taking advantage of the $300 in credits each new user gets for one year and 1TB of processed data every user gets every month forever
* Google G Suite https://gsuite.google.com/ for email and cheap storage http://www.techrepublic.com/article/how-to-mount-your-google-drive-on-linux-with-google-drive-ocamlfuse/
* CloudFlare.com

