# Kees

A command line interface for reading passwords from [1Password](https://agilebits.com/onepassword) vaults.

[Agile Bits](https://agilebits.com) does not officially support Linux. This lack of agility bites, so I built a vault _reader_, but cannot build a vault _writer_.

This project was highly influenced by George Brock's [1pass](https://github.com/georgebrock/1pass)


# Install It

```
$ pip install kees
```


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
