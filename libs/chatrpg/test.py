from chat_rpg import ChatRpg
c = ChatRpg('chatrpg_config.cfg')
#print c.generate_character("riotgradius",5,10,5,10)
#print c.generate_character("derpderp",10,10,5,5)
#c.run_combat("riotgradius", 'c', "derpderp", 'c')
c.fill_enemy_db(100)
c.run_adventure()
