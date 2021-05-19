# An Internet of Things Office Door Sign Using iOS Shortcuts

## Motivation

See [the original README](https://github.com/mikerenfro/iot-office-door-sign) and [the Raspberry Pi variant](https://github.com/mikerenfro/iot-office-door-sign/blob/master/Raspberry-Pi/README-Raspberry.md), except by mid-2021, I looked into if I could post messages to the door sign with "Hey, Siri" on either my watch or my phone. Turns out the watch was a no-go, but the phone works fine using Shortcuts.

## Prerequisites

- iOS device that can run Shortcuts
- Twitter app for iOS

The shortcuts are pretty straightforward. Some of them are static text, like the one for "In Office":

![In office overview]

Others prompt for input, either for literal text like a location, or parsed like a return time.

![Location overview]

![Back at overview]

All of them run a second Shortcut that will append the current millisecond value to the end of the tweet text:

![Tweet text milliseconds overview]

The less obvious part of that shortcut is the format string required for milliseconds, `{SSS}`.

![Tweet text milliseconds detail]

The end result is a Twitter screen where I can hit the Tweet button, and my sign gets updated as usual:

![In office result]

[In office overview]: in-office-overview.png
[Location overview]: location-overview.png
[Back at overview]: back-at-overview.png
[Tweet text milliseconds overview]: tweet-text-milliseconds-overview.png
[Tweet text milliseconds detail]: tweet-text-milliseconds-detail.png
[In office result]: in-office-result.png
