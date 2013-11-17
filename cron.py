import datetime
import json
import re
import sys
import time
import urllib
import urllib2
import summarize as sz
import re

import constants


def get_twfy_birthday(mp_extra_info):
    sys.stdout.write('.')
    sys.stdout.flush()
    try:
        dob_tuple = time.strptime(mp_extra_info["date_of_birth"], '%Y-%m-%d')
        dob = datetime.datetime(*dob_tuple[:3])
        return mp_extra_info["date_of_birth"]
    except (ValueError, KeyError):
        pass
    return None


def get_wiki_birthday(mp_extra_info):
    try:
        wiki_url = mp_extra_info['wikipedia_url']
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        infile = opener.open(wiki_url)
        page = infile.read()
        
        m = re.search('<td.*?Date of birth</td>\n<td>(.*?)</td>', page)
        dob_str = m.group(1)
        dob_tuple = time.strptime(dob_str, "%d %B %Y")
        dob = dob_str
        return dob
    except (ValueError, KeyError, AttributeError):
        pass
    return None


MAX_LEN = 1000


def mp_sz(wiki_url):
    def strip_wiki_extras(sent):
        return re.sub("(\s\(born.*?\d{4}\))|(\[.*?\])|(^\s)", "", sent)

    def abridge(sent):
        i = MAX_LEN
        while i < len(sent):
            if sent[i] == " ":
                return sent[:(i + 1)] + "..."
            i += 1
        return sent

    sum_arr = sz.summarize_page(wiki_url).summaries
    sum_clean_arr = [strip_wiki_extras(s) for s in sum_arr]
    summary = " ".join(sum_clean_arr)
    if len(summary) > MAX_LEN:
        summary = abridge(summary)
    return summary


url = urllib2.urlopen("http://www.theyworkforyou.com/api/getMPs?" + urllib.urlencode({
    "key": constants.TWFY_API_KEY,
}))

all_members = json.loads(url.read().decode("latin-1").encode("utf-8"))

# make a list of all the MP IDs
all_ids = [x['person_id'] for x in all_members]

# make a comma separated list of all the MP IDs
all_ids_str = ','.join(all_ids)

# get a big json object of all the extra MP info!
url = "http://www.theyworkforyou.com/api/getMPsInfo?" + urllib.urlencode({
    "key": constants.TWFY_API_KEY,
    "id": all_ids_str,
})
url_data = urllib2.urlopen(url)
all_mp_extra_info = json.loads(url_data.read().decode("latin-1").encode("utf-8"))

all_data = [
    {
        'twfy_id': x['person_id'],
        'name': x['name'],
        'interests': all_mp_extra_info[x['person_id']].get('wrans_subjects', None),
        'twfy_dob': get_twfy_birthday(all_mp_extra_info[x['person_id']]),
        'wiki_dob': get_wiki_birthday(all_mp_extra_info[x['person_id']]),
        'wiki_url': all_mp_extra_info[x['person_id']].get('wikipedia_url', None)
    } for x in all_members
]

with open('data%s.json' % datetime.datetime.now().isoformat().replace(":", "."), 'w') as outfile:
    json.dump(all_data, outfile)
