from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.display import display, HTML, clear_output
import ipywidgets
import os
import requests
from coursetools.nbenvironment import NbEnvironment
import pybot.settings as settings

@magics_class
class PybotMagics(Magics):

    def get_notebook_environment(self):
        nbe_props = NbEnvironment().properties
        skipkeys = ['minio_client', 'settings', 'run_datetime']
        for k in skipkeys:
            del nbe_props[k] 
        return nbe_props

    def opt_status(self, eula=settings.EULA):
        if not os.path.exists(eula):
            return "new"
        else:
            with open(eula,"r") as f:
                opt = f.read().strip().lower()
                return "in" if opt != 'out' else 'out'
    
    @cell_magic
    def pybot(self, line, cell):
        prompt = line.strip().lower()
        opt = self.opt_status()
        if opt=='new' or prompt in ['opt','opt in','opt out']:

            def on_button_optin(b):
                with open(settings.EULA,"w") as f:
                    f.write("in")
                clear_output()
                display(HTML("You are now opted IN. Run this cell again to use the assistant."))            

            def on_button_optout(b):
                with open(settings.EULA,"w") as f:
                    f.write("out")
                clear_output()
                display(HTML("You are now opted OUT. Run this cell again to use the assistant."))                            
                
            display(HTML(settings.STUDY_TEXT))
            if opt == 'in':
                display(HTML("<p>At present, you have opted IN.<p>"))
            elif opt=='out':
                display(HTML("<p>At present, you have opted OUT.<p>"))
            else:
                display(HTML("<p>At present, you have not opted in or out.<p>"))
                                
            button_optin = ipywidgets.Button(description="Opt In", icon='fa-check')
            button_optout = ipywidgets.Button(description="Opt Out", icon='fa-close')
            display(ipywidgets.HBox([button_optin, button_optout]))            
            button_optin.on_click(on_button_optin)
            button_optout.on_click(on_button_optout)
        elif prompt in ["version", "ver", "about"]:
            response = requests.get(settings.PYBOT_URL)
            response.raise_for_status()
            output = response.text
            display(HTML(f"<code>{output}</code>"))
        elif prompt in ["prompts", "help", "?" ]:
            display("TODO: get all working prompts")
        else:  
            # Run the main code 
            lines = "".join(cell)
            nbe_props = self.get_notebook_environment()
            payload = { "prompt": prompt, "celldata": lines, "notebook_environment": nbe_props,"opt" : opt }
            headers = { 'accept' : 'application/json', 'X-Api-Key': settings.API_KEY, 'Content-Type' : 'application/json' }
            response = requests.post(settings.PYBOT_URL, headers=headers, json = payload)
            response.raise_for_status()
            output = response.text
            self.shell.set_next_input(output, replace=False)
               
    @cell_magic
    def demo(self, line, cell):
        self.shell.set_next_input(cell, replace=False)

        
try:
    ip = get_ipython()
    ip.register_magics(PybotMagics)
except NameError:
    pass # Not in a jupyter notebook
