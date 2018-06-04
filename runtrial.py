
from jupyter_client import MultiKernelManager
mkm = MultiKernelManager()
mkm.start_kernel(kernel_id=88472)
import notebook.notebookapp as nbapp

app = nbapp.NotebookApp(kernel_manager=mkm, kernel_id=88472)
app.launch_instance() # this launches a notebook, but the kernel manager is not actually passed down in the constructor

app.kernel_manager = mkm
app.launch_instance() # no effect. need to 
