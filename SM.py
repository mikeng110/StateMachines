from abc import ABCMeta, abstractmethod

#Right now i am not crazy that in order to make verbose we need to redo the algorithm defined in getnextvalues.

class SM(metaclass=ABCMeta):
    def __init__(self):
        pass

    @property
    @abstractmethod
    def startState(self):
        pass

    @abstractmethod
    def getNextValues(self, state, inp):
        pass

    def start(self, verbose=False):
        self.state = self.startState
        if verbose:
            print("Start State: " + str(self.state))

    def step(self, inp, verbose=False):
         (s, o) = self.getNextValues(self.state, inp)

         if verbose:
            print( self.__str__() + " -> " + "In: " + str(inp) + ", Out: " + str(o) + ", Next State: " + str(s))

         self.state = s
         return o

    def transduce(self, inputs, verbose=False):
        self.start(verbose)
        return [self.step(inp, verbose) for inp in inputs]

    def run(self, n=10, verbose=False):
        return self.transduce([None]*n, verbose)

    def __str__(self):
        return self.__class__.__name__ + "(" + str(self.startState) + ")"


class Cascade(SM):

    startState = None

    def __init__(self, m1, m2):
        self.m1 = m1
        self.m2 = m2

        self.m1.start()
        self.m2.start()

        self.startState = (m1.state, m2.state)

    def getNextValues(self, state, inp, verbose=False):
        (s1, o1) = self.m1.getNextValues(state[0], inp)
        (s2, o2) = self.m2.getNextValues(state[1], o1)

        return ((s1, s2), o2)

    def step(self, inp, verbose=False):
        o = None
        newS = None
        if verbose:
            o = self.m1.step(inp, verbose)
            s1 = self.m1.state

            o = self.m2.step(o, verbose)
            s2 = self.m2.state

            newS = (s1, s2)

        else:
            (newS, o) = self.getNextValues(self.state, inp)

        self.state = newS

        return o


class Feedback(SM):
    startState = None

    def __init__(self, sm):
        self.m = sm
        self.m.start()
        self.startState = self.m.startState

    def getNextValues(self, state, inp):
        (ignore, o) = self.m.getNextValues(state, "undefined")
        (newS, ignore) = self.m.getNextValues(state, o)
        return (newS, o)

    def step(self, inp, verbose=False): #Try to redesign so you can make verbose for multible levels without needing a costume step function.
         o = None
         newS = None

         if verbose:
             o = self.m.step("undefined")
             self.m.step(o, verbose)
             newS = self.m.state

         else:
             (newS, o) = self.getNextValues(self.state, inp)

         self.state = newS
         return o

    def transduce(self, inputs, verbose=False):
        self.start(verbose)
        ret = []
        for index, inp in enumerate(inputs, start=0):
            if verbose:
                print("Step: " + str(index))
            ret.append(self.step(inp, verbose))
            if verbose:
                print("\n")

        return ret







