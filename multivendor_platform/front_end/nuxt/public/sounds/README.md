# Chat Notification Sounds

This directory contains audio files for chat notifications.

## Required Files

### notification.mp3
- **Purpose**: Plays when a new message is received
- **Duration**: 1-2 seconds recommended
- **Format**: MP3
- **Volume**: Should be normalized to prevent loud playback

## Installation

1. Download or create your notification sound
2. Convert it to MP3 format if needed
3. Place the file in this directory: `/public/sounds/notification.mp3`
4. The chat system will automatically use it

## Free Sound Resources

You can download free notification sounds from:
- https://notificationsounds.com/
- https://freesound.org/
- https://mixkit.co/free-sound-effects/notification/

## Customization

To use a different sound:
1. Replace the `notification.mp3` file
2. Or update the sound path in `ChatWidget.vue`:

```javascript
const audio = new Audio('/sounds/your-custom-sound.mp3')
```

## User Control

Users can enable/disable notification sounds through:
- Chat widget menu (⋮ icon)
- The setting is saved in browser localStorage
- Default: Enabled

## Testing

To test the notification sound:
1. Open two browser windows
2. Log in with different accounts
3. Start a chat between them
4. Send a message from one account
5. The other account should hear the notification sound

## Notes

- Sound only plays when receiving messages from others
- Sound won't play for your own messages
- Browser must allow audio playback
- Some browsers require user interaction before playing audio

