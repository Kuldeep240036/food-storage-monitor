from notification_service import notify_management


def test_notification_flow():
    result = notify_management(
        "Test alert: abnormal storage condition detected.",
        send_mobile_sms=True
    )

    assert result["management_notification"] is True
    assert result["mobile_sms"] is True


if __name__ == "__main__":
    test_notification_flow()
    print("Notification test passed.")
