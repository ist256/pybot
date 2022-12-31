import requests
from IPython.core.magic import Magics, magics_class, cell_magic

from coursetools.nbenvironment import NbEnvironment

import settings as settings


def get_notebook_environment():
    nbe_props = NbEnvironment().properties
    skipkeys = ['minio_client', 'settings', 'run_datetime']
    for k in skipkeys:
        del nbe_props[k] 
    return nbe_props

def opt_status(eula=pbs.EULA):
    if not os.path.exists(eula):
        return "new"
    else:
        with open(eula,"r") as f:
            opt = f.read().strip().lower()
            return "in" if opt != 'out' else 'out'

        
@magics_class
class MyMagics(Magics):

    @cell_magic
    def pybot(self, line, cell):
        line = line.strip().lower()
        opt = opt_status()
        if opt=='new' or line in ['opt','help','?']:

            def on_button_optin(b):
                with open(pbs.EULA,"w") as f:
                    f.write("in")
                clear_output()
                display(HTML("You are now opted IN. Run this cell again to use the assistant."))            

            def on_button_optout(b):
                with open(pbs.EULA,"w") as f:
                    f.write("out")
                clear_output()
                display(HTML("You are now opted OUT. Run this cell again to use the assistant."))                            
                
            display(HTML(study_text))
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
        else:  
            # Run the main code 
            lines = "".join(cell)
            nbe_props = get_notebook_environment()
            payload = { "prompt": line, "celldata": lines, "notebook_environment": nbe_props,"opt" : opt }
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
    ip.register_magics(MyMagics)
except NameError:
    pass # Not in a jupyter notebook
