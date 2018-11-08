import time
import json
from collections import namedtuple

import signal

DUMPSTER = '/var/cache/hubble/status.json'

class HubbleStatusResourceNotFound(Exception):
    pass

class HubbleStatus(object):
    dat = dict()
    class Stat(object):
        def __init__(self):
            self.last_t = self.start = time.time()
            self.count  = 0
            self.ema_dt = None
            self.dur = None
            self.ema_dur = None

        @property
        def dt(self):
            return time.time() - self.last_t

        @property
        def asdict(self):
            r = { 'start': self.start, 'count': self.count, 'dt': self.dt, 'ema_dt': self.ema_dt }
            if self.dur is not None:
                r.update({'dur': self.dur, 'ema_dur': self.ema_dur})
            return r

        def mark(self):
            t = time.time()
            self.count += 1
            dt = self.dt
            self.last_t = t
            self.ema_dt  = dt if self.ema_dt is None else 0.5*self.ema_dt + 0.5*dt

        def fin(self):
            self.dur = self.dt
            self.ema_dur  = self.dur if self.ema_dur is None else 0.5*self.ema_dur + 0.5*self.dur

    @classmethod
    def set_status_dumpster(cls, loc):
        global DUMPSTER
        DUMPSTER = loc

    def __init__(self, namespace, *resources):
        if namespace is None:
            namespace = '_'
        self.namespace = namespace
        if len(resources) == 1 and isinstance(resources[0], (list,tuple,dict)):
            resources = tuple(resources)
        self.resources = [ self._namespaced(x) for x in resources ]
        for r in self.resources:
            self.dat[r] = self.Stat()

    @property
    def stats(self):
        return { x: self.dat[x].asdict for x in self.dat }

    def _namespaced(self, n):
        if self.namespace is None or self.namespace.startswith('_'):
            return n
        if n.startswith(self.namespace + '.'):
            return n
        return self.namespace + '.' + n

    def _checkmark(self, n):
        m = self._namespaced(n)
        if m not in self.resources:
            raise HubbleStatusResourceNotFound('"{}" is not a resource of this HubbleStatus instance')
        return m

    def mark(self, n):
        n = self._checkmark(n)
        self.dat[n].mark()

    def fin(self, n):
        n = self._checkmark(n)
        self.dat[n].fin()

    @property
    def asdict(self):
        return { x: self.dat[x].asdict for x in self.dat }
