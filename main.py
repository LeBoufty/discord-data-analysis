import json
import os

folder_path = "Messages"
folder_list = [
    "Messages/" + folder
    for folder in os.listdir(folder_path)
    if os.path.isdir(os.path.join(folder_path, folder))
]
file_list = [
    "Messages/" + folder + "/messages.json"
    for folder in os.listdir(folder_path)
    if os.path.isdir(os.path.join(folder_path, folder))
]
channel_info_list = [
    "Messages/" + folder + "/channel.json"
    for folder in os.listdir(folder_path)
    if os.path.isdir(os.path.join(folder_path, folder))
]
index = json.load(open("Messages/index.json", "r"))
YEAR: str | None = "2025"

monthly_message_counts = {}
meow_count = {}
for file in file_list:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        if YEAR is not None:
            data = [m for m in data if m["Timestamp"][:4] == YEAR]
        for message in data:
            date = message["Timestamp"]
            month = date[:7]
            # Add the message to the count for that month
            if month in monthly_message_counts:
                monthly_message_counts[month] += 1
            else:
                monthly_message_counts[month] = 1
            # Meow test
            if (
                "meow" in message["Contents"].lower()
                or "miaou" in message["Contents"].lower()
            ):
                if month in meow_count:
                    meow_count[month] += message["Contents"].lower().count(
                        "meow"
                    ) + message["Contents"].lower().count("miaou")
                else:
                    meow_count[month] = message["Contents"].lower().count(
                        "meow"
                    ) + message["Contents"].lower().count("miaou")

