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

	def azonositas(fn, j):
		return Tanulo.objects.filter(fnev=fn, jelszo=j).count()!=0

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

		uzenetek = []

		if not Tanulo.azonositas(post['felhasznalonev'], post['jelszo']):
			print("sikertelen azonosítás!")
			uzenetek.append("Hibás a felhasználónév vagy a jelszó!")
			return uzenetek

		diak = tlista[0]

		print("sikeres azonosítás.")
		uzenetek.append("Sikeresen azonosítottuk a felhasználót.")

		fogl = list(Foglalkozas.objects.filter(nev=post['valasztas']))[0] # ez a választott foglalkozás
		if	fogl.db <= 0:
			print('jelentkezés sikertelen')
			uzenetek.append('jelentkezés sikertelen, mert közben már elvitték a helyet!')
			return uzenetek

		print('jelentkezés sikeres!')
		uzenetek.append('jelentkezés sikeres!')


		valasztasszures = Valasztas.objects.filter(tanulo=diak)

		if valasztasszures.count()>0:		
			regivalasztasa = list(valasztasszures)[0]
			regivalasztasa.foglalkozas.db+=1
			regivalasztasa.foglalkozas.save()
			regivalasztasa.foglalkozas = fogl
			fogl.db-=1
			fogl.save()
			regivalasztasa.save()
			print("foglalkozás sikeresen módosítva")
			uzenetek.append("foglalkozás sikeresen módosítva")
			return uzenetek

		# sikeres azonosítás, van szabad hely, első választás esetén 
		Valasztas.objects.create(tanulo=diak, foglalkozas=fogl)
		fogl.db-=1
		fogl.save()
		print('első választás rögzítve')
		uzenetek.append("választás rögzítve (első választás, módosítás nem történt)")
		return uzenetek




# teendők:

# - ha az admin site-on keresztül törölnek egy választást, akkor a szabad helyek száma is frissüljön! desktruktorokkal kell játszani majd.
# - Elég lenne egy függvény, ami szinkronizálja a db számokat a választások alapján, és ezt meg lehessen hívni admin site-ról.

