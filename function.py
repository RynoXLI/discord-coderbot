import sys
import numpy as np
import json

def check_multiples(msg):
  '''
  Check how many dice are being asked to be thrown

  Parameters:
  msg - discord.client.message object storing the received message
  
  returns number of dice thrown
  '''
  # Reverses String Before d
  msg = msg.strip()
  msg = msg[::-1]
  i = 0
  while i < len(msg) and msg[i].isdigit():
    i += 1
  if i == 0: return -1 # If No Given Numbers Return -1
  else:
    # Reverses Again After Finding When the Numbers Stop
    number_of_dice = int(msg[0:i][::-1])
    return number_of_dice

def extract_names(name):
  '''
  Function to separate discord username from id

  Parameters:
  name - discord.client.author object
  
  returns Username and UserID

  '''
  if (type(name) != "string"):
    name = str(name)
  name = name.split("#", 1)
  user = name[0]
  id = name[1]
  return user, id

async def coin_flip(myBot, message):
  '''
  Has the bot flip a coin and send the results.
  Responds to Flip and Coin in the same sentence

  Parameters:
  myBot - Coderbot Class Found in bot.py
  message - discord.client.message object storing the received message

  returns 1 on proper execution
  '''
  try:
    if '!coin' in message.content.lower().strip() or '!flip' in message.content.lower().strip():
        if np.random.randint(0, high=2) == 0:
          await message.channel.send("Heads")
        else:
          await message.channel.send("Tails")
  except Exception as inst:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
    await message.channel.send("```" + errorMsg + "```")
    return 0
  return 1

async def roll_dice(myBot, message):
  '''
  Rolls a die based on the message input

  Parameters:
  myBot - Coderbot Class Found in bot.py
  message - discord.client.message object storing the received message

  return 1 on proper execution
  '''
  try:
    stripped_msg = message.content.lower().strip()
    if ('roll:' in stripped_msg or "!roll" in stripped_msg or "!dice" in stripped_msg or "!die" in stripped_msg) and 'd' in stripped_msg:
        msg = message.content.lower().split('d', 1)
        start = msg[1]
        die_count = check_multiples(msg[0])
        if die_count == -1: die_count = 1
        faces = ''
        for i in start:
          if (i.isdigit()):
            faces += i
        if faces == '':
          await message.channel.send("Try Something Else Plz Dummy!")
          return

        faces = int(faces)
        if faces <= 0 or die_count > 100:
          await message.channel.send("Try Something Else Plz Dummy!")
          return
        else:
          results = [np.random.randint(1, high=(faces+1)) for _ in range(die_count)]
          if len(results) > 1:
            output = "Total Roll: " + str(die_count) + "d" + str(sum(results))
            for i, result in enumerate(results):
              output += "\nRoll " + str(i + 1) + ": 1d" + str(result)
              if result == 1 or result == faces:
                await message.add_reaction("<:thinkban:776586606358167602>")

          else:
            output = str(die_count) + "d" + str(results[0])
          if die_count == sum(results) or die_count * faces == sum(results):
            await message.add_reaction("<:thinkban:776586606358167602>")
          await message.channel.send(output)
  except Exception as inst:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
    await message.channel.send("```" + errorMsg + "```")
    return 0
  return 1  

async def dialogue_handler(myBot, message):
  '''
  Handles dialogue responses for bot

  Parameters:
    myBot - Coderbot Class Found in bot.py
    message - discord.client.message object being responded to

  returns 1 on proper execution
  '''
  try:
    # Bad Bot and Good Bot Messages With Live Updates to Statistics.json
    if "bad bot" in message.content.lower():
      await message.channel.send("I am so sowwry! I prowomise towo dowo better UwU!")
      # Statistics JSON File
      with open('statistics.json', 'r') as stats:
        data = json.load(stats)
        stats.close()
      with open('statistics.json', 'w') as stats:
        data['Phrases']['Bad Bot'] += 1
        json.dump(data, stats)
        stats.close()
    
    elif "good bot" in message.content.lower():
      await message.channel.send("Thank youwo vewwy muwuch! I will continuwue towo dowo my best OwO!")
      with open('statistics.json', 'r') as stats:
        data = json.load(stats)
        stats.close()
      with open('statistics.json', 'w') as stats:
        data['Phrases']['Good Bot'] += 1
        json.dump(data, stats)
        stats.close()

    # Checks Mentions for Individual/Group Messages
    if len(message.mentions) > 0:
      for name in message.mentions:
        if '!pogchamp' not in message.content.lower() and extract_names(message.author)[0].lower() == extract_names(name)[0].lower():
          msg = "```System.out.println(\"Sigh... Okay, I guess you can be my little Pogchamp. {0}, Come here\")```"
          await message.channel.send(msg.format(extract_names(message.author)[0]))
          return

      if '!pogchamp' in message.content.lower():
        if len(message.mentions) == 1 and "coderbot" == extract_names(message.mentions[0])[0].lower():
          output = "... Umm, sure I guess I can be my own little Pogchamp, you bully! :sob:"
        
        elif len(message.mentions) == 1:
          output = "```System.out.println(\"Sigh... Okay, I guess you can be my little Pogchamp. {0}, Come here\")```".format(extract_names(message.mentions[0])[0])

        else:
          editedStr = ''
          for i, user in enumerate(message.mentions):
            if extract_names(user)[0].lower() == "coderbot":
              continue 

            if i != (len(message.mentions) - 1):
              editedStr += str(extract_names(user)[0]) + ", "
            else:
              editedStr += "and " + str(extract_names(user)[0])
          output = "```System.out.println(\"Sigh... Okay, I guess you can be my little Pogchamps. {0}, Come here\")```".format(editedStr)

        # Output String is Built in the Conditionals Above and Sent
        await message.channel.send(output)

  except Exception as inst:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
    await message.channel.send("```" + errorMsg + "```")
    return 0

  return 1

async def reaction_handler(myBot, message):
  '''
  Similar to dialogue_handler, adds reaction emotes to certain messages

  Parameters:
    myBot - Coderbot Class Found in bot.py
    message - discord.client.message object being responded to

  returns 1 for correct 
  '''

  try:
    if str(message.author) == "Mat#5553" and np.random.randint(1, 21) == 1:
      await message.add_reaction("<:thinkban:776586606358167602>")

    if str(message.author) == "PokeProfRob#2670" and np.random.randint(1, 21) == 1:
      await message.add_reaction("<:mat:792252631765483520>")

    if message.content.lower().startswith('poll:') or message.content.lower().startswith('!poll'):
        await message.add_reaction("✅")
        await message.add_reaction("❌")

  except Exception as inst:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
    await message.channel.send("```" + errorMsg + "```")
    return 0
  return 1

async def sleeping_protocol(myBot, message):
  try:
    if myBot.asleep and ("ohayo" in message.content.lower() or (len(message.mentions) > 0 and extract_names(message.mentions[0])[0].lower()) == "coderbot"):
          await myBot.awaken()
          await message.channel.send("Good Morning Everyone! :heart:")
          return

    elif not myBot.asleep and message.content.lower() == "oyasumi" or "stop bot" in message.content.lower(): 
      #and extract_names(message.author)[0].lower() == "yvillia":
      await message.channel.send("Like totally nighty-nighters everyone! :kissing_heart:")
      await myBot.oyasumi()
      return

    else:
      return
    
  except Exception as inst:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
    await message.channel.send("```" + errorMsg + "```")
    return 0
  return 1
