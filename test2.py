from ipykernel.eventloops import register_integration
import qt
  
@register_integration('slicer')
def loop_slicer(kernel):
    """Start a kernel with the Slicer event loop."""

    poll_interval = int(1000*kernel._poll_interval)
    
    class Timer(object):
        def __init__(self, func):
            print "init..."
            self.timer = qt.QTimer()
            self.app = slicer.app 
            self.func = func

        def on_timer(self):
            self.timer.start(poll_interval)
            self.func()

        def start(self):
            print "starting..."
            self.on_timer()

    kernel.timer = Timer(kernel.do_one_iteration)
    kernel.timer.start()

#-----------------------------------------------------------------------------
# Code from ipykernel
#-----------------------------------------------------------------------------

import sys

from IPython.utils.frame import extract_module_locals
from ipykernel.kernelapp import IPKernelApp
import ipykernel.eventloops
def embed_kernel(module=None, local_ns=None, **kwargs):
    """Embed and start an IPython kernel in a given scope.

    Parameters
    ----------
    module : ModuleType, optional
        The module to load into IPython globals (default: caller)
    local_ns : dict, optional
        The namespace to load into IPython user namespace (default: caller)

    kwargs : various, optional
        Further keyword args are relayed to the IPKernelApp constructor,
        allowing configuration of the Kernel.  Will only have an effect
        on the first embed_kernel call for a given process.

    """
    # get the app if it exists, or set it up if it doesn't
    if IPKernelApp.initialized():
        app = IPKernelApp.instance()
    else:
        print "app"
        app = IPKernelApp.instance(**kwargs)
        #app.initialize([])
        # Undo unnecessary sys module mangling from init_sys_modules.
        # This would not be necessary if we could prevent it
        # in the first place by using a different InteractiveShell
        # subclass, as in the regular embed case.

    # load the calling scope if not given
    (caller_module, caller_locals) = extract_module_locals(1)
    if module is None:
        module = caller_module
    if local_ns is None:
        local_ns = caller_locals

    print "eventloops.enable_gui"
    #ipykernel.eventloops.enable_gui('slicer', kernel=app.kernel)
    loop_slicer(app.kernel)
    print "initi"
    app.initialize(['python', '--gui=slicer'])
    app.kernel.user_module = module
    app.kernel.user_ns = local_ns
    app.shell.set_completer_frame()
    #loop_slicer(app.kernel)

    main = app.kernel.shell._orig_sys_modules_main_mod
    if main is not None:
        sys.modules[app.kernel.shell._orig_sys_modules_main_name] = main

    print "app.start"
    app.start()
    return app
