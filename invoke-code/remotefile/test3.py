

class ClassA:
	def test(self):
		print('test func')
	def func2(self,s):
		print(s) 

	int_value = 1


print(__file__,'global func')

def funcA():
	print('funA func')

def funcA(s):
	print(s)	

if __name__ == '__main__':
	print('main func')