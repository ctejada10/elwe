# Elwë
The Teleri were the greatest singer elves of Middle-Earth, and Elwë was one of
their leaders. This project helps me discover new music by searching aggregating
websites (e.g., Metacritic, Pitchfork) for the best new releases, and adds them
to my Apple Music library.

## Usage
This project is made up of two parts. The Python code you're browsing now, and
an [iOS Shortcut](https://www.icloud.com/shortcuts/475ea8fd1cee4a149b31fe471aa0e3f4)
that adds the albums to your Apple Music library.

### Running Python code
This project is run by executing `src/elwe.py [path/to/config/folder]`.

#### Apple Music authentication
This project assumes you have an Apple Developer account and a developer key as
well as a "Music User Token". Without them you won't be able to access the Apple
Music API.