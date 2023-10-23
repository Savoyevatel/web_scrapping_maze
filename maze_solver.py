from bs4 import BeautifulSoup
from splinter import Browser
from selenium.webdriver.common.keys import Keys
import time

browser = Browser("chrome")

browser.visit('https://www.the-art-of-web.com/javascript/maze-game/')
elements = browser.find_by_id("maze")
html_content = elements.html
soup = BeautifulSoup(html_content, 'html.parser')

div_elements = soup.find_all('div')
class_names = [element.get('class') for element in div_elements]

cleaned_class_names = [' '.join(names) if names else '' for names in class_names]
cleaned_class_names = [item for index, item in enumerate(cleaned_class_names, 0) if index % 34 != 0]
class_33 = [cleaned_class_names[i:i+33] for i in range(0,len(cleaned_class_names),33)]
LUT = {
    'wall': 'W',
    'nubbin': 'N',
    'nubbin wall': 'W',
    'wall sentinel': 'S',
    'door': '.',
    'key': 'K',
    'door entrance hero': 'H',
    'door entrance': 'W',
    'hero': 'H',
    'door exit': 'E',
    'nubbin wall wall': 'W'
}

maze = [[LUT.get(cell, cell) for cell in row] for row in class_33]

positions = {'H': None, 'K': None, 'E': None}

for symbol in positions.keys():
    for i, row in enumerate(maze):
        if symbol in row:
            positions[symbol] = (i, row.index(symbol))
            break

coordinates = []
print("Positions:")
for symbol, position in positions.items():
    coordinates.append(position)
    print(f"{symbol}: {position}")

to_int = {
    'W': '1',
    'N': '0',
    'S': '1',
    '.': '0',
    '': '0',
    'K': '0',
    'H': '0',
    'E': '0',
}

maze = [[to_int.get(cell, cell) for cell in row] for row in maze]
maze = [[int(x) for x in i] for i in maze]

def find_path(maze, start, end):
    m = [[0] * len(maze[0]) for _ in range(len(maze))]
    i, j = start
    m[i][j] = 1

    def step_hero(k):
        for i in range(len(m)):
            for j in range(len(m[i])):
                if m[i][j] == k:
                    neighbors = [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]
                    for x, y in neighbors:
                        if 0 <= x < len(m) and 0 <= y < len(m[i]) and m[x][y] == 0 and maze[x][y] == 0:
                            m[x][y] = k + 1
    k = 0
    while m[end[0]][end[1]] == 0:
        k += 1
        step_hero(k)

    i, j = end
    k = m[i][j]
    path = [(i, j)]
    while k > 1:
        neighbors = [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]
        for x, y in neighbors:
            if 0 <= x < len(m) and 0 <= y < len(m[i]) and m[x][y] == k - 1:
                i, j = x, y
                path.append((i, j))
                k -= 1
    return path


path_to_key = find_path(maze, coordinates[1], coordinates[0])
path_to_exit = find_path(maze, coordinates[2], coordinates[1])


def make_movement(browser, move):
    if move == 'up':
        browser.type('words', Keys.ARROW_UP)
    elif move == 'down':
        browser.type('words', Keys.ARROW_DOWN)
    elif move == 'left':
        browser.type('words', Keys.ARROW_LEFT)
    elif move == 'right':
        browser.type('words', Keys.ARROW_RIGHT)


movements = ['up', 'down', 'left', 'right']

for lst in [path_to_key, path_to_exit]:
    for i in range(len(lst) - 1):
        w, x = lst[i]
        y, z = lst[i + 1]

        if w > y:
            make_movement(browser, movements[0])
        elif w < y:
            make_movement(browser, movements[1])
        elif x > z:
            make_movement(browser, movements[2])
        elif x < z:
            make_movement(browser, movements[3])

time.sleep(10)

browser.quit()
