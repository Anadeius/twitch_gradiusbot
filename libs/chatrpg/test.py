from chat_rpg import ChatRpg
c = ChatRpg('chatrpg_config.cfg')
#print c.generate_character("riotgradius",5,10,5,10)
#print c.generate_character("derpderp",10,10,5,5)
#c.run_combat("riotgradius", "derpderp")
for x in range(0,100):
    c.gen_creature(1)
