# An Internet of Things Office Door Sign using Adafruit's PyPortal

## Motivation

My previous job was research and development engineer for a university.
That meant I spent a fair amount of time outside my office (across multiple buildings), and students, faculty, or staff would not know where I was, or when I was returning.
Even if I left sticky notes on my door, it was pretty likely I'd get pulled from one location to another before I could return to my office and update the sticky notes.

So I mounted a [Chumby](http://wiki.chumby.com/index.php?title=Main_Page#Chumby_devices) to the window in my office door, and connected its RSS reader app to a feed I could update remotely.
It was a little bit hacky, as I had to cycle the Chumby display between the RSS feed and a clock to ensure the feed display was up to date.
When the Chumby service was being discontinued, I had to migrate to booting an alternative firmware from a flash drive.

After I changed jobs to high performance computing systems administrator for the university, I don't get summoned across buildings as often, but it still happens, and now I have some graphs of HPC usage I'd like to publicize to passersby.
So the Chumby was modified to alternate between displaying a PNG of my HPC's usage and displaying my RSS feed.

And then, my Chumby died sometime last year.
So it was finally time to explore other options, and the [PyPortal](https://www.adafruit.com/product/4116) had just launched.
The cost of a Raspberry Pi and an LCD was more than I wanted to spend initially, and would have been bulkier.

## Prerequisites

- Adafruit PyPortal (SD card is technically optional, but I've not tested without one)
- Web server that can run cron jobs using Python 2 (Python 3 may work, but is untested)
- Web browser (phone or otherwise)
- Twitter account dedicated to the sign status messages

## Web Front End

In the `frontend/door.html`, you can find shortcuts the main user-facing interface with shortcuts to status messages.
By default, I group these shortcut messages by those frequently-used, by building (and floor), and by return times.
On mobile devices, this uses the venerable (and not recently updated) [iUI web framework](http://www.iui-js.org).

![iOS front end view]

On desktops, this uses some basic CSS to add compact the lists of shortcuts, and to add whitespace around the shortcut groups.

![Desktop front end view]

Upon clicking one of the status entry links, you'll be directed to the Twitter app (if installed), or the Twitter web interface.
Click the Tweet button to post the status message.
The message will automatically have the current millisecond value appended in braces.
This is to avoid a Twitter anti-spam measure for posting the same message too often (in case I had to update my sign from "In office" to "Back at X" to "In office" very quickly if my plans changed).
The back end Python script will remove the braces and the millisecond value before posting to the feed.

![Twitter view on phone]

## Server Back End

### Publishing an Image

My default image is a small overview of my HPC's load for the last 7 days, generated by [Ganglia](http://ganglia.sourceforge.net).
Each pixel of width in the image roughly corresponds to 1 hour of time, so I grab the most recent 7 days of data at the top of each hour.

![Ganglia sample image]

The cron job for saving that image looks like:

    0 * * * * wget 'https://host/ganglia/graph.php?c=ITS\%20HPC&m=load_one&r=week&g=load_report&z=small' -O /path/to/load.png -o /dev/null)"

Note that any `%` signs in `wget`'s URL need to be escaped with a `\`, otherwise [cron will assume the `%` sign represents a newline](https://serverfault.com/questions/274475/escaping-double-quotes-and-percent-signs-in-cron).

### Reformatting a Twitter Feed into JSON Elements

From the `backend directory`, edit `twitter-feed-to-json.ini` to use the correct Twitter API credentials and URL to the image.
`twitter-feed-to-json.py` requires the [Twitter module from PyPi](https://pypi.org/project/twitter/), and you'll need to perform the OAuth dance on the script's first run to authenticate it to Twitter.

The cron job for creating the JSON looks like:

    * * * * * bash -c "(cd /path/to/folder/ && ./twitter-feed-to-json.py )"

and the resulting JSON looks like:

    [{"status":"Back at 9:00 AM", "date":"- Sunday, March 24, 4:32 PM", "graph":"https://host/path/to/load.png"}]

## PyPortal

From the `PyPortal` directory, copy the `code.py` and `fonts/DejaVuSansMono-14.bdf` files to the `CIRCUITPY` drive.
Edit `secrets.py` to add a `pyportal_source` key to the `secrets` dictionary, pointing to the JSON URL on your web server.
Edit `code.py` to your desired image size, image position, text appearance, JSON traversal paths, and refresh times (for both the image and text).

When completed and running, the default settings with a small Ganglia graph look like the photo below.

![Door sign]

[Ganglia sample image]: ganglia-week.png
[iOS front end view]: web-sample-phone.png
[Desktop front end view]: web-sample-desktop.png
[Twitter view on phone]: twitter-phone.jpg
[Door sign]: door-sign.jpg
