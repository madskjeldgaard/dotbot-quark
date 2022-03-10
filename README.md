[dotbot_repo]: https://github.com/anishathalye/dotbot

Plugin for [Dotbot][dotbot_repo], that adds ```quark``` directive, which allows you install [SuperCollider](https://supercollider.github.io/) packages aka. quarks. 

## Installation

1. Simply add this repo as a submodule of your dotfiles repository:
```
git submodule add https://github.com/madskjeldgaard/dotbot-quark.git
```

2. Pass this folder (or directly quark.py file) path with corresponding flag to your [Dotbot][dotbot_repo] script:
  - ```-p /path/to/file/quark.py```

  or

 - ```--plugin-dir /pato/to/plugin/folder```


## Example

```yaml
- quark:
  - https://codeberg.org/madskjeldgaard/mk-libs
  - atk-sc3
  - CC14
  - CuePlayer
```

## Known problems

This approach is very slow since it starts an sclang instance per quark to adhere more to dotbot conventions and to make it easier for dotbot to figure out which quark exactly failed/succeeded in installing.
