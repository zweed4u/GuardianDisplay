import sys, json, requests

session=requests.session()

headers={
	'X-API-Key':'GET_FROM_BUNGIE',
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36'
}


username=raw_input("UserName? ")
platform=raw_input("Platform? (1 for Xbox, 2 for Playstation) ")
if int(platform) !=1 and int(platform) !=2:
	print 'Please rerun and enter a valid unput for console.'
	sys.exit()
memberUrl='https://www.bungie.net/platform/destiny/'+platform+'/Stats/GetMembershipIdByDisplayName/'+username

memberId=session.get(memberUrl,headers=headers)

if memberId.json()['Response']=='0':
	print 'ErrorStatus:',memberId.json()['ErrorStatus']
	print 'Message:',memberId.json()['Message']
	print '\nPlease rerun and ensure that your username is entered correctly. (Case-sensitive)'
	sys.exit()
else:
	print 'MemberId:', memberId.json()['Response'],'(',username,')'


accountUrl='http://www.bungie.net/platform/destiny/'+platform+'/Account/'+memberId.json()['Response']+'/'
account=session.get(accountUrl,headers=headers)

print
print 'Grimoire Score:',account.json()['Response']['data']['grimoireScore']
print username,'has',len(account.json()['Response']['data']['characters']),'characters.'
print
print '##########################################################'	
print
for character in account.json()['Response']['data']['characters']:
	if character['characterBase']['raceHash'] == 898834093:
		race='Exo'
	if character['characterBase']['raceHash'] == 3887404748:
		race='Human'
	if character['characterBase']['raceHash'] == 2803282938:
		race='Awoken'
	
	if character['characterBase']['classHash']==3655393761:
		cl='Titan'
	if character['characterBase']['classHash']==671679327:
		cl='Hunter'
	if character['characterBase']['classHash']==2271682572:
		cl='Warlock'
	print cl,'::',race
	print 'Level:',character['characterLevel']
	print 'Light:',character['characterBase']['powerLevel']
	print 'Last Played:',character['characterBase']['dateLastPlayed']
	print 'Minutes Played Last Session:',character['characterBase']['minutesPlayedThisSession']
	print 'Minutes Played with this Character Total:',character['characterBase']['minutesPlayedTotal']
	print
	print 'Gear Equipped...'
	hashes=['SubClass','Helmet','Gauntlets','Chest Armor','Leg Armor','Class Item','Primary','Special','Heavy','Ship','Sparrow','Ghost','Emblem','Armor Shader','Emote','Horn','Artifact']
	count=0
	for item in character['characterBase']['peerView']['equipment']:	
		try:
			itemUrl='http://www.bungie.net/platform/Destiny/Manifest/InventoryItem/'+str(item['itemHash'])
			itemName=session.get(itemUrl,headers=headers)	
			name=itemName.json()['Response']['data']['inventoryItem']['itemName']
			try:			
				descrip=itemName.json()['Response']['data']['inventoryItem']['itemDescription']	
			except:
				#emblem  no description
				descrip='n/a'		
		except:
			name=item['itemHash']
		print hashes[count],'::',name
		if count==5 or count==8 or count==11:
			print
		count+=1
	print
	print '##########################################################'	
	print

	
