from utils.config_utils import ConfigUtils
import requests

def _send_notification(config_path, notification_name, notification_title=None, notification_text=None):
	c = ConfigUtils(config_path)
	r = requests.post(
				getattr(c, notification_name),
				json={'text': notification_text, 'title': notification_title})

def send_new_album_notification(config_file_path, new_albums):
	title = f'Added the following {len(new_albums)} album(s) to your library:'
	text  = ''
	for entry in new_albums:
		text += f'- {entry["album"]} by {entry["artist"]}\n'
	text = text.rstrip()
	_send_notification(config_file_path, 'new_album', title, text)

def send_error_notification(config_file_path, location):
	title = f'Error while running Elwë in {location}.'
	text  = ''
	_send_notification(config_file_path, 'error', title, text)


if __name__ == '__main__':
	_send_notification('new_album', notification_title='El', notification_text='Testing')