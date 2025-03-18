def test_method():
    return "call to test_method"

class TestClass:
    @classmethod
    def classMethode(cls):
        print ("classMethod")

    @classmethod
    def _classMethodeInternal(cls):
        print ("classMethodInternal")
    @staticmethod
    def staticMethode():
        print("staticMethod")
    
    def instanceMethode(self):
        print("instanceMethod")
    def _testInternal(self):
        print ("internal method")
    def testExternal(self):
        print("externalMethod")



class Reverse:
    def __init__(self, data):
        self.data = data
        self.index = len(data)
        
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.index == 0:
                raise StopIteration
            self.index = self.index - 1
        return self.data[self.index]




if __name__ == "__main__":
    print("support library - import only")