from html.parser import HTMLParser

class get_info(HTMLParser):
    def __init__(self):
        super().__init__()
        self.info = []
        self.p = False
        self.pa = False

    def handle_starttag(self, tag, attrs):
        if(tag == 'p'):
            self.p = True

        if(self.p and tag == 'a'):
            self.pa = True
            self.url = attrs[0][1]

    def handle_data(self, data):
        if self.pa:
            self.name = data

    def handle_endtag(self, tag):
        if(self.pa and tag == 'a'):
            self.pa = False
            self.info.append([self.name, self.url])

        if(tag == 'p'):
            self.p = False

file = open('link.html', 'r')
html = file.read()
file.close()

parser = get_info()
parser.feed(html)

file = open('link.txt', 'w')
for [name, url] in parser.info:
    file.write(f'{name},{url}\n')
file.close()
