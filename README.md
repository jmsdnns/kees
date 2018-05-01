# Kees

A command line interface for reading passwords from [1Password](https://agilebits.com/onepassword) vaults.

[Agile Bits](https://agilebits.com) does not officially support Linux. This lack of agility bites, so I built a vault _reader_, but cannot build a vault _writer_.

This project was highly influenced by George Brock's [1pass](https://github.com/georgebrock/1pass)

_It's written in Python 3 too, in case that's something you care about_


# Using it

Get some password out of your vault like this

```
$ kees gmail
Password:
y0uRp@ssw0rd
```

Put your password in your copy buffer

```
$ kees soundcloud | xclip -i selection clip_board
$
```

Kees assumes the keychain is stored at `~/Dropbox/1Password.agilekeychain`, _unless_ you tell it otherwise with the `--path` flag.

```
$ kees --path ~/whatever/1Password.agilekeychain gmail
...
```


# Install It

Go get it

```
$ cd $SOMEWHERE
$ git clone https://github.com/jmsdnns/kees
```

Then install it

```
$ cd kees
$ pipenv install .
```

And then make it a command by putting this in your shell.

```
$ alias kees="PIPENV_PIPFILE=$SOMEWHERE/kees/Pipfile pipenv run kees"
$ kees "soundcloud"
Password:

```
