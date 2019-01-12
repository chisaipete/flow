from bs4 import BeautifulSoup
from inbox import gmail
import time
# from inbox import pocket
# p = pocket.Pocket()
# p.add()
# print(p.archive)

# use a manual export instead
pocket_export = "ril_export.html"
print(f'Reading exported pocket list: {pocket_export}')
with open(pocket_export, encoding='utf8') as pe:
    soup = BeautifulSoup(pe, 'html.parser')

# print(soup.find(id='unread'))

# for entry in soup.find(id='unread').children:
#     print(entry.contents[0].get('href'))

first_h1 = soup.find('h1')
uls = []
for next_sib in first_h1.findNextSiblings():
    if next_sib.name == 'ul':
        uls.append(next_sib)

article_urls = []
archive_urls = []

for li in uls[0].findAll('li'):
    for a in li.findAll('a'):
        article_urls.append(a.get('href'))

for li in uls[1].findAll('li'):
    for a in li.findAll('a'):
        archive_urls.append(a.get('href'))


# print(article_urls)
# m = gmail.Mailbox()
# for url in article_urls:
#     m.send_message(m.create_message('cmpete@gmail.com', 'save@emailthis.me', '', url))

print(archive_urls)
m = gmail.Mailbox()
count = 0
for url in archive_urls:
    print(url)
    m.send_message(m.create_message('cmpete@gmail.com', 'save@emailthis.me', '', url))
    count += 1
    if count == 20:
        count = 0
        print('Sleeping...')
        time.sleep(10)
