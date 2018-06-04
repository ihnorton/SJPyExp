from IPython.kernel.zmq.kernelbase import Kernel
from IPython.kernel.zmq.kernelapp import IPKernelApp
from ipykernel.eventloops import register_integration

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




class MyKernel(Kernel):
  pass

def start():
  kernel = IPKernelApp.instance(kernel_class=MyKernel)
  kernel.initialize()
  kernel.kernel.eventloop = loop_slicer
  kernel.start()
