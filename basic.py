
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
	isString = 0;
	isExpr = 0;
	isVar = 0;
	isRightValue = 0;
	isPrinting = 0;
	isRightFlag = 0;

	tokens = []
	chars = list(fileContent)

	for c in chars:
		if(c == "\n"):
			if(numbers != "" and isExpr == 0):
				if(var != ""):
					tokens.append("VAR:"+var)
				tokens.append("NUM:"+numbers)
			elif(expr != ""):
				if(var != ""):
					tokens.append("VAR:"+var)
				tokens.append("EXPR:"+expr)
			elif(var != ""):
				tokens.append("VAR:"+var)
			numbers = ""
			expr = ""
			var = ""
			tok = ""
			isExpr = 0
			isVar = 0
			isRightValue = 0
			isRightFlag = 0
		elif(c == " " and isString == 0):
			if(tok == "PRINT"):
				tokens.append("PRINT")
				isPrinting = 1
			elif(tok == "INPUT"):
				tokens.append("INPUT")
			tok = ""

		elif(c == "$" and isRightValue == 0 and isPrinting == 0):
			isVar = 1
		elif(c == "$" and isRightValue == 0 and isPrinting == 1):
			if(expr!=""):
				expr += c
			else:
				numbers += c
				isRightFlag = 1
		elif(isVar == 1):
			if(c != "="):
				var += c
			else:
				isVar = 0;
				isRightValue = 1;
		elif(c in "+-/*()" and isExpr == 0):
			expr += numbers+c
			isExpr = 1
			isRightFlag == 0
		elif isExpr == 1:
			expr += c
		elif((c in "1234567890."and isString == 0) or isRightValue == 1 or isRightFlag == 1):
			numbers += c
		elif(c == "\"" and isString == 0):
			isString = 1
		elif(c == "\"" and isString == 1):
			isString = 0
			tokens.append("STRING:"+string)
			string = ""
		elif(isString == 1):
			string += c
		else:
			tok += c
	print(tokens)
	# print(varDict)
	return tokens


def calculateExpr(data):
	list = re.findall(r"[a-z,A-Z,_]",data)
	for x in list:
		data = data.replace("$"+x,varDict[x])
	return eval(data)


def parse(data):
	i = 0
	while i < len(data):
		if(data[i] == "PRINT"):
			dataType = data[i+1].split(":")[0]
			value = data[i+1].split(":")[1]
			if( dataType == "STRING"):
				print(value)
			elif(dataType == "EXPR"  or dataType == "NUM"):
				print(calculateExpr(value))
			elif(dataType == "VAR"):
				print(varDict[value])
			i += 2

		elif("VAR:" in data[i]):
			varName = data[i].split(":")[1]
			value = data[i+1].split(":")[1]
			varDict[varName] = str(calculateExpr(value))
			i += 2

		elif(data[i] == "INPUT"):
			if("VAR:" in data[i+1]):
				inputVar = data[i+1].split(":")[1]
				varDict[inputVar] = input()
				i += 2
			else:
				inputString = data[i+1]
				inputVar = data[i+2].split(":")[1]
				varDict[inputVar] = input(inputString.replace("STRING:",""))
				i += 3


def run():
	file = openFile(argv[1])
	tokens = lex(file)
	parse(tokens)
	# print(varDict)

run()
	