import sys,time
sys.path.insert(0,'.')
import app
t=time.time()
print(app.gfx_render(open('fb_id.txt').read().strip()),round(time.time()-t),flush=True)
