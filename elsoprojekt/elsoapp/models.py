from django.db import models

# Create your models here.


class Tanulo(models.Model):

	nev = models.CharField(max_length=128)
	fnev = models.CharField(max_length=128)
	jelszo = models.CharField(max_length=128)
	email = models.CharField(max_length=128)

	class Meta:
		verbose_name = 'Tanuló'
		verbose_name_plural = 'Tanulók'

	def __str__(self):
		return f"{self.nev} ({self.fnev} - {self.jelszo})"

	def feltoltes():
		with open('tanulo_input.tsv', 'r') as f:
			for t in f.readlines():
				tan = t.split('\t')
				Tanulo.objects.create(nev = tan[0], fnev=tan[1], jelszo = tan[2], email=tan[3])

class Foglalkozas(models.Model):
	nev = models.CharField(max_length=128)
	maxdb = models.IntegerField()
	db = models.IntegerField()
	

	class Meta:
		verbose_name = 'Foglalkozás'
		verbose_name_plural = 'Foglalkozások'

	def __str__(self):
		return f"{self.nev} ({self.db}/{self.maxdb})"
	

class Valasztas(models.Model):
	tanulo = models.ForeignKey(Tanulo, on_delete=models.CASCADE)
	foglalkozas = models.ForeignKey(Foglalkozas, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Választás'
		verbose_name_plural = 'Választások'

	def __str__(self):
		return f"{self.tanulo.nev} -> {self.foglalkozas.nev}"

	def formrol(post):
		print("POST request érkezet!!! :)")
		print(f"A {post['felhasznalonev']} felhasználónevű tanuló a {post['jelszo']} jelszót beírva a {post['valasztas']} foglalkozást választaná")

		tlista = list(Tanulo.objects.filter(fnev=post['felhasznalonev'], jelszo=post['jelszo']))
		if len(tlista)==0:
			print("sikertelen azonosítás!!!!!")
		else:
			fogl = list(Foglalkozas.objects.filter(nev=post['valasztas']))[0]
			Valasztas.objects.create(tanulo=tlista[0], foglalkozas=fogl)




# teendők:
# - Ha sikertelen azonosítás történik, írja ezt ki a felhasználónak!
# - Ha sikeres azonosítás történik, írja ezt ki a felhasználónak!
# - Ne lehessen létszámon felül jelentkezni!
# - Ha már elvitték közben a helyet, írja ezt ki a felhasználónak!
# - Ha sikeres jelentkezés történt, akkor írja ezt ki a felhasználónak!
# - Egy diák ne tudjon két foglalkozásra jelentkezni!
# - Az új jelentkezés írja felül a régit! (hogy ne kelljen jelentkezéstörléssel bajlódni)
# - Ha valaki így tesz, akkor az átjelentkezés tényét írja ki a felhasználónak!
