
import requests
import json

class Message():
	def __init__(self,status,text):
		self.status = status
		self.text = text

class Result:
	m11 = Message("Ok","OK")
	m12 = Message("Ok", "OK => Testing res and ResContent is empty.")
	m21 = Message("Diff", "Diff => Testing res and ResContent is diff.")
	m22 = Message("Diff", "Diff => Testing res is empty and ResContent isn't empty.")
	m23 = Message("Diff", "Diff => Testing res isn't empty and ResContent is empty.")
	m31 = Message("Error", "System respons messge =>")
	


def apiPrint( msg, config, rInstance ):
	if msg:
		print("  {msg}".format(msg=msg.text))
	print("  >> {method} {status} {url}".format(method=config["method"],status=rInstance.status_code,url=rInstance.url))

def errorPrint(msg, rInstance):
	if msg:
		print("  {status} => {msg} {res}".format(status=msg.status,msg=msg.text,res=rInstance.content))

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

def compareObj(a,b):
	if ordered(a) == ordered(b):
		return True
	else:
		return False

def resCompare( res, rInstance ):
	msg = ""
	if res.data and rInstance.content:
		for k in res.ingore:
			del res.data[k]
		if compareObj(res.data, rInstance.json()):
			msg=Result.m11
		else:
			msg=Result.m21
	elif not res.data and not rInstance.content:
		msg=Result.m12
	elif not res.data:
		msg=Result.m22
	elif not rInstance.content:
		msg=Result.m23
	return msg

class TEMPDATA():
	def __init__(self):
		self.data=json.dumps({})
	def setFields(self,obj):
		try:
			self.data=obj
		except Exception as e:
			print("TEMPDATA:error:key:",key)
			print("TEMPDATA:error:",e)
	def getByField(self,key):
		return self.data[key]
	def getData(self):
		return self.data

class API():
	def __init__(self,config):
		self.config = config
	def RUN(self):
		method=self.config["method"]
		if method=="GET":
			self.GET()
		elif method=="POST":
			self.POST()
		elif method=="PUT":
			self.PUT()
		elif method=="DEL":
			self.DEL()
		return self.instance
	def GET(self):
		self.instance=requests.get( self.config["url"], params=self.config["params"], data=self.config["body"], headers=self.config["headers"] )
	def POST(self):
		self.instance=requests.post( self.config["url"], params=self.config["params"], data=self.config["body"], headers=self.config["headers"] )
	def PUT(self):
		self.instance=requests.put( self.config["url"], params=self.config["params"], data=self.config["body"], headers=self.config["headers"] )
	def DEL(self):
		self.instance=requests.delete( self.config["url"], params=self.config["params"], data=self.config["body"], headers=self.config["headers"] )

def flowTest( host, flow ):
	print(" ")

	for index,api in enumerate(flow["list"]):
		req = api["request"]
		res = { "data":api["response"], "ingore":api["resIgnore"] }
		url = host+req["path"]

		for key in api["update"]:
			req["body"][key]=api["update"][key]

		if not req['headers']:
			req['headers']['Content-Type'] = "application/json;charset=UTF-8"
			req["body"] = json.dumps(req["body"])
			print(req["body"])

		config = req
		config["url"] = url

		apiInstance = API(config)
		rInstance = apiInstance.RUN()

		try:
			msg=""
			if rInstance.status_code==200 or rInstance.status_code==201:
					msg = resCompare(res, rInstance)
		except Exception as e:
			print("Response temp data or compare function:error:",e)
	
		apiPrint(msg, req, rInstance)

		if rInstance.status_code!=200 and rInstance.status_code!=201:
			errorPrint(Result.m31, rInstance)
		
		if msg and msg.status=="Diff":
			print("  ---")
			print("  {content}".format(content=rInstance.content))
			print("  {res}".format(res=res))

		print(" ")

	print("\n")

def runTest():
	with open('apis.json' , 'r') as reader:
	    jf = json.loads(reader.read())
	print(" ")
	print("Project:",jf["name"])
	print("HOST:",jf["host"])
	print("\n")
	for flow in jf["flow"]:
		print(" ")
		print("FLOW:",flow["name"])
		flowTest(jf["host"], flow)
	

if __name__ == '__main__':
    runTest()