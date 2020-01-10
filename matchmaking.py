def matchmaking(lang_entreprise, lang_worker, sal_entreprise, sal_worker, distance, test):

	compatibilty = 0.0


	positive = 0
#HARD SKILL
#on verifie que les hard skills du user sont les bons
	for e in lang_entreprise:
		for w in lang_worker:
			if e == w:
				positive += 1

#on fait une 1ere modification du taux de compatibilite en fonction des hard skills
	compatibilty = positive/len(lang_entreprise['language']) * 100

#SALAIRE
#on augmente de 10% la compatibilite si les 2 salaires sont proches ou si le salaire demande est moins eleve 
	if sal_worker < sal_entreprise:
		compatibilty *= 1.10

	elif sal_worker > sal_entreprise and sal_worker < sal_entreprise * 1.10:
		compatibilty *= 1.10

#on baisse la compatibilite si les 2 salaires sont distant 
	elif sal_worker > sal_entreprise * 1.10 and sal_worker < sal_entreprise * 1.15:
		compatibilty *= 0.05

	elif sal_worker > sal_entreprise * 1.15 and sal_worker < sal_entreprise * 1.20:
		compatibilty *= 0.10

	elif sal_worker > sal_entreprise * 1.20:
		compatibilty *= 0.20

	if compatibilty > 100:
		compatibilty = 100


#DISTANCE
	km = sum(distance.values())

#si la distance est moins de 2 km la compatibilite augmente de 10%

	if km <= 2.0:
		compatibilty *= 1.10

#sinon elle baisse progressivement
	else:
		compatibilty = (0.01 * km) * compatibilty

	if compatibilty > 100:
		compatibilty = 100

#TEST PERSONNALITE
	test_results = sum(test.values())
#on fait une moyenne des 2 resultats
	compatibilty = (compatibilty + test_results) / 2

return(compatibilty)
