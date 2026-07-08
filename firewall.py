import os
import ipaddress
from datetime import datetime

# -------------------------------
# Terminal Colors
# -------------------------------
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

# -------------------------------
# Log Actions
# -------------------------------
def log_action(action, ip):
    with open("firewall.log", "a") as log:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"{time} - {action} - {ip}\n")

# -------------------------------
# Validate IP Address
# -------------------------------
def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

# -------------------------------
# Display Menu
# -------------------------------
def menu():
    print(f"\n{CYAN}========================================={RESET}")
    print(f"{BLUE}        PYSHIELD FIREWALL RESET}")
    print(f"{CYAN}========================================={RESET}")
    print("1. Block IP")
    print("2. Unblock IP")
    print("3. View Firewall Rules")
    print("4. View Log File")
    print("5. Flush All Firewall Rules")
    print("6. Exit")
    print(f"{CYAN}========================================={RESET}")

# -------------------------------
# Main Program
# -------------------------------
while True:

    menu()

    choice = input("\nEnter your choice: ")

    # --------------------------------
    # Block IP
    # --------------------------------
    if choice == "1":

        ip = input("Enter the IP address to block: ")

        if not validate_ip(ip):
            print(f"{RED}❌ Invalid IP address!{RESET}")
            continue

        command = f"sudo iptables -A INPUT -s {ip} -j DROP"
        result = os.system(command)

        if result == 0:
            log_action("BLOCKED", ip)
            print(f"{GREEN}✅ {ip} has been blocked.{RESET}")
        else:
            print(f"{RED}❌ Failed to block IP.{RESET}")

    # --------------------------------
    # Unblock IP
    # --------------------------------
    elif choice == "2":

        ip = input("Enter the IP address to unblock: ")

        if not validate_ip(ip):
            print(f"{RED}❌ Invalid IP address!{RESET}")
            continue

        command = f"sudo iptables -D INPUT -s {ip} -j DROP"
        result = os.system(command)

        if result == 0:
            log_action("UNBLOCKED", ip)
            print(f"{GREEN}✅ {ip} has been unblocked.{RESET}")
        else:
            print(f"{RED}❌ Rule not found or unable to remove it.{RESET}")

    # --------------------------------
    # View Firewall Rules
    # --------------------------------
    elif choice == "3":

        print(f"\n{YELLOW}========== Firewall Rules =========={RESET}\n")
        os.system("sudo iptables -L --line-numbers")

    # --------------------------------
    # View Log File
    # --------------------------------
    elif choice == "4":

        print(f"\n{YELLOW}========== Firewall Log =========={RESET}\n")

        if os.path.exists("firewall.log"):
            with open("firewall.log", "r") as file:
                data = file.read()

                if data.strip():
                    print(data)
                else:
                    print("No logs available.")

        else:
            print("Log file not found.")

    # --------------------------------
    # Flush Firewall Rules
    # --------------------------------
    elif choice == "5":

        confirm = input(
            f"{YELLOW}Are you sure you want to remove ALL firewall rules? (yes/no): {RESET}"
        )

        if confirm.lower() == "yes":

            os.system("sudo iptables -F")

            print(f"{GREEN}✅ All firewall rules have been removed.{RESET}")

        else:

            print(f"{YELLOW}Operation cancelled.{RESET}")

    # --------------------------------
    # Exit
    # --------------------------------
    elif choice == "6":

        print(f"{BLUE}👋 Thank you for using PyShield Firewall!{RESET}")
        break

    # --------------------------------
    # Invalid Choice
    # --------------------------------
    else:

        print(f"{RED}❌ Invalid choice! Please try again.{RESET}")
