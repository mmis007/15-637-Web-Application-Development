from django.shortcuts import render
from django.http import HttpResponse


def calc(request):

	def calculate(opr,a,b):
		if opr == 1:
			return a+b
		elif opr == 2:
			return a-b
		elif opr == 3:
			return a*b
		else:
			if b == 0:
				return 'error'
			else:
				return a//b

	screen=0
	savednum=0
	lastopr=0
	result=0
	status=0
	digit=0
	operator=0

	if 'screen' in request.POST:
		try:screen = int(request.POST['screen'])
		except ValueError:
			if request.POST['screen'] != 'error':
				return render(request,'calc.html',
					{'screen':'error', 'lastopr':0, 'savednum':0, 'status':-1})

	if 'savednum' in request.POST:
		try:savednum = int(request.POST['savednum'])
		except ValueError:
			return render(request,'calc.html',
				{'screen':'error', 'lastopr':0, 'savednum':0, 'status':-1})


	if 'lastopr' in request.POST:
		try:lastopr = int(request.POST['lastopr'])
		except ValueError:
			return render(request,'calc.html',
				{'screen':'error', 'lastopr':0, 'savednum':0, 'status':-1})


	if 'status' in request.POST:
		try:status = int(request.POST['status'])
		except ValueError:
			return render(request,'calc.html',
				{'screen':'error', 'lastopr':0, 'savednum':0, 'status':-1})

	if 'digit' in request.POST:

		try:
			digit = int(request.POST['digit'])
		except ValueError:
			return render(request,'calc.html',
				{'screen':'error', 'lastopr':0, 'savednum':0, 'status':-1})
		else:

			if status == 0:		
				''' the last action was 'digit' '''	
				result = digit+ 10 * screen

			else:
				result = digit	
				status = 0
			
	


	if 'operator' in request.POST:
		
		try:operator = int(request.POST['operator'])
		except ValueError:
			return render(request,'calc.html',
				{'screen':'error', 'lastopr':0, 'savednum':0, 'status':-1})
				
		else:
			if status == -1:
				''' the last action was in error '''
				result = 'error'
				savednum = 0
				lastopr = 0
				status = -1

			elif status == 0:
				''' the last action was 'digit' '''
				if lastopr == 0:
					result = screen
					savednum = screen
					lastopr = operator
					status = 1
					
				else:
					result = calculate(lastopr, savednum, screen)
					lastopr = operator
					
					if result == 'error':
						savednum = 0	
						status = -1				
					else:
						savednum = result
						status = 1
		
			elif status == 1:
				''' the last action was 'operator' '''
				result = screen
				savednum = screen
				lastopr = operator
				status = 1

			else:
				''' the last action was 'equals' '''
				result = screen
				savednum = screen
				lastopr = operator
				status = 1
		


	if 'equals' in request.POST:
		
		if status == -1:
			''' the last action was in error '''
			result = 0
			savednum = 0
			lastopr = 0
			status = 0

		elif status == 0:
			''' the last action was 'digit' '''
			if lastopr > 0:
				
				result = calculate(lastopr, savednum, screen)
				if result == 'error':
					savednum = 0	
					status = -1	
				else:
					lastopr = 0				
					savednum = 0
					status = 2

			else:
				result = screen
				savednum = screen
				status = 2

		else:
			''' the last action was 'operator' '''
			result = screen
			savednum = screen
			status = 2
		

	return render(request,'calc.html',
		{'screen':result, 'lastopr':lastopr, 'savednum':savednum, 'status':status})






