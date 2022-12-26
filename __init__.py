from IPython.core.magic import Magics, magics_class, cell_magic

@magics_class
class DemoMagics(Magics):

    @cell_magic
    def demo(self, line, cell):
        self.shell.set_next_input(cell, replace=False)
	

try:
    ip = get_ipython()
    ip.register_magics(DemoMagics)
except NameError:
    pass # Not in a jupyter notebook
