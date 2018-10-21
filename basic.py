
from sys import *
import re

varDict = {}

def openFile(filename):
	file = open(filename,"r").read()
	return file

def lex(fileContent):
	tok = ""
	string = ""
	numbers = ""
	var = ""
	expr = ""
	ifCond= ""
	isString = 0;
	isExpr = 0;
	isVar = 0;
	isRightValue = 0;
	isPrinting = 0;
	isRightVarFlag = 0;
	ifControl = 0;

	tokens = []
	chars = list(fileContent)
	ifList = []
	ifCount = 0

	for c in chars:
		if(c == "\n"):
			if(numbers != "" and isExpr == 0):
				if(var != ""):
					tokens.append("VAR:"+var)
				if(len(re.findall(r"[/,*,-,+,%,.,(,),0-9,=,\"]",numbers))==0):
					tokens.append("VAR:"+numbers)
				else:
					tokens.append("NUM:"+numbers)
			elif(expr != ""):
				if(var != ""):
					tokens.append("VAR:"+var)
				tokens.append("EXPR:"+expr)
			elif(string !=""):
				if(var !=""):
					tokens.append("VAR:"+var)
				tokens.append("STRING:"+string.replace("\"",""))
			elif(ifControl == 1):
				tokens.append("COND:"+ifCond)
			elif(var != ""):
				tokens.append("VAR:"+var)
			numbers = ""
			string = ""
			expr = ""
			var = ""
			tok = ""
			ifCond = ""
			isExpr = 0
			isVar = 0
			isString = 0
			isRightValue = 0
			isRightVarFlag = 0
			ifControl = 0
			isPrinting = 0
		elif(c == " " and isString == 0):
			if(tok == "PRINT"):
				tokens.append("PRINT")
				isPrinting = 1
			elif(tok == "IF"):
				ifCount += 1
				ifList.append(str(ifCount))
				tokens.append("IF:"+str(ifCount))
				ifControl = 1
			elif(tok == "INPUT"):
				tokens.append("INPUT")
			elif(tok == "END"):
				tokens.append("END:"+ifList.pop())
			tok = ""
		elif(ifControl == 1):
			ifCond += c
		elif(c == "$" and isRightValue == 0 and isPrinting == 0):
			isVar = 1
		elif(c == "$" and isRightValue == 0 and isPrinting == 1):
			if(expr!=""):
				expr += c
			else:
				numbers += c
			isRightVarFlag = 1
		elif(isVar == 1):
			if(c != "="):
				var += c
			else:
				isVar = 0;
				isRightValue = 1;
		elif(c in "+-/*%()" and isExpr == 0 and isString == 0):
			expr += numbers+c
			isExpr = 1
			isRightVarFlag = 0
		elif isExpr == 1:
			expr += c
		elif((c in "1234567890." and isString == 0) or (isRightValue == 1 and c!="\"" and isString == 0) or isRightVarFlag == 1):
			numbers += c
		elif(c == "\"" and isString == 0):
			isString = 1
		elif(isString == 1):
			string += c
		else:
			tok += c
	# print(tokens)
	# print(varDict)
	return tokens


def calculateExpr(data):
	list = re.findall(r"[a-z,A-Z,_]",data)
	for x in list:
		data = data.replace("$"+x,varDict[x])
	return eval(data)

def checkCondition(cond):
	side = -1
	leftSide = ""
	rightSide = ""
	op = ""
	for x in list(cond):
		if(side == -1 and x not in "<>="):
			leftSide += x
		elif(x in "<>="):
			op += x
			side = 1
		elif(side == 1):
			rightSide += x

	if(op == ">"):
		return (calculateExpr(leftSide) > calculateExpr(rightSide))
	elif(op == "<"):
		return (calculateExpr(leftSide) < calculateExpr(rightSide))
	elif(op == "="):
		if("\"" in leftSide and "\"" in rightSide):
			return (leftSide == rightSide)
		else:
			return (calculateExpr(leftSide) == calculateExpr(rightSide))
	elif(op == "=<"):
		return (calculateExpr(leftSide) <= calculateExpr(rightSide))
	elif(op == ">="):
		return (calculateExpr(leftSide) >= calculateExpr(rightSide))



def parse(data):
	i = 0
	ifList = []
	while i < len(data):
		if(data[i] == "PRINT"):
			dataType = data[i+1].split(":")[0]
			value = data[i+1].split(":")[1]
			if( dataType == "STRING"):
				print(value)
			elif(dataType == "EXPR"  or dataType == "NUM"):
				print(calculateExpr(value))
			elif(dataType == "VAR"):
				print(varDict[value.replace("$","")])
			i += 2

		elif("VAR:" in data[i]):
			varName = data[i].split(":")[1]
			value = data[i+1].split(":")[1]
			varType = data[i+1].split(":")[0]
			if(varType == "STRING"):
				varDict[varName] = value
			else:
				varDict[varName] = str(calculateExpr(value))
			i += 2

		elif(data[i] == "INPUT"):
			if("VAR:" in data[i+1] and "STRING:" not in data[i+2]):
				inputVar = data[i+1].split(":")[1]
				varDict[inputVar] = input()
				i += 2
			else:
				inputString = data[i+2]
				inputVar = data[i+1].split(":")[1]
				varDict[inputVar] = input(inputString.replace("STRING:",""))
				i += 3

		elif("IF" in data[i]):
			ifNo = data[i].split(":")[1]
			cond = data[i+1].split(":")[1]
			if(checkCondition(cond)):
				i += 2
			else:
				i += 2
				count = 1
				for x in data[i:len(data)]:
					if("END" in x and x.split(":")[1] == ifNo):
						break
					count += 1
				i += count
				count = 0

		elif("END" in data[i]):
			i += 1


def run():
	file = openFile(argv[1])
	tokens = lex(file)
	parse(tokens)
	# print(varDict)

run()

