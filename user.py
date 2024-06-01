import json
import os

folder_path = 'messages'
folder_list = ["messages/"+folder for folder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder))]
file_list = ["messages/"+folder+"/messages.json" for folder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder))]
channel_info_list = ["messages/"+folder+"/channel.json" for folder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder))]
index = json.load(open("messages/index.json", "r"))

monthly_message_counts = {}
meow_count = {}
for file in file_list:
    with open(file, 'r', encoding="utf-8") as f:
        data = json.load(f)
        for message in data:
            date = message['Timestamp']
            month = date[:7]
            # Add the message to the count for that month
            if month in monthly_message_counts:
                monthly_message_counts[month] += 1
            else:
                monthly_message_counts[month] = 1
            # Meow test
            if "meow" in message['Contents'].lower() or "miaou" in message['Contents'].lower():
                if month in meow_count:
                    meow_count[month] += message['Contents'].lower().count("meow") + message['Contents'].lower().count("miaou")
                else:
                    meow_count[month] = message['Contents'].lower().count("meow") + message['Contents'].lower().count("miaou")

# Server stats
server_message_counts = {}
messages_sent_in_servers = 0
messages_sent_in_dms = 0
people_dm_counts = {}
for folder in folder_list:
    with open(folder + "/channel.json", 'r', encoding="utf-8") as f:
        server_data = json.load(f)
        # DMs
        if server_data['type'] == 1 or server_data['type'] == 3: # 1 is DM, 3 is group DM
            with open(folder + "/messages.json", 'r', encoding="utf-8") as f:
                data = json.load(f)
                msg_count = data.__len__()
                messages_sent_in_dms += msg_count
                if server_data['type'] == 1: channel_name = index[server_data['id']].replace("Direct Message with ", "").replace("#0", "")
                else: channel_name = server_data.get('name', None)
                if channel_name is None or channel_name == "":
                    channel_name = "@Unknown"
                if channel_name in people_dm_counts:
                    people_dm_counts[channel_name] += msg_count
                else:
                    people_dm_counts[channel_name] = msg_count
                messages_sent_in_dms += msg_count
        else:
            with open(folder + "/messages.json", 'r', encoding="utf-8") as f:
                data = json.load(f)
                msg_count = data.__len__()
                messages_sent_in_servers += msg_count
            if 'guild' in server_data:
                server_name = server_data['guild']['name']
                with open(folder + "/messages.json", 'r', encoding="utf-8") as f:
                    data = json.load(f)
                    msg_count = data.__len__()
                    if server_name in server_message_counts:
                        server_message_counts[server_name] += msg_count
                    else:
                        server_message_counts[server_name] = msg_count
            else:
                server_name = index[server_data['id']].split(" in ")[-1]
                with open(folder + "/messages.json", 'r', encoding="utf-8") as f:
                    data = json.load(f)
                    msg_count = data.__len__()
                    if server_name in server_message_counts:
                        server_message_counts[server_name] += msg_count
                    else:
                        server_message_counts[server_name] = msg_count

try:
    os.mkdir("output")
except FileExistsError:
    pass

# Monthly message counts
sorted_keys = sorted(monthly_message_counts.keys())
sortie = open("output/monthly_message_counts.csv", "w")
sortie.write("month,count\n")
for key in sorted_keys:
    sortie.write(key + "," + str(monthly_message_counts[key]) + "\n")
sortie.close()

# Meow counts
sorted_keys = sorted(meow_count.keys())
sortie = open("output/meow_counts.csv", "w")
sortie.write("month,count\n")
for key in sorted_keys:
    sortie.write(key + "," + str(meow_count[key]) + "\n")
sortie.close()

# Server message counts
sorted_keys = sorted(server_message_counts.keys(), key=lambda k: server_message_counts[k], reverse=True)
sortie = open("output/server_message_counts.csv", "w", encoding="utf-8")
sortie.write("server,count\n")
for key in sorted_keys:
    sortie.write('"'+key+'"'+ "," + str(server_message_counts[key]) + "\n")
sortie.close()

# Messages sent in servers vs dms
sortie = open("output/server_dm_ratio.csv", "w")
sortie.write("type,count\n")
sortie.write("server," + str(messages_sent_in_servers) + "\n")
sortie.write("dm," + str(messages_sent_in_dms) + "\n")
sortie.close()

# Messages sent to people in dms
sorted_keys = sorted(people_dm_counts.keys(), key=lambda k: people_dm_counts[k], reverse=True)
sortie = open("output/people_dm_counts.csv", "w")
sortie.write("person,count\n")
others = 0
for key in sorted_keys:
    if key == "@Unknown":
        others += people_dm_counts[key]
    else:
        sortie.write(key + "," + str(people_dm_counts[key]) + "\n")
sortie.write("Others," + str(others) + "\n")
sortie.close()
