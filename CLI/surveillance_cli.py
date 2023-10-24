import json
import requests

"""
EXPERIMENTAL FEATURE
"""

def process_users(json_filename, output_filename):
    with open(json_filename, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    # Filter users with distances of 500 and 1000
    users_500 = [user for user in data if user["distance"] == "500"]
    users_1000 = [user for user in data if user["distance"] == "1000"]

    # Sort users alphabetically based on their first name
    sorted_users_500 = sorted(users_500, key=lambda user: user["id"])
    sorted_users_1000 = sorted(users_1000, key=lambda user: user["id"])

    def write_users_to_file(users, file):
        for user in users:
            file.write("ID: {}\n".format(user["id"]))
            file.write("First Name: {}\n".format(user["firstname"]))
            if user.get("lastname"):
                file.write("Last Name: {}\n".format(user["lastname"]))
            if user.get("username"):
                file.write("Username: {}\n".format(user["username"]))
            if user.get("phone"):
                file.write("Phone: {}\n".format(user["phone"]))
            file.write("Distance: {}m\n\n".format(user["distance"]))
            file.write("-" * 40 + "\n")  # Add a separator

    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("Users within Distance of 500m:\n")
        output_file.write("=" * 40 + "\n")
        write_users_to_file(sorted_users_500, output_file)

        output_file.write("\n\n")

        output_file.write("Users within Distance of 1000m:\n")
        output_file.write("=" * 40 + "\n")
        write_users_to_file(sorted_users_1000, output_file)


def send_webhook_notification(webhook_url, message, files):
    while message:
        current_message = message[:1500]
        message = message[1500:]
        payload = {
            "content": current_message,
            "username": "Geogramint",
            "avatar_url": "https://github.com/Alb-310/Geogramint/blob/master/appfiles/Geogramint.png?raw=true"
        }

        if files is not None:
            response = requests.post(webhook_url, files=files)
        else:
            response = requests.post(webhook_url, json=payload)
        if response.status_code == 200 or response.status_code == 204:
            print("Webhook notification sent successfully.")
        else:
            print("Failed to send webhook notification.")


