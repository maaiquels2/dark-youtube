import sys; sys.path.insert(0, "."); import app, pipeline
pid = open("fb_id.txt").read().strip(); d = app.load_project(pid); n = len(d["scenes"])
first = {}
for i in range(n): first.setdefault(pipeline.act_of(i, n), i + 1)
C = "Kevin MacLeod (incompetech.com), licensed under Creative Commons: By Attribution 4.0, https://creativecommons.org/licenses/by/4.0/"
d["music_tracks"] = [
 {"file": "music/floating-cities.mp3", "from_scene": first["act1"], "volume": 0.16, "title": "Floating Cities", "act": "act1", "credit": C},
 {"file": "music/investigations.mp3", "from_scene": first["act2"], "volume": 0.17, "title": "Investigations", "act": "act2", "credit": C},
 {"file": "music/darkest-child.mp3", "from_scene": first["act3"], "volume": 0.18, "title": "Darkest Child", "act": "act3", "credit": C},
 {"file": "music/heartbreaking.mp3", "from_scene": first["after"], "volume": 0.15, "title": "Heartbreaking", "act": "after", "credit": C}]
pipeline._save(d); print(first)
