import os
import urllib.parse
import urllib.request


def management_notification(message: str) -> None:
    """Display a management notification in the prototype."""
    print("\n=== MANAGEMENT NOTIFICATION ===")
    print(message)
    print("===============================\n")


def send_sms(message: str) -> bool:
    """
    Send an SMS when Twilio configuration and ENABLE_REAL_SMS=true
    are available. Otherwise, run in safe simulation mode.
    """
    enable_real_sms = os.getenv("ENABLE_REAL_SMS", "false").lower() == "true"

    if not enable_real_sms:
        print(f"[SIMULATED SMS] {message}")
        return True

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER")
    to_number = os.getenv("MANAGEMENT_PHONE")

    if not all([account_sid, auth_token, from_number, to_number]):
        print("[SMS NOT SENT] Required Twilio configuration is missing.")
        return False

    data = urllib.parse.urlencode({
        "From": from_number,
        "To": to_number,
        "Body": message
    }).encode()

    url = (
        f"https://api.twilio.com/2010-04-01/Accounts/"
        f"{account_sid}/Messages.json"
    )

    password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, url, account_sid, auth_token)

    auth_handler = urllib.request.HTTPBasicAuthHandler(password_manager)
    opener = urllib.request.build_opener(auth_handler)

    try:
        request = urllib.request.Request(url, data=data, method="POST")
        opener.open(request, timeout=10)
        return True
    except Exception as exc:
        print(f"[SMS ERROR] {exc}")
        return False


def notify_management(
    message: str,
    send_mobile_sms: bool = True
) -> dict:
    """Send the management notification and optional mobile SMS."""
    management_notification(message)

    sms_status = None
    if send_mobile_sms:
        sms_status = send_sms(message)

    return {
        "management_notification": True,
        "mobile_sms": sms_status
    }


if __name__ == "__main__":
    test_message = (
        "FreshChoice SafeStore alert: abnormal storage condition "
        "detected. Please review the management dashboard."
    )

    result = notify_management(test_message)
    print("Notification result:", result)
