# CoronaHackZurich2020

## Technical
Set these environment variables to work with `azure.py` (values posted in Slack):
- "AZURE_KEY"
- "AZURE_ENDPOINT"

## Pitch
### Inspiration
To find out how the society feels at a certain moment in time is of great interest for many - from policy makers that want to support their people where it matters over social entrepreneurs that want to improve the welfare of the society to reporters that want to cover the most important topics and have a positive impact.
But the usual sources of this emontional data often suffer from being highly biased - it only covers a subset of groups within the society, not at the society as a whole.

The topics that concern society the most and the impact of these topics on people's emotions are often found out from singular and limited sources like the frequency of certain Hashtags on Twitter in a certain timespan.
These data streams are typically dominated by technological knowledgeable, educated, adult men and women.
It is obvious that this is not an accurate cross-section of a society as it does not include children, old people and people that enjoyed less education.
These groups amount much larger numbers of people than the clientele of Twitter and are often affected by entirely different issues.

Another method of sentiment testing is by randomly questioning people in the buzzing downtowns of cities.
But this method also faces the same issue: Only the sentiment of certain groups of people (here the young (physically or mentally), urban upper middle class) is captured. 

Therefore the big challenge is: **How can we find out the accurate state of the emotional well-being of the whole cross-section of society, not only for certain groups?** 

### Our solution

The problem is that using only one data source leads to results that doesn't represent the whole of society well.
We believe that combining several data sources in a proportional manner, each being dominated by certain demographics and groups, can give an accurate view of how the whole of society thinks and feels.

We identified several data sources, each representing a different demographics.
 
Only summary right now, will write full sentences later

- Problem: singular data source -> doesnt reflect whole society very well
- use several (also uncommon) data sources and combine them
- data source:
    - Spotify
    - SwissCom data
    - Twitter
    - Maybe news or something
- Argue that each of these data sources reflect a different group of society (but that very well), and if you do weighted averaging of them in the right fashion (according to the proportions of the corresponding groups in society), you can get a much more accurate scare level than with only news data or whatever

### How we build it

- Use Azure for fancy scientify background analytics stuff ( ;) )
- Server uses the lighweight and efficient Flask
- Twitter API and special data from SwissCom

### Challenges

- Twitter API is a nightmare
- Presentating all the data is a UX challenge which we of course mastered perfectly

### Accomplishment

- coming up with combining different data sources which is a surely innovative and useful method


### Whats next?

- Measure the correct proportions each data source should have
- add more data sources like other social networks (e.g. Instagram)

### Build with

- Python
- Azure (thanks Microsoft)
- Cutting edge web technologies