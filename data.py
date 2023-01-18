import json
from numpy import unique

# data = []
# with open("links.json", "r") as f:
#     temp = json.load(f)
#     for link in temp:
#         for href in link['link']:
#             data.append(href)
#
# unique(data)
#
# with open(r'out.txt', 'w') as output:
#     for link in data:
#         output.write("%s\n" % link)

# data = []
with open("out.txt", "r") as f:
    temp = f.read()

    data = temp.replace('\n', ' ').split()

    # for t in temp:
    #     data.append(t)

print(len(data))
