# nuitka-project: --enable-plugin=pyside6
# nuitka-project: --include-qt-plugins=platforminputcontexts
# nuitka-project: --noinclude-qt-translations
# nuitka-project: --include-data-dir=assets=assets
# nuitka-project: --include-data-files=style.qss=style.qss
# nuitka-project: --output-dir=deployment
# nuitka-project: --remove-output

# nuitka-project-if: {OS} == "Windows":
#    nuitka-project: --mode=onefile
#    nuitka-project: --windows-console-mode=disable
#    nuitka-project: --windows-icon-from-ico=assets/icon.ico
#    nuitka-project: --output-filename=prayer-pause.exe
# nuitka-project-else:
#    nuitka-project: --mode=standalone
#    nuitka-project: --output-filename=prayer-pause

from prayer_pause.main import main

if __name__ == "__main__":
    main()

