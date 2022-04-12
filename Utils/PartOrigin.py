def PartOrigin(PdgId,MomId,MomMomId,lep_id):
	# Origin -1=other, 0=prompt, 1=promptformphot, 2=nonpromtconv, 3=bdfake, 4=fake, 5=nonpromptelectron, 6=nonprompttaus, 7=nonpromptglu, 8=mistaggedglu?
	# Origin -1=other, 0=prompt, 1=bdfake, 2=fake, 3=nonpromptelecton, 4=promptformphot, 5=nonpromptconv
	origin = -1

	test_origin_1 = ( PdgId==22 and (abs(MomId)==11 or abs(MomId)==13 or abs(MomId)==15) )
	test_origin_2 = ( MomId==22 and (abs(MomMomId)==11 or abs(MomMomId)==13 or abs(MomMomId)==15) ) and (PdgId==lep_id)

	n = test_origin_1 + test_origin_2

	if n>=1:
		origin = 2

	else:
		test_origin = ( PdgId==22 and not (abs(MomId)==11 or abs(MomId)==13 or abs(MomId)==15) )

		if test_origin>=1:
			origin = 1

		else:
			test_origin_1 = ( PdgId==23 )
			test_origin_2 = ( ( (MomId==23) or (abs(MomId)==24) or (MomId==25) ) and (PdgId==lep_id) )
			test_origin_3 = ( ( (MomMomId==23) or (abs(MomMomId)==24) or (MomMomId==25) ) and ((PdgId==lep_id) and (MomId==lep_id)))
			test_origin_4 = ( ( (abs(MomId)==999888) or abs(MomMomId)==999888 ) and (PdgId==lep_id) )

			n = test_origin_1 + test_origin_2 + test_origin_3 + test_origin_4

			if n>=1:
				origin = 0

			else:
				test_origin_1 = ((abs(PdgId)>410)and(abs(PdgId)<436))or((abs(PdgId)>10410)and(abs(PdgId)<10433)) or ((abs(PdgId)>20412)and(abs(PdgId)<20434))
				test_origin_2 = ((abs(PdgId)>510)and(abs(PdgId)<546))or((abs(PdgId)>10510)and(abs(PdgId)<10544)) or ((abs(PdgId)>20512)and(abs(PdgId)<20544))
				test_origin_3 = ((abs(MomId)>410)and(abs(MomId)<436))or((abs(MomId)>10410)and(abs(MomId)<10433)) or ((abs(MomId)>20412)and(abs(MomId)<20434))
				test_origin_4 = ((abs(MomId)>510)and(abs(MomId)<546))or((abs(MomId)>10510)and(abs(abs(MomId))<10544)) or ((abs(MomId)>20512)and(abs(MomId)<20544))
				test_origin_5 = ((abs(MomMomId)>410)and(abs(MomMomId)<436))or((abs(MomMomId)>10410)and(abs(MomMomId)<10433)) or ((abs(MomMomId)>20412)and(abs(MomMomId)<20434))
				test_origin_6 = ((abs(MomMomId)>510)and(abs(MomMomId)<546))or((abs(MomMomId)>10510)and(abs(MomMomId)<10544)) or ((abs(MomMomId)>20512)and(abs(MomMomId)<20544))

				n = test_origin_1 + test_origin_2 + test_origin_3 + test_origin_4 + test_origin_5 + test_origin_6

				if n>=1:
					origin = 3

				else:
					test_origin_1 = ((abs(PdgId)<10)or(abs(PdgId)>100))
					test_origin_2 = ((abs(MomId)<10)or(abs(MomId)>100))
					test_origin_3 = ((abs(MomMomId)<10)or(abs(MomMomId)>100))

					n = test_origin_1 + test_origin_2 + test_origin_3

					if n>=1:
						origin = 4

					else:
						test_origin = (abs(PdgId)==11) or abs(MomId)==11 or abs(MomMomId)==11

						if test_origin>=1:
							origin = 5

						else:
							test_origin = (abs(PdgId)==15) or abs(MomId)==15 or abs(MomMomId)==15

							if test_origin>=1:
								origin = 6

							else:
								test_origin = MomId==21 and (abs(MomMomId)==12 or abs(MomMomId)==14 or abs(MomMomId)==16)

								if test_origin>=1:
									origin = 7

								else:
									test_origin = PdgId==21

									if test_origin>=1:
										origin = 8

	return origin
