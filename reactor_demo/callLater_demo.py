# -*- coding: utf-8 -*-
"""
输出：
Start!
call_later_fun_after_shorter_time is called
call_later_fun_after_longer_time is called
Stop!

twisted里对回调的处理和tornado基本一致
在开始监听时设置此次监听的超时时间t, 当此次监听到达时间t后，此次监听结束
t的值与callLater有关，最终是通过_pendingTimedCalls确定的

class ReactorBase(object):
    def mainLoop(self):
        while self._started:
            try:
                while self._started:
                    # Advance simulation time in delayed event
                    # processors.
                    self.runUntilCurrent()
                    t2 = self.timeout()
                    t = self.running and t2
                    # 开始监听
                    self.doIteration(t)


twisted是如何保证每次设置的超时时间t是最小的回调时间的， 即twisted是如何保证调用的时间顺序的？
如本例，总是call_later_fun_after_shorter_time先调用，call_later_fun_after_longer_time后调用

原因在于_pendingTimedCalls是heap queue，通过代码可知_pendingTimedCalls是通过heapq的方法来push, pop的，
可以查看heapq文档，heap queue可以保证_pendingTimedCalls[0]是最小的时间
The interesting property of a heap is that its smallest element is always the root, heap[0].

    def timeout(self):
        ...
        delay = self._pendingTimedCalls[0].time - self.seconds()
        ...

这块儿的逻辑也是和tornado基本一致的
"""

from twisted.internet import reactor


def call_later_fun_after_longer_time():
    print 'call_later_fun_after_longer_time is called'


def call_later_fun_after_shorter_time():
    print 'call_later_fun_after_shorter_time is called'


reactor.callLater(10, call_later_fun_after_longer_time)
reactor.callLater(5, call_later_fun_after_shorter_time)
reactor.callLater(11, reactor.stop)


print 'Start!'
reactor.run()
print 'Stop!'
