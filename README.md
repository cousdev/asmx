# ASMX
ASMX is a development platform, comprised of a modular assembler, and a VM which runs on [Scratch](https://scratch.mit.edu/).
It allows you to write simple programs in a custom assembly-like language, and then execute them in an educational and visual environment.
ASMX is perfect for people who want to learn how computers work with low-level programming, people looking to contribute to a project for the first time, or people who want to create interesting projects whilst still using Scratch.

---

## Features
- ⚙️ **Macro-based Assembler** - Powerful macro system with modular namespaces and grammar extensions
- 🧱 **Scratch VM** - The virtual machine is implemented in Scratch, making it visual, easy to experiment with, and beginner-friendly
- 📦 **Package System** - Create and load your own macro packages, allowing you to extend the instruction set
- 🕹️ **Demo Projects Included** - Demo projects like Rock Paper Scissors are included to help you learn and experiment
- 💡 **Made For Learning** - Built with simplicity and education in mind, perfect for exploring how computers work

---

## Getting Started

### 🧰 Requirements
- Python 3.8 or above
- A local clone/copy of this repo

### 🚀 Quick Start
To download ASMX, run:

```
pip install asmx
```

Congrats, you just installed ASMX! Open up the guide, by running:

```
asmx --docs
```

Then click on the Guide section.

## Project Structure
```
asmx/
├── asmx_core/           # Core Python package (assembler logic, macro dispatcher, parser, etc.)
│   ├── macros.py
│   ├── parser.py
│   └── packages/        # User-defined + Standard library packages
├── docs/                # Documentation for ASMX
├── asmx.py              # Entry point, run this file
README.md
setup.py
setup.cfg
...
```

## Documentation
Documentation is built with [MkDocs.](https://www.mkdocs.org/) To open the documentation, run:

```
asmx --docs
```

If you are looking to contribute to the documentation, go to the [asmx-docs repo.](https://github.com/cousdev/asmx-docs/)

## Contributing
All contributions are welcome! You could:
- Fix bugs
- Write documentation
- Create new packages
- Submit new demo programs or games
- Help add new features
- Simplify code
- Write tests
- Expand the VM's capabilities

If you're interested, just open an issue or pull request. Make sure your code is clean and commented where necessary.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## ⚠️ Important Note
The ASMX project is still in early development - expect changes and bugs!
