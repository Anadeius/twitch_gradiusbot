from chat_rpg import ChatRpg
c = ChatRpg('chatrpg_config.cfg')
print c.generate_character("riotgradius",10,10,5,5)
print c.generate_character("derpderp",10,10,5,5)
#c.run_combat("riotgradius", 'c', "derpderp", 'c')
#c.fill_enemy_db(100)
#c.run_adventure(2)
for l in range(0,5):
    c.give_xp('riotgradius', 100)
    #c.give_xp('derpderp', 100)
c.equip_items('riotgradius','crappychest', 'chest', [0,0,0,0])
c.get_character_sheet('riotgradius')
c.get_character_sheet('derpderp')
c.export_to_web()
