# Automatically mark some items as read in Nextcloud News

Some news feeds are very interesting, but sometimes also contain advertisements or simply uninteresting articles.
Of course you can ignore them, but with this small script you also can set up rules which mark these items as read
so you don't see them at all.

## Get started

You can clone this repository or simply download `main.py` and `config-example.ini`. To run the script
you'll need Python 3 installed.

## Configuration

All configuration is read from the file `config.ini` which is expected next to the script.
You can copy the file named `config-example.ini` to `config.ini` to get started.

This makes use of the [Nextcloud News API](https://nextcloud.github.io/news/api/api-v1-3/)
which requires authentication, so you need to supply your username and password - and of course the address
of your Nextcloud installation. Put these into the section `[login]`.

### Filters

Each filter has a name (or title) you can define as you like. It's enclosed in brackets `[...]`.

You can add one or more of the following criteria. *Beware: If you don't add any attribute, then your filter
will match all items!*

* `feedId`: Apply the filter only on one specific feed. You can find out the number you should enter here
  by hovering your mouse over the feed name in the sidebar in Nextcloud News. The URL shown at the bottom of you screen
  ends in the right number, e.g. `.../items/feeds/32/` - here, the feed ID is 32.
* `titleRegex`: Check if some part of the item title matches this regular expression (case-insensitively).
* `bodyRegex`: Check if some part of the item body matches this regular expression (case-insensitively).
* `hoursAge`: Match items older than this (`pubDate` is checked, not `updatedDate` or `lastModified`).

If you define them, these criteria *all* have to match (in one filter) for the checked item to be marked as read, 
they are *and*-joined. So the less criteria you specify (per filter), the broader the matched portion of feed items
should be.

If you need help with regular expressions, you can e.g. look 
[here](https://docs.python.org/3/library/re.html#regular-expression-syntax).

## When and how to run

This script can be run in conjunction with Nextcloud's normal cron hook, e.g. like this:

```
*/5 * * * * /usr/bin/php -f /path/to/nextcloud/cron.php ; ( /path/to/nextcloud-news-filter/main.py | grep -E '(filter|marking as read)' >>/path/to/nextcloud-news-filter.log )
```

The part up to the semicolon was there before, only the latter part was appended when installing this script.

Note: You should make sure that the user executing this (probably `www-data` or something similar) has the rights
(1.) to execute the script and (2.) to write to the indicated log file.

## Communication

If you find a bug or want a new feature, you are welcome to file an issue on Github or even fix things yourself
and create a pull request. You can also [write me an email](https://zephyrsoft.org/contact-about-me)
and I'll see what I can do.

## License

This work is licensed under the GNU General Public License (GPL), Version 3.
