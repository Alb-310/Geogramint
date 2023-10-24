import datetime
import uuid

generated_uuids = set()


def generate_unique_uuid_string():
    global generated_uuids
    while True:
        new_uuid = uuid.uuid4()
        uuid_string = str(new_uuid)
        if uuid_string not in generated_uuids:
            generated_uuids.add(uuid_string)
            return uuid_string


def generate_unix_timestamp_milliseconds():
    now = datetime.datetime.now()
    timestamp_milliseconds = int(now.timestamp() * 1000)
    return timestamp_milliseconds


def generate_empty_dexie_json():
    data = {
        "entities": [],
        "relations": []
    }

    return data


def fill_dexie_json(users, groups, location, data, extended_report):
    creationdate = generate_unix_timestamp_milliseconds()
    origin_id = generate_unique_uuid_string()
    data["entities"].append({
        "comments": "",
        "critical": False,
        "typeId": "clh6rm4cqtxi60bw1w134w6bj",
        "value": location,
        "id": origin_id,
        "creationDate": creationdate,
        "editionDate": creationdate
    })

    for user in users:
        if extended_report == "False" and user.distance != "500" and user.distance != "1000" and user.distance != "2000":
            continue
        id = generate_unique_uuid_string()
        if user.distance == "500":
            color = "6"
        elif user.distance == "1000":
            color = "1"
        elif user.distance == "2000":
            color = "8"
        else:
            color = "2"
        data["entities"].append({
            "comments": f"Telegram ID: {user.id}\nName: {user.firstname} {user.lastname if user.lastname is not None else ''}\nUsername:{user.username}\nPhone: {user.phone}",
            "critical": False,
            "typeId": "clh6s4hvvtyfk0buj91gibjf9",
            "value": f"User: {user.username[1:-1] if user.username is not None else user.firstname[1:-1]}{' ' + user.lastname[1:-1] if user.username is None and user.lastname is not None else ''}",
            "id": id,
            "creationDate": creationdate,
            "colorNum": f"{color}",
            "editionDate": creationdate
        })

        id_relation = generate_unique_uuid_string()
        data["relations"].append({
            "bidirectional": False,
            "comments": "",
            "critical": False,
            "label": f"{user.distance}m",
            "rating": 3,
            "source": "Geogramint",
            "originId": origin_id,
            "targetId": id,
            "creationDate": creationdate,
            "id": id_relation,
            "resource": "Geogramint",
        })

        if user.username is not None:
            username_id = generate_unique_uuid_string()
            id_relation_username = generate_unique_uuid_string()
            data["entities"].append({
                "comments": "",
                "critical": False,
                "typeId": "clh6rf805twci0bujhft9fc5m",
                "value": f"{user.username[1:-1]}",
                "id": username_id,
                "creationDate": creationdate,
                "colorNum": "4",
                "editionDate": creationdate
            })

            data["relations"].append({
                "bidirectional": False,
                "comments": "",
                "critical": False,
                "label": "",
                "rating": 3,
                "source": "Geogramint",
                "originId": id,
                "targetId": username_id,
                "creationDate": creationdate,
                "id": id_relation_username,
                "resource": "Geogramint"
            })

        if user.id is not None:
            id_id = generate_unique_uuid_string()
            id_relation_id = generate_unique_uuid_string()
            data["entities"].append({
                "comments": "Telegram ID",
                "critical": False,
                "typeId": "clh6rg2butu0h0buuof2ycaq6",
                "value": f"{user.id}",
                "id": id_id,
                "creationDate": creationdate,
                "colorNum": "4",
                "editionDate": creationdate
            })

            data["relations"].append({
                "bidirectional": False,
                "comments": "",
                "critical": False,
                "label": "",
                "rating": 3,
                "source": "Geogramint",
                "originId": id,
                "targetId": id_id,
                "creationDate": creationdate,
                "id": id_relation_id,
                "resource": "Geogramint"
            })

        if user.phone is not None:
            phone_id = generate_unique_uuid_string()
            id_relation_phone = generate_unique_uuid_string()
            data["entities"].append({
                "comments": "",
                "critical": False,
                "typeId": "clh6rdbkqtw6p0bujaqrekndj",
                "value": f"+{user.phone[1:-1]}",
                "id": phone_id,
                "creationDate": creationdate,
                "colorNum": "4",
                "editionDate": creationdate
            })

            data["relations"].append({
                "bidirectional": False,
                "comments": "",
                "critical": False,
                "label": "",
                "rating": 3,
                "source": "Geogramint",
                "originId": id,
                "targetId": phone_id,
                "creationDate": creationdate,
                "id": id_relation_phone,
                "resource": "Geogramint"
            })

        if user.firstname is not None:
            name_id = generate_unique_uuid_string()
            id_relation_name = generate_unique_uuid_string()
            data["entities"].append({
                "comments": f"{'Last Name Unknown' if user.lastname is None else ''}",
                "critical": False,
                "typeId": "clh6rcu0jtw4n0bujt1zdz84r",
                "value": f"{user.firstname[1:-1]}{' ' + user.lastname[1:-1] if user.lastname is not None else ''}",
                "id": name_id,
                "creationDate": creationdate,
                "colorNum": "4",
                "editionDate": creationdate
            })

            data["relations"].append({
                "bidirectional": False,
                "comments": "",
                "critical": False,
                "label": "",
                "rating": 3,
                "source": "Geogramint",
                "originId": id,
                "targetId": name_id,
                "creationDate": creationdate,
                "id": id_relation_name,
                "resource": "Geogramint"
            })

    for group in groups:
        if extended_report == "False" and group.distance != "500" and group.distance != "1000" and group.distance != "2000":
            continue
        id = generate_unique_uuid_string()
        if group.distance == "500":
            color = "6"
        elif group.distance == "1000":
            color = "1"
        elif group.distance == "2000":
            color = "8"
        else:
            color = "2"
        data["entities"].append({
            "comments": f"Telegram ID: {group.id}\nGroup Name: {group.name}",
            "critical": False,
            "typeId": "clh6s4hvvtyfk0buj91gibjf9",
            "value": f"Group: {group.name}",
            "id": id,
            "creationDate": creationdate,
            "colorNum": f"{color}",
            "editionDate": creationdate
        })

        id_relation = generate_unique_uuid_string()
        data["relations"].append({
            "bidirectional": False,
            "comments": "",
            "critical": False,
            "label": f"{group.distance}m",
            "rating": 3,
            "source": "Geogramint",
            "originId": origin_id,
            "targetId": id,
            "creationDate": creationdate,
            "id": id_relation,
            "resource": "Geogramint"
        })

    return data
