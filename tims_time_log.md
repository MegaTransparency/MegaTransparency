4/6/17

* 12:13PM - 2:20PM: writing ETL script for Washington Voter Registration, talking with a reporter who told me to look up Pink Hankasher, writing a Socrata query for officers with most level 2/3 use of force
* sloppy didn't record time prior to 12:13PM

4/4/17 - 4/5/17

* sloppy didn't record time

4/3/17

* 6:00PM - : deal with login 
* 4:00PM - 5:20PM: make font size smaller, log almost every view and get/post data so can make a show me my past queries, start using VueJS

4/2/17

* was sloppy and didn't record my times. Wrote script that publishes public page views and wrote API to access it

4/1/17

* 10:00PM - 10:50PM: setting up MegaTransparency. Doing name change etc. Main reason for change is I stupidly canceled my phone account without first disabling two factor. Phone company said it wasn't possible to get a new account with old phone number even though old number isn't in use. Figured best thing to do was create new domains account and new domain.

3/28/17 - 3/31/17

* Had really bad week. Ended up in hospital for mental health.

3/27/17

* 11:18PM - 11:59PM: figuring out how to do if current_time > very first time arrived + 30 minutes SELECT date_part('epoch',now())*1000;
* 9:36PM - 11:14PM: figuring out how to update past page views with user uuid 
* 8:48PM - 9:17PM: came up with this query to get the first time arrived for each session uuid SELECT 'session_public_uuid' AS what_uuid, session_public_uuid, min(time_arrived) AS first_time_arrived FROM (SELECT data->>'session_public_uuid' AS session_public_uuid, data->>'time_arrived' AS time_arrived FROM page_views) AS pv WHERE session_public_uuid IS NOT NULL GROUP BY session_public_uuid UNION SELECT 'user_uuid' AS what_uuid, user_uuid, min(time_arrived) AS first_time_arrived FROM (SELECT data->>'user_uuid' AS user_uuid, data->>'time_arrived' AS time_arrived FROM page_views) AS pv WHERE user_uuid IS NOT NULL GROUP BY user_uuid;
* 8:34PM - 8:48PM: more fixes to session code, filed a request to Seattle Police for RMS operational status and case access audit trail
* 7:10AM - 7:46AM: for the 30 minute privacy grace period start looking into adding user_uuid to all page view rows with current session public uuid, file request to Seattle Police for customized access fee to get audit trail data for body cams
* 12:00AM - 12:38AM: working on 30 minute privacy grace period

3/26/17

* 11:40PM - 11:59PM: adding session id so can implement the 30 minute privacy grace period
* 12:16PM - 2:00PM: Write some javascript to update pageview data with time left, mouse locations, and resolution
* 10:00AM - 11:50AM: "Implement public activity log" https://github.com/wayeasycorp/FreeOpenData/issues/17, setting up postgresql on my sagemathcloud project so I can do python2 manage.py migrate see https://github.com/sagemathinc/smc/wiki/Using-PostgreSQL-in-SageMathCloud 
* 8:15AM - 8:30AM: writing up https://github.com/wayeasycorp/FreeOpenData/issues/17

3/25/17

* 5:36PM - 6:00PM: enabling Google login
* 4:23PM - 5:36PM: working through http://serverfault.com/questions/775965/wiring-uwsgi-to-work-with-django-and-nginx-on-ubuntu-16-04
* 8:16AM - 9:27AM: getting deployment going, really confused/stuck about how to deploy via uwsgi
* 6:20AM - 8:00AM: setting up postgresql, configuring the app, trying get deployment going
* 4:32AM - 6:00AM: setting up the server, writing down instructions for setup

3/24/17

* 5:40PM - 6:00PM: working towards getting a new server going and get FOD deployed

3/23/17

* 5:03PM - 9:12PM: got uwsgi working manually `uwsgi --http-socket :9090 --wsgi-file wsgi.py --callable app`, remove javascript based https forcer, will force via nginx, so can use app in test mode, for upstart I had to install sudo apt-get install upstart-sysv, can't seem to get site served up via nginx, the info in /etc/init/freeopendata.conf was wrong, server refused to reboot, was unable to fix boot using rescue boot, was able to copy key files
* 1:33PM - 3:04PM: https://github.com/wayeasycorp/FreeOpenData/issues/14, https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04, various static file changes, wasn't able to get uwsgi working on command line, stupid power/internet went out

3/22/17

* 5:00PM - 9:00PM: Open Seattle: talked with Socrata's Chris Metcalf and a person on the migrations team about how to improve the Socrata to BigQuery ETL.
* 6:20AM - 6:30AM: committing code pushing
* 5:00AM - 5:40AM: got database table creation working

3/21/17

* 8:30PM - 9:06PM: got login via command line working but can't seem to create database tables like before
* 8:00PM - 8:25PM: https://github.com/wayeasycorp/FreeOpenData/issues/9 struggling with logging into postgres via command line
* 7:30PM - 7:40PM: github
* 7:00PM - 7:30PM: https://github.com/wayeasycorp/FreeOpenData/issues/4
* 5:10PM - 5:45PM: walking around thinking about features to make and when
* 7:25AM - 7:30AM: for https://github.com/wayeasycorp/FreeOpenData/issues/2 add verify=False

3/20/17

* 7:56PM - 8:57PM: https://github.com/wayeasycorp/FreeOpenData/issues/2
* 7:14PM - 7:51PM: https://github.com/wayeasycorp/FreeOpenData/issues/2
* 6:40PM - 7:14PM: little improvements to copy all socrata data
* 7:22AM - 7:46AM: thinking about what needs to be done for launch, wrote 3 issues

3/19/17

* 9:05PM - 11:45PM: setting up wordpress, ran into redirect issue that stuggled to resolve
* 9:00PM - 9:05PM: made video
* 7:12PM - 7:57PM: add to readme
* 4:55PM - 5:15PM: write down on paper (I need to go paperless just like the government) blog post ideas
* 3:40PM - 4:05PM: tweeting with folks that lead to decision to make detailed log of Socrata to BigQuery ETL and add more info about who competing with and when to readme
* 5:11AM - 6:21AM: debugging script that copies Socrata datasets to BigQuery and sending tweet to BigQuery outreach person
* 3:30AM - 3:51AM: adding income goals to readme
* 1:40AM - 3:30AM: cleaning up mission statement, adding details to readme

3/18/17

* 3:00PM - 5:30PM: writing script to copy all Socrata datasets to BigQuery
* 1:30PM - 3:00PM: preparing to download all Socrata datasets [trying to get google-drive-ocamlfuse working], talking with https://twitter.com/BecomingDataSci about the site, and creating Twitter icon, requested help from google-drive-ocamlfuse author https://github.com/astrada/google-drive-ocamlfuse/issues/276, figured out that I hadn't enabled gdrive api
* 1:08PM - 1:30PM: setting up CloudFlare and Google G Suite 
