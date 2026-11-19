
# Blockcutter

## Download: [Modrinth](https://modrinth.com/datapack/blockcutter/version/latest)
### Minecraft Versions: 26.3
Adds quality of life features to the stonecutter and more!

## Features
- Convert blocks into slabs, stairs, walls or trapdoors
- Craft slabs, stairs and walls back into blocks
- Convert logs into wood

## Crafting
**Recipes**:

<img src="https://github.com/DominoWWW/Block-Cutter/blob/main/readme-images/recipes.gif?raw=true" width="300"/>

## Wiki

#### Installing:
Insert the zip file into your datapacks folder.

#### Uninstalling:
Delete the zip file.

#### Contributing
Clone the repository and install the development tools in a Python virtual environment:

```sh
git clone https://github.com/DominoWWW/Blockcutter.git
cd Blockcutter
python -m venv .venv
source .venv/bin/activate
python -m pip install beet bolt
```

##### build
Build the datapack with:

```sh
beet build
```

##### Testing
**Individual Tests:** \
```command
/test run <test>
```

**Run test server:** \
You need [carpet mod](https://modrinth.com/mod/carpet) and [GameTest Fabric](https://modrinth.com/mod/gametest-fabric) installed on a fabric server
Test server start command:
```sh
java -DbundlerMainClass="net.minecraft.gametest.Main" -jar server.jar --packs "<path/to/dir/with/the/datapack>"
```