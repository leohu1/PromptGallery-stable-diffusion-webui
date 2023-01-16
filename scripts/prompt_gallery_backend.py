import gradio as gr
from modules import shared, scripts
from modules import script_callbacks
from typing import List, Optional, Tuple
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from modules import shared

# pg_ip = "127.0.0.1"
#pg_ip = "127.0.0.1" if shared.cmd_opts.listen else 'localhost'
# pg_port = 5173



# def on_ui_settings():
#     global pg_ip
   
#     with open("./extensions/prompt_gallery_name.json") as fd:
#         name = json.load(fd)['name']
#     os.chmod('./extensions/'+name, stat.S_IRWXO)
#     app = FastAPI()
#     app.mount('/', StaticFiles(directory='./extensions/'+name,html=True))
#     config = Config(app=app,  host=pg_ip,port=pg_port, log_level="info", loop="asyncio", limit_max_requests=1)
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=["*"], 
#         allow_credentials=True, 
#         allow_methods=["*"], 
#         allow_headers=["*"]  
#     )

#     thread = threading.Thread(target= uvicorn.run, kwargs={'app':app, 'host': pg_ip, 'port':pg_port})
#     thread.start()

#     wait_time = 0
#     if_connect =False

#     while if_connect == False and wait_time<=6:
#         try:
#             tmp = requests.get("http://{}:{}".format(pg_ip, str(pg_port)))
#             if_connect = True if int(tmp.status_code) /100 == 2. or int(tmp.status_code) /100 == 2 else False
#         except:
#             print(".")
#             time.sleep(1)
#             wait_time+=1

extension_dir = scripts.basedir()


def on_app_started(demo: Optional[gr.Blocks], app: FastAPI):
    app.mount('/prompt_gallery', StaticFiles(directory=extension_dir,html=True))


def on_ui_tabs():
    if  shared.cmd_opts.theme is None or shared.cmd_opts.theme != 'dark':
        extension_theme = 'white'
    else:
        extension_theme = 'black'
    remote_webui = '127.0.0.1'
    if  shared.cmd_opts.server_name:
        remote_webui = str(shared.cmd_opts.server_name)
    port = str(shared.cmd_opts.port) if shared.cmd_opts.port is not None else "7860"
    
    html = f"""<script>var ip = window.location.hostname;</script>
    <iframe id="tab_iframe" allow="clipboard-read; clipboard-write" 
    style="width: 100%; min-height: 1080px; padding: 0;margin: 0;border: none;" 
    src="/prompt_gallery/?theme={extension_theme:s}&port={port:s}&ip={remote_webui:s}" 
    frameborder="0" marginwidth="0" marginheight="0"></iframe>"""
    with gr.Blocks(analytics_enabled=False, elem_id="prompt_gallery") as prompt_gallery:
        prompt_gallery = gr.HTML(html)
    
    return (prompt_gallery , "Prompt Gallery", "prompt_gallery"),

script_callbacks.on_ui_tabs(on_ui_tabs)

script_callbacks.on_app_started(on_app_started)