PREFIX = '/music/freakonomics'

NAME = 'Freakonomics Radio'
ICON = 'icon-default.png'
ART = 'art-default.jpg'

BASE_URL = 'http://www.freakonomics.com'
PODCASTS_URL = BASE_URL + '/radio/freakonomics-radio-podcast-archive/'

####################################################################################################
def Start():
  
    ObjectContainer.title1 = NAME
    TrackObject.thumb = R(ICON)
    
####################################################################################################
@handler(PREFIX, NAME, ICON, ART)
def Main():
    oc = ObjectContainer()
    data = HTML.ElementFromURL(PODCASTS_URL)
    for podcast in data.xpath('//table[@class="radioarchive"]//tr'):
        try: url = podcast.xpath('.//a')[0].get('href')
        except: continue
        if not url.startswith('http://'):
            url = BASE_URL + url
        ep_num = podcast.xpath('./td')[0].text
        try: ep_title = podcast.xpath('.//span[contains(@class, "title")]/a')[0].text
        except: ep_title = podcast.xpath('.//a/span[contains(@class, "title")]')[0].text
        title = "%s - %s" % (ep_num, ep_title)
        try: summary = podcast.xpath('./td/text()')[1]
        except: summary = ""
        date = podcast.xpath('.//td')[-2].text
        try: date = Datetime.ParseDate(date).date()
        except: date = None
        runtime = podcast.xpath('.//td')[-1].text
        duration = DurationMS(runtime)
        oc.add(TrackObject(url=url, title=title, summary=summary, duration=duration, originally_available_at=date))
    return oc

####################################################################################################
def DurationMS(runtime):
    parts = runtime.split(':')
    duration = (int(parts[0])*60 + int(parts[1]))*1000
    return duration