# Server stats
server_message_counts = {}
messages_sent_in_servers = 0
messages_sent_in_dms = 0
people_dm_counts = {}
for folder in folder_list:
    with open(folder + "/channel.json", "r", encoding="utf-8") as f:
        server_data = json.load(f)
        # DMs
        if (
            server_data["type"] == "DM" or server_data["type"] == "GROUP_DM"
        ):  # 1 is DM, 3 is group DM
            with open(folder + "/messages.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if YEAR is not None:
                    data = [m for m in data if m["Timestamp"][:4] == YEAR]
                msg_count = data.__len__()
                messages_sent_in_dms += msg_count
                if server_data["type"] == "DM":
                    channel_name = (
                        index[server_data["id"]]
                        .replace("Direct Message with ", "")
                        .replace("#0", "")
                    )
                else:
                    channel_name = server_data.get("name", None)
                if channel_name is None or channel_name == "":
                    channel_name = "@Unknown"
                if channel_name in people_dm_counts:
                    people_dm_counts[channel_name] += msg_count
                else:
                    people_dm_counts[channel_name] = msg_count
                messages_sent_in_dms += msg_count
        else:
            with open(folder + "/messages.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if YEAR is not None:
                    data = [m for m in data if m["Timestamp"][:4] == YEAR]
                msg_count = data.__len__()
                messages_sent_in_servers += msg_count
            if "guild" in server_data:
                server_name = server_data["guild"]["name"]
                with open(folder + "/messages.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if YEAR is not None:
                        data = [m for m in data if m["Timestamp"][:4] == YEAR]
                    msg_count = data.__len__()
                    if server_name in server_message_counts:
                        server_message_counts[server_name] += msg_count
                    else:
                        server_message_counts[server_name] = msg_count
            else:
                server_name = index[server_data["id"]].split(" in ")[-1]
                with open(folder + "/messages.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if YEAR is not None:
                        data = [m for m in data if m["Timestamp"][:4] == YEAR]
                    msg_count = data.__len__()
                    if server_name in server_message_counts:
                        server_message_counts[server_name] += msg_count
                    else:
                        server_message_counts[server_name] = msg_count

# Montly messages per server :
monthly_server_message_counts = {}
monthly_dm_message_counts = {}
servers = []
for folder in folder_list:
    with open(folder + "/channel.json", "r", encoding="utf-8") as f:
        server_data = json.load(f)
        if (
            server_data["type"] == "DM" or server_data["type"] == "GROUP_DM"
        ):  # 1 is DM, 3 is group DM
            with open(folder + "/messages.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if YEAR is not None:
                    data = [m for m in data if m["Timestamp"][:4] == YEAR]
                for message in data:
                    date = message["Timestamp"]
                    month = date[:7]
                    if server_data["type"] == "DM":
                        channel_name = (
                            index[server_data["id"]]
                            .replace("Direct Message with ", "")
                            .replace("#0", "")
                        )
                    else:
                        channel_name = server_data.get("name", None)
                    if channel_name is None or channel_name == "":
                        channel_name = "@Unknown"
                    if month in monthly_dm_message_counts:
                        if channel_name in monthly_dm_message_counts[month]:
                            monthly_dm_message_counts[month][channel_name] += 1
                        else:
                            monthly_dm_message_counts[month][channel_name] = 1
                    else:
                        monthly_dm_message_counts[month] = {channel_name: 1}
        else:
            with open(folder + "/messages.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if YEAR is not None:
                    data = [m for m in data if m["Timestamp"][:4] == YEAR]
                for message in data:
                    date = message["Timestamp"]
                    month = date[:7]
                    if "guild" in server_data:
                        server_name = server_data["guild"]["name"]
                        if server_name not in servers:
                            servers.append(server_name)
                        if month in monthly_server_message_counts:
                            if server_name in monthly_server_message_counts[month]:
                                monthly_server_message_counts[month][server_name] += 1
                            else:
                                monthly_server_message_counts[month][server_name] = 1
                        else:
                            monthly_server_message_counts[month] = {server_name: 1}
                    else:
                        server_name = index[server_data["id"]].split(" in ")[-1]
                        if server_name not in servers:
                            servers.append(server_name)
                        if month in monthly_server_message_counts:
                            if server_name in monthly_server_message_counts[month]:
                                monthly_server_message_counts[month][server_name] += 1
                            else:
                                monthly_server_message_counts[month][server_name] = 1
                        else:
                            monthly_server_message_counts[month] = {server_name: 1}

try:
    os.mkdir("output")
except FileExistsError:
    pass

# Monthly message counts
sorted_keys = sorted(monthly_message_counts.keys())
sortie = open("output/monthly_message_counts.csv", "w", encoding="utf-8")
sortie.write("month,count\n")
for key in sorted_keys:
    sortie.write(key + "," + str(monthly_message_counts[key]) + "\n")
sortie.close()

# Meow counts
sorted_keys = sorted(meow_count.keys())
sortie = open("output/meow_counts.csv", "w", encoding="utf-8")
sortie.write("month,count\n")
for key in sorted_keys:
    sortie.write(key + "," + str(meow_count[key]) + "\n")
sortie.close()

# Server message counts
sorted_keys = sorted(
    server_message_counts.keys(), key=lambda k: server_message_counts[k], reverse=True
)
sortie = open("output/server_message_counts.csv", "w", encoding="utf-8")
sortie.write("server,count\n")
for key in sorted_keys:
    if server_message_counts[key] > 0:
        sortie.write('"' + key + '"' + "," + str(server_message_counts[key]) + "\n")
sortie.close()

# Messages sent in servers vs dms
sortie = open("output/server_dm_ratio.csv", "w", encoding="utf-8")
sortie.write("type,count\n")
sortie.write("server," + str(messages_sent_in_servers) + "\n")
sortie.write("dm," + str(messages_sent_in_dms) + "\n")
sortie.close()

# Messages sent to people in dms
sorted_keys = sorted(
    people_dm_counts.keys(), key=lambda k: people_dm_counts[k], reverse=True
)
sortie = open("output/people_dm_counts.csv", "w", encoding="utf-8")
sortie.write("person,count\n")
others = 0
for key in sorted_keys:
    if people_dm_counts[key] > 0:
        if key == "@Unknown":
            others += people_dm_counts[key]
        else:
            sortie.write('"' + key + '"' + "," + str(people_dm_counts[key]) + "\n")
sortie.write("Others," + str(others) + "\n")
sortie.close()

# Monthly messages per server
sorted_months = sorted(monthly_server_message_counts.keys())
sorted_servers = sorted(
    servers,
    key=lambda server: next(
        (
            month
            for month in sorted_months
            if monthly_server_message_counts[month].get(server, 0) != 0
        ),
        None,
    ),
)
sortie = open("output/monthly_server_message_counts.csv", "w", encoding="utf-8")
sortie.write("month," + '"' + '","'.join(sorted_servers) + '"' + "\n")
for month in sorted_months:
    line = month
    for server in sorted_servers:
        if server in monthly_server_message_counts[month]:
            line += "," + str(monthly_server_message_counts[month][server])
        else:
            line += ",0"
    sortie.write(line + "\n")
sortie.close()

# Monthly messages per dm
sorted_months = sorted(monthly_dm_message_counts.keys())
sorted_dms = sorted(
    people_dm_counts.keys(), key=lambda dm: people_dm_counts[dm], reverse=True
)
sortie = open("output/monthly_dm_message_counts.csv", "w", encoding="utf-8")
sortie.write("month," + '"' + '","'.join(sorted_dms) + '"' + "\n")
for month in sorted_months:
    line = month
    for dm in sorted_dms:
        if dm in monthly_dm_message_counts[month]:
            line += "," + str(monthly_dm_message_counts[month][dm])
        else:
            line += ",0"
    sortie.write(line + "\n")
sortie.close()
