from utils.config_utils import ConfigUtils
import requests

def _send_notification(config_path: str, notification_name: str, notification_title: str=None, notification_text: str=None) -> None:
	"""
    Send a notification using the specified notification configuration.

    Args:
        config_path (str): Path to the configuration file.
        notification_name (str): The name of the notification configuration in the file.
        notification_title (str, optional): Title of the notification. Defaults to None.
        notification_text (str, optional): Text content of the notification. Defaults to None.
	"""
	c = ConfigUtils(config_path)
	r = requests.post(
				getattr(c, notification_name),
				json={'text': notification_text, 'title': notification_title})

def send_new_album_notification(config_file_path: str, new_albums: list) -> None:
	"""
    Send a notification about newly added albums.

    Args:
        config_file_path (str): Path to the configuration file.
        new_albums (list): List of dictionaries containing information about new albums.

    Example of dictionary in new_albums:
        {'artist': 'Artist Name', 'album': 'Album Name'}

    The function sends a notification about each album in the new_albums list.
	"""
	title = f'Added the following {len(new_albums)} album(s) to your library:'
	text  = ''
	for entry in new_albums:
		text += f'- {entry["album"]} by {entry["artist"]}\n'
	text = text.rstrip()
	_send_notification(config_file_path, 'new_album', title, text)

def send_error_notification(config_file_path: str, location: str) -> None:
	"""
    Send an error notification.

    Args:
        config_file_path (str): Path to the configuration file.
        location (str): The location or context where the error occurred.

    The function sends an error notification with details about the error and its location.
	"""
	title = f'Error while running Elwë in {location}.'
	text  = ''
	_send_notification(config_file_path, 'error', title, text)


if __name__ == '__main__':
	_send_notification('new_album', notification_title='El', notification_text='Testing')