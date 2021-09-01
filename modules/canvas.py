#import pytz
#from icalendar import Calendar, Event
#import datetime
#from pytz import UTC # timezone
import atoma, requests, html, re, discord

def get_info():
    url = 'https://wabash.instructure.com/feeds/announcements/enrollment_h2D75q7ntULGtkEQa5YTAbVpd4c1YFVBIxkk9v6V.atom'
    response = requests.get(url)
    feed = atoma.parse_atom_bytes(response.content)
    entry = feed.entries[0]

    title = entry.title.value
    author = entry.authors[0].name
    content_with_tags = entry.content.value
    content = remove_html_tags(content_with_tags)
    date = entry.published

    return date, author, title, content

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).replace('&nbsp;','')

def get_embed():
        # loads in the data
        date, author, title, content = get_info()

        # define the embed
        embed = discord.Embed(title=f'{title}',description = content,color=discord.Color.green())
        embed.set_author(name = author)

        return embed