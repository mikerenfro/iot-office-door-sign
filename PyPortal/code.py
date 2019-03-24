import time
import board
from adafruit_pyportal import PyPortal
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
import json
from secrets import secrets

# Set up where we'll be fetching data from. Presumes a JSON structure of:
# [{"status":"At home",
#   "date":"- Monday, May 1, 9:54 PM",
#   "graph":"https://host/graph.png"}]
DATA_SOURCE = secrets['pyportal_source']

# Status graph details
image_json_path = [0, 'graph']
image_size = (297, 122)
image_position = (11, 0)
image_refresh_time = 3600

# Status text details
font_path = "/fonts/DejaVuSansMono-14.bdf"
text_wrap = 38
line_spacing = 0.75
status_dict = {'status': {'position': (5, 174),
                          'color': 0xffffff,
                          'length': 140,
                          'json_path': [0, 'status'],
                          'format': '{0}'},
               'date': {'position': (5, 230),
                        'color': 0x4f29b4,
                        'length': text_wrap,
                        'json_path': [0, 'date'],
                        'format': '{{0: >{0}}}'.format(text_wrap)}
                        # "monospaced right justify"
              }
status_refresh_time = 30

# Should be no need for modifications past this point.

# Initialize font
big_font = bitmap_font.load_font(font_path)
big_font.load_glyphs(b' ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`1234567890-=~!@#$%^&*()_+[]{},./<>?;:\\|\'"')

# Initialize PyPortal
pyportal = PyPortal(debug=False,
                    url=DATA_SOURCE,
                    image_json_path=image_json_path,
                    image_resize=image_size,
                    image_position=image_position,
                    status_neopixel=board.NEOPIXEL,
                   )

# Initialize status text areas
text_areas = {}
for k, entry in status_dict.items():
    pos = entry['position']
    color = entry['color']
    length = entry['length']
    textarea = Label(big_font, text=length*' ')
    textarea._line_spacing = line_spacing
    textarea.x = pos[0]
    textarea.y = pos[1]
    textarea.color = color
    pyportal.splash.append(textarea)
    text_areas[k] = textarea

# Initialize looping and change conditions
refresh_time = None
raw_status_dict_old = {}

while True:
    # Periodically, sync time and grab a new image
    if (not refresh_time) or (time.monotonic() - refresh_time) > image_refresh_time:
        try:
            print("Getting time from internet")
            pyportal.get_local_time()
            refresh_time = time.monotonic()
            print("Grabbing new image")
            value = pyportal.fetch()
            print("Response is", value)
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
            continue
    # Every time, grab the status JSON and check for changes to text area contents
    try:
        print("Grabbing new status")
        json_file = DATA_SOURCE.split('/')[-1]
        if pyportal._sdcard:
            json_file = '/sd/' + json_file
        pyportal.wget(url=DATA_SOURCE,
                      filename=json_file,
                      chunk_size=512)
        with open(json_file, 'r') as f:
            lines = f.readlines()
        json_str = ' '.join(lines)
        j = json.loads(json_str)
        # Check JSON for changes to text area contents
        raw_status_dict = {}
        for k in status_dict.keys():
            json_path = status_dict[k]['json_path']
            json_traversed = pyportal._json_traverse(j, json_path)
            text = '\n'.join(pyportal.wrap_nicely(json_traversed, text_wrap))
            raw_status_dict[k] = text
        if raw_status_dict == raw_status_dict_old:
            print("No changes in json text")
        else:
            print("At least one thing changed in json text")
        # Update changed text areas
        for k, v in raw_status_dict.items():
            if not(v == raw_status_dict_old.get(k)):
                print("Status item '{0}' changed from '{1}' to '{2}'".format(k, raw_status_dict_old.get(k), v))
                text_areas[k].text = status_dict[k]['format'].format(v)
        # Update status dictionary for next iteration
        raw_status_dict_old = raw_status_dict

    except (RuntimeError, ValueError) as e:
        print("Some error occured, retrying! -", e)
    time.sleep(status_refresh_time)