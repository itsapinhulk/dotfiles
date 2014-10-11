#! /usr/bin/python
import os
import logging
import shutil
import subprocess

'''
sudo fc-cache -vf ~/.fonts
'''
gitConfigFile = os.path.abspath(os.path.join(os.path.dirname(__file__), 'git_settings/gitconfig'))
backupDir = os.path.expanduser('~/.backup')
createDirs = [
        '~/.backup',
        '~/.vim',
        '~/.fonts',
        '~/.config/fontconfig/conf.d',
    ]
setupMap = {
                                   'vimrc' : '~/.vimrc',
                                  'bashrc' : '~/.bashrc',
                              'dir_colors' : '~/.dir_colors',
        'git_settings/git-completion.bash' : '~/.git-completion.bash',
              'git_settings/git-prompt.sh' : '~/.git-prompt.sh',
                            'vim/autoload' : '~/.vim/autoload',
                              'vim/bundle' : '~/.vim/bundle',
         'fonts/10-powerline-symbols.conf' : '~/.config/fontconfig/conf.d/10-powerline-symbols.conf',
              'fonts/PowerlineSymbols.otf' : '~/.fonts/PowerlineSymbols.otf',
    }

def _setupFonts():
    if (0 == os.getuid()):
        fcCacheCommand = ['fc-cache', '-vf', '~/.fonts']
        subprocess.call(fcCacheCommand)
    else:
        logging.warn('Cannot run fc-cache without sudo')

def _setupGit():
    gitCommand = ['git', 'config', '--global', 'include.path', gitConfigFile]
    subprocess.call(gitCommand)

def _backupIfFile(filePath):
    if os.path.lexists(filePath):
        if os.path.islink(filePath):
            os.remove(filePath)
        else:
            shutil.copy(filePath, backupDir)
            os.remove(filePath)
  
def _main():
    for dirName in createDirs:
        actualDirName = os.path.expanduser(dirName)
        if not os.path.exists(actualDirName):
            os.makedirs(actualDirName)

    for origPath in setupMap.keys():
        targetPath = os.path.expanduser(setupMap[origPath])
        actualOrigPath = os.path.abspath(os.path.join(os.path.dirname(__file__), origPath))
        if os.path.exists(actualOrigPath):
            _backupIfFile(targetPath)
            os.symlink(actualOrigPath, targetPath)
        else:
            logging.warn('Specified path doesn\'t exist : ' + str(actualOrigPath))

    _setupGit()
    _setupFonts()
    
if '__main__' == __name__:
    _main()
