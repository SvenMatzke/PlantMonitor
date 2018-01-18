import machine


def set_and_put_to_deepsleep(time_in_s):
    """
    Puts your device to deepsleep for a given time.
    Hardware note:
    connect gpio16 to reset to be able to deep sleep

    :param time_in_s: time to be in deepsleep
    """
    # configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after 10 seconds (waking the device)
    rtc.alarm(rtc.ALARM0, time_in_s * 1000)

    # put the device to sleep
    machine.deepsleep